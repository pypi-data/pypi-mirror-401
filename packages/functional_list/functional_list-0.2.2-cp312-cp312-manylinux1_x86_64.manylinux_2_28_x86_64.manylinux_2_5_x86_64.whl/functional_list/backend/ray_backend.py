"""functional_list.backend.ray_backend

Ray backend implementation for ListMapper.

This backend executes ListMapper operations using Ray tasks.

Performance note
----------------
Scheduling one Ray task per item is typically slow for small per-item functions.
To reduce overhead, this backend supports *chunking*: one Ray task processes a
batch of items in a tight loop.

Notes:
- Ray is an optional dependency. This module does not import Ray at import-time.
  Ray is imported lazily when the backend is used.
- Functions passed to Ray must be serializable by Ray (cloudpickle).

Install:
- With uv: `uv add ray`
- With pip: `pip install ray`
"""

from __future__ import annotations

import heapq
from typing import Any, Callable, List, Optional, Sequence, TypeVar

from functional_list.backend._chunking import chunked, flatten
from functional_list.backend._distributed_utils import (
    DISTINCT_THRESHOLD,
    SORT_THRESHOLD,
    DistributedBackendMixin,
    calculate_chunk_size,
    chunk_distinct_function,
    chunk_reduce_function,
    chunk_sort_function,
    merge_pair_function,
)
from functional_list.backend.base import BackendError, BaseBackend

try:
    import ray  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    ray = None  # type: ignore[assignment]

T = TypeVar("T")
U = TypeVar("U")


