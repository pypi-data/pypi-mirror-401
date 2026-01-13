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

from typing import Any, Callable, List, Optional, Sequence, TypeVar

from functional_list.backend._chunking import chunked, flatten
from functional_list.backend.base import BackendError, BaseBackend

try:
    import ray  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    ray = None  # type: ignore[assignment]

T = TypeVar("T")
U = TypeVar("U")


class RayBackend(BaseBackend):
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

    def filter(self, data: Sequence[T], pred: Callable[[T], bool]) -> List[T]:
        """Filter elements using a predicate executed on Ray.

        This is implemented as a distributed predicate evaluation followed by
        a local selection step.

        Parameters
        ----------
        data:
            Input sequence.
        pred:
            Predicate function returning True for elements to keep.

        Returns
        -------
        list
            The filtered elements (stable order).
        """

        flags = self.map(data, pred)
        return [x for x, keep in zip(data, flags) if keep]

    def foreach(self, data: Sequence[T], func: Callable[[T], Any]) -> None:
        """Execute a side-effecting function on each element using Ray."""
        _ = self.map(data, func)
