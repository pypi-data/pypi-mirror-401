"""Local backend.

Provides:
- serial
- threads (ThreadPoolExecutor)
- processes (ProcessPoolExecutor)

Optionally uses Cython-accelerated helpers (if installed/built) for faster
serial execution.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Sequence, TypeVar

from functional_list.accelerators.local_accel import (
    chunked_map,
    chunked_predicate,
    filter_by_flags,
)
from functional_list.accelerators.reduce_accel import fast_reduce_numeric
from functional_list.backend.base import BackendError, BaseBackend

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True)
class LocalBackend(BaseBackend):
    """Local backend.

    Parameters
    ----------
    mode:
        Execution mode.

        - ``"serial"``: in-process execution
        - ``"threads"``: ThreadPoolExecutor
        - ``"processes"``: ProcessPoolExecutor

    workers:
        Number of worker threads/processes. If None, uses executor default.

    chunk_size:
        Only used for ``mode="serial"``.

        Controls how many items are processed per inner loop chunk by the
        (optional) accelerator helpers. Larger values usually reduce overhead.

    Notes
    -----
    - For ``mode="processes"``, `func` must be pickleable.
    - This backend does not automatically vectorize user functions; for
      columnar data prefer PyArrow compute where possible.
    """

    mode: str = "serial"
    workers: Optional[int] = None
    chunk_size: int = 2048

    @property
    def name(self) -> str:  # type: ignore[override]
        """A human-readable backend name (e.g. ``local[threads]``)."""
        return f"local[{self.mode}]"

    def map(self, data: Sequence[T], func: Callable[[T], U]) -> List[U]:
        """Apply a function to each element using the selected local execution mode."""
        if self.mode == "serial":
            # Use optional accelerator (Cython if available, else Python fallback).
            return chunked_map(data, func, self.chunk_size)

        if self.mode == "threads":
            with ThreadPoolExecutor(max_workers=self.workers) as ex:
                return list(ex.map(func, data))

        if self.mode == "processes":
            with ProcessPoolExecutor(max_workers=self.workers) as ex:
                return list(ex.map(func, data))

        raise BackendError(f"Unknown LocalBackend mode: {self.mode}")

    def filter(self, data: Sequence[T], pred: Callable[[T], bool]) -> List[T]:
        """Filter elements according to `pred` using the selected mode."""
        if self.mode == "serial":
            flags = chunked_predicate(data, pred, self.chunk_size)
            return filter_by_flags(data, flags)

        flags = self.map(data, pred)
        return [x for x, keep in zip(data, flags) if keep]

    def foreach(self, data: Sequence[T], func: Callable[[T], Any]) -> None:
        """Apply a side-effecting function to each element."""
        if self.mode == "serial":
            for x in data:
                func(x)
            return

        _ = self.map(data, func)

    def reduce(self, data: Sequence[T], func: Callable[[T, T], T]) -> T:  # type: ignore[override]
        """Reduce a sequence to a single value.

        This method keeps the same semantics as :meth:`BaseBackend.reduce`.

        Optimization
        ------------
        In ``mode="serial"`` we try an optional Cython fast path for a small set
        of common numeric reductions (sum/product/min/max). If we can't identify
        the operation or the types don't match, we fall back to the base Python
        implementation.
        """
        if not data:
            raise ValueError("Cannot reduce an empty ListMapper")

        # Only serial mode tries fast paths. Executor modes keep the base behavior.
        if self.mode != "serial":
            return super().reduce(data, func)

        fast = fast_reduce_numeric(data, func)
        if fast is not None:
            return fast

        return super().reduce(data, func)