class RayBackend(DistributedBackendMixin, BaseBackend):
    """Execute ListMapper operations on Ray.

    Parameters
    ----------
    address:
        Ray cluster address.
        - None: starts a local Ray instance (default)
        - "auto": connect to an existing cluster if available
        - or a specific address string

    init_kwargs:
        Extra keyword arguments forwarded to `ray.init(...)`.

    chunk_size:
        If provided (and > 1), the backend will submit one Ray task per chunk
        instead of one Ray task per element. This usually improves benchmark
        performance significantly for small per-item functions.

    Examples
    --------
    >>> from functional_list.list_functional_mapper import ListMapper
    >>> from functional_list.backend import RayBackend
    >>>
    >>> backend = RayBackend(address=None, chunk_size=10_000)
    >>> out = ListMapper[int](1, 2, 3).map(lambda x: x * x, backend=backend)
    >>> out.to_list()
    [1, 4, 9]
    """

    name = "ray"

    def __init__(
        self,
        *,
        address: Optional[str] = None,
        init_kwargs: Optional[dict] = None,
        chunk_size: Optional[int] = None,
    ):
        """Create a RayBackend.

        See class docstring for parameter descriptions.
        """

        self._address = address
        self._init_kwargs = init_kwargs or {}
        self._chunk_size = chunk_size

    def _ensure_ray(self):
        """Import and initialize Ray if needed."""
        if ray is None:
            raise BackendError("RayBackend requires 'ray'. Install with: uv add ray")

        if not ray.is_initialized():
            ray.init(address=self._address, **self._init_kwargs)
        return ray

    def map(self, data: Sequence[T], func: Callable[[T], U]) -> List[U]:
        """Apply a function to each element using Ray tasks.

        Parameters
        ----------
        data:
            Input sequence.
        func:
            Function applied to each element.

        Returns
        -------
        list
            The mapped results in the same order as `data`.
        """

        ray_mod = self._ensure_ray()

        chunk_size = self._chunk_size
        if chunk_size is None or chunk_size <= 1:

            @ray_mod.remote
            def _apply(x):
                return func(x)

            futures = [_apply.remote(x) for x in data]
            return ray_mod.get(futures)

        # Chunked execution: one task per chunk.
        chunks = chunked(data, chunk_size)

        @ray_mod.remote
        def _apply_chunk(xs):
            return [func(x) for x in xs]

        futures = [_apply_chunk.remote(xs) for xs in chunks]
        nested: List[List[U]] = ray_mod.get(futures)
        return flatten(nested)

    def _create_reduce_tasks(
        self, chunks: List[Sequence[T]], func: Callable[[T, T], T]
    ) -> List[T]:
        """Create reduce tasks for each pre-chunked segment."""
        ray_mod = self._ensure_ray()

        @ray_mod.remote
        def _reduce_chunk(xs: Sequence[T]):
            return chunk_reduce_function(xs, func)

        futures = [_reduce_chunk.remote(chunk) for chunk in chunks]
        return [r for r in ray_mod.get(futures) if r is not None]

    def _execute_reduce_tree(
        self, partial_results: List[T], func: Callable[[T, T], T]
    ) -> T:
        """Execute tree reduction over partial results using Ray tasks."""
        ray_mod = self._ensure_ray()

        results = partial_results
        while len(results) > 1:
            paired: List[Any] = []
            for i in range(0, len(results), 2):
                if i + 1 < len(results):
                    paired.append((results[i], results[i + 1]))
                else:
                    paired.append((results[i],))  # type: ignore[arg-type]

            @ray_mod.remote
            def _merge_pair(pair):
                return merge_pair_function(pair, func)

            futures = [_merge_pair.remote(pair) for pair in paired]
            results = ray_mod.get(futures)

        return results[0]

    def distinct(self, data: Sequence[T]) -> List[T]:
        """Remove duplicates using Ray's distributed processing.

        For large datasets, this uses Ray to process chunks in parallel,
        then combines unique elements locally.

        Parameters
        ----------
        data:
            Input sequence.

        Returns
        -------
        list
            List with duplicates removed, preserving first occurrence order.
        """
        ray_mod = self._ensure_ray()

        # For small datasets, use base implementation
        if len(data) < DISTINCT_THRESHOLD:
            return super().distinct(data)

        # For large datasets, use distributed deduplication
        chunk_size = calculate_chunk_size(len(data), self._chunk_size)
        chunks = list(chunked(data, chunk_size))

        @ray_mod.remote
        def _distinct_chunk(xs):
            return chunk_distinct_function(xs)

        # Get unique elements from each chunk in parallel
        futures = [_distinct_chunk.remote(chunk) for chunk in chunks]
        chunk_results = ray_mod.get(futures)

        # Combine results and deduplicate globally (must be done locally for order)
        combined = []
        for chunk_uniques in chunk_results:
            combined.extend(chunk_uniques)

        return list(dict.fromkeys(combined))

    def sort(
        self,
        data: Sequence[T],
        key: Optional[Callable[[T], Any]] = None,
        reverse: bool = False,
    ) -> List[T]:
        """Sort using Ray's distributed sorting capabilities.

        For large datasets, this uses a distributed sort pattern:
        1. Sort chunks in parallel
        2. Merge sorted chunks

        Parameters
        ----------
        data:
            Input sequence.
        key:
            Optional key function for sorting.
        reverse:
            If True, sort in descending order.

        Returns
        -------
        list
            Sorted list.
        """
        ray_mod = self._ensure_ray()

        # For small datasets, use base implementation
        if len(data) < SORT_THRESHOLD:
            return super().sort(data, key=key, reverse=reverse)

        # For large datasets, use distributed sort-merge
        chunk_size = calculate_chunk_size(len(data), self._chunk_size)
        chunks = list(chunked(data, chunk_size))

        @ray_mod.remote
        def _sort_chunk(xs):
            return chunk_sort_function(xs, key, reverse)

        # Sort each chunk in parallel
        futures = [_sort_chunk.remote(chunk) for chunk in chunks]
        sorted_chunks = ray_mod.get(futures)

        # Merge sorted chunks using heapq
        if reverse:
            merged = list(heapq.merge(*sorted_chunks, key=key, reverse=True))
        else:
            merged = list(heapq.merge(*sorted_chunks, key=key))

        return merged
