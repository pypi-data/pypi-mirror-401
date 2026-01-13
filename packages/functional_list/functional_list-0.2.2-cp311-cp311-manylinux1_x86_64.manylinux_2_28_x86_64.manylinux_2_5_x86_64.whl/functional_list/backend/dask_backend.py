"""Dask backend.

Optional dependency: dask

Performance note
----------------
Creating one Dask task per element is typically slow for small per-item
functions (scheduler/graph overhead dominates). This backend supports chunking:
one task processes a batch of items.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, Sequence, TypeVar

from functional_list.backend._chunking import chunked, flatten
from functional_list.backend._distributed_utils import (
    DistributedBackendMixin,
    chunk_distinct_function,
    chunk_reduce_function,
    chunk_sort_function,
    merge_pair_function,
)
from functional_list.backend.base import BackendError, BaseBackend

try:
    from dask import delayed  # type: ignore[import-not-found]
    from dask.base import compute  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    delayed = None  # type: ignore[assignment]
    compute = None  # type: ignore[assignment]

T = TypeVar("T")
U = TypeVar("U")


class DaskBackend(DistributedBackendMixin, BaseBackend):
    """Execute ListMapper operations using Dask (optional dependency).

    Parameters
    ----------
    scheduler:
        Scheduler passed to `dask.compute`. Common values: "threads", "processes".

    chunk_size:
        If provided (and > 1), one Dask task processes a chunk of items. This
        reduces overhead and is usually required for good benchmark results.
    """

    name = "dask"

    def __init__(
        self, *, scheduler: Optional[str] = None, chunk_size: Optional[int] = None
    ):
        self._scheduler = scheduler
        self._chunk_size = chunk_size

    @staticmethod
    def _ensure_dask():
        if delayed is None or compute is None:
            raise BackendError("DaskBackend requires 'dask'. Install with: uv add dask")
        return delayed, compute

    def map(self, data: Sequence[T], func: Callable[[T], U]) -> List[U]:
        d_delayed, d_compute = self._ensure_dask()

        chunk_size = self._chunk_size
        if chunk_size is None or chunk_size <= 1:
            tasks = [d_delayed(func)(x) for x in data]
            (results,) = d_compute(tasks, scheduler=self._scheduler)
            return list(results)

        chunks = chunked(data, chunk_size)

        @d_delayed
        def _apply_chunk(xs: Sequence[T]) -> List[U]:
            return [func(x) for x in xs]

        tasks = [_apply_chunk(xs) for xs in chunks]
        (nested,) = d_compute(tasks, scheduler=self._scheduler)
        return flatten(nested)

    def _create_reduce_tasks(
        self, chunks: List[Sequence[T]], func: Callable[[T, T], T]
    ) -> List[T]:
        """Create and execute reduce tasks for each chunk."""
        d_delayed, d_compute = self._ensure_dask()

        @d_delayed
        def _reduce_chunk(xs):
            return chunk_reduce_function(xs, func)

        partial_results = [_reduce_chunk(chunk) for chunk in chunks]
        (computed,) = d_compute(partial_results, scheduler=self._scheduler)
        return [r for r in computed if r is not None]

    def _execute_reduce_tree(
        self, partial_results: List[T], func: Callable[[T, T], T]
    ) -> T:
        """Execute tree reduction on partial results."""
        d_delayed, d_compute = self._ensure_dask()

        while len(partial_results) > 1:
            new_level = []
            for i in range(0, len(partial_results), 2):
                if i + 1 < len(partial_results):

                    @d_delayed
                    def _merge(a, b):
                        return merge_pair_function((a, b), func)

                    new_level.append(_merge(partial_results[i], partial_results[i + 1]))
                else:
                    new_level.append(partial_results[i])
            partial_results = new_level

        result = d_compute(partial_results[0], scheduler=self._scheduler)
        return result[0] if isinstance(result, tuple) else result

    def _create_distinct_tasks(self, chunks: List[Sequence[T]]) -> List[Any]:
        """Create distinct tasks for each chunk."""
        d_delayed, _ = self._ensure_dask()

        @d_delayed
        def _distinct_chunk(xs):
            return chunk_distinct_function(xs)

        return [_distinct_chunk(chunk) for chunk in chunks]

    def _execute_distinct_tasks(self, tasks: List[Any]) -> List[List[T]]:
        """Execute distinct tasks and return results."""
        _, d_compute = self._ensure_dask()
        (chunk_results,) = d_compute(tasks, scheduler=self._scheduler)
        return chunk_results

    def _create_sort_tasks(
        self,
        chunks: List[Sequence[T]],
        key: Optional[Callable[[T], Any]],
        reverse: bool,
    ) -> List[Any]:
        """Create sort tasks for each chunk."""
        d_delayed, _ = self._ensure_dask()

        @d_delayed
        def _sort_chunk(xs):
            return chunk_sort_function(xs, key, reverse)

        return [_sort_chunk(chunk) for chunk in chunks]

    def _execute_sort_tasks(self, tasks: List[Any]) -> List[List[T]]:
        """Execute sort tasks and return results."""
        _, d_compute = self._ensure_dask()
        (sorted_chunks,) = d_compute(tasks, scheduler=self._scheduler)
        return sorted_chunks
