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
from functional_list.backend.base import BackendError, BaseBackend

try:
    from dask import delayed  # type: ignore[import-not-found]
    from dask.base import compute  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    delayed = None  # type: ignore[assignment]
    compute = None  # type: ignore[assignment]

T = TypeVar("T")
U = TypeVar("U")


class DaskBackend(BaseBackend):
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

    def _ensure_dask(self):
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

    def filter(self, data: Sequence[T], pred: Callable[[T], bool]) -> List[T]:
        flags = self.map(data, pred)
        return [x for x, keep in zip(data, flags) if keep]

    def foreach(self, data: Sequence[T], func: Callable[[T], Any]) -> None:
        _ = self.map(data, func)
