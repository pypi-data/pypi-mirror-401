"""Local backend accelerators (optional).

This module provides small helper functions that can be implemented in Cython
for speed. The LocalBackend uses these helpers in *serial* mode to avoid
overheads from executors for small/medium workloads.

Design
------
- If the Cython extension is built/available, we import it.
- Otherwise we fall back to pure Python implementations.

Notes
-----
These helpers **do not** accelerate arbitrary Python callables (the callback
still runs in Python). The main benefit is reduced dispatch overhead by doing
chunking/filtering in optimized code paths and by enabling future fast-paths.
"""

from __future__ import annotations

from typing import Callable, List, Sequence, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def _py_chunked_map(
    data: Sequence[T], func: Callable[[T], U], chunk_size: int
) -> List[U]:
    """Map with manual chunking (pure Python fallback)."""
    if chunk_size <= 0:
        chunk_size = 1
    out: List[U] = []
    # Local bindings for speed
    append = out.append
    for i in range(0, len(data), chunk_size):
        for x in data[i : (i + chunk_size)]:  # noqa: E203
            append(func(x))
    return out


def _py_chunked_predicate(
    data: Sequence[T], pred: Callable[[T], bool], chunk_size: int
) -> List[bool]:
    """Compute predicate flags with manual chunking (pure Python fallback)."""
    if chunk_size <= 0:
        chunk_size = 1
    flags: List[bool] = []
    append = flags.append
    for i in range(0, len(data), chunk_size):
        dt_to_iterate = data[i : (i + chunk_size)]  # noqa: E203
        for x in dt_to_iterate:
            append(bool(pred(x)))
    return flags


def _py_filter_by_flags(data: Sequence[T], flags: Sequence[bool]) -> List[T]:
    """Filter items by a boolean mask (pure Python fallback)."""
    out: List[T] = []
    append = out.append
    for x, keep in zip(data, flags):
        if keep:
            append(x)
    return out


# Try to use the Cython extension if present.
try:  # pragma: no cover
    # pylint: disable=import-error,no-name-in-module
    from functional_list.accelerators._local_accel import (  # type: ignore[import-untyped]
        chunked_map,
        chunked_predicate,
        filter_by_flags,
    )

except ImportError:  # pragma: no cover
    chunked_map = _py_chunked_map
    chunked_predicate = _py_chunked_predicate
    filter_by_flags = _py_filter_by_flags

__all__ = [
    "chunked_map",
    "chunked_predicate",
    "filter_by_flags",
]
