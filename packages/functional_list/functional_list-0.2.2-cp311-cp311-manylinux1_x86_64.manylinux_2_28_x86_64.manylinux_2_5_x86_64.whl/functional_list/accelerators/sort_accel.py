"""Sort accelerators (optional Cython acceleration).

This module provides sorting operations with optional Cython acceleration.
If the Cython extension is available, it will be used; otherwise, we fall back
to pure Python implementations.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")

# Try to import Cython-accelerated version
try:
    from functional_list.accelerators._sort_accel import (
        fast_sort as _cy_fast_sort,  # type: ignore[import]
    )
    from functional_list.accelerators._sort_accel import (
        fast_sort_dicts_by_key as _cy_fast_sort_dicts_by_key,
    )
    from functional_list.accelerators._sort_accel import (
        fast_sort_tuples_by_index as _cy_fast_sort_tuples_by_index,
    )

    _HAS_CYTHON = True
except ImportError:
    _HAS_CYTHON = False


def _py_fast_sort(
    data: Sequence[T], key_func: Optional[Callable[[T], Any]], reverse: bool
) -> List[T]:
    """Pure Python fallback for fast_sort."""
    return sorted(data, key=key_func, reverse=reverse)  # type: ignore


def _py_fast_sort_tuples_by_index(
    data: Sequence[tuple], index: int, reverse: bool
) -> List[tuple]:
    """Pure Python fallback for sorting tuples by index."""
    return sorted(data, key=lambda x: x[index], reverse=reverse)


def _py_fast_sort_dicts_by_key(
    data: Sequence[dict], dict_key: str, reverse: bool
) -> List[dict]:
    """Pure Python fallback for sorting dicts by key."""
    return sorted(data, key=lambda x: x[dict_key], reverse=reverse)


def fast_sort(
    data: Sequence[T],
    key_func: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> List[T]:
    """Sort data with optional key function.

    Uses Cython acceleration if available, otherwise falls back to pure Python.

    Parameters
    ----------
    data : Sequence[T]
        Data to sort
    key_func : Optional[Callable[[T], Any]]
        Optional key function for sorting
    reverse : bool
        If True, sort in descending order

    Returns
    -------
    List[T]
        Sorted list
    """
    if _HAS_CYTHON:
        return _cy_fast_sort(data, key_func, reverse)  # type: ignore
    return _py_fast_sort(data, key_func, reverse)


def fast_sort_tuples_by_index(
    data: Sequence[tuple], index: int = 0, reverse: bool = False
) -> List[tuple]:
    """Sort tuples by a specific index.

    This is optimized for sorting lists of tuples, common in key-value operations.

    Parameters
    ----------
    data : Sequence[tuple]
        List of tuples to sort
    index : int
        Index within tuple to sort by (default: 0)
    reverse : bool
        If True, sort in descending order

    Returns
    -------
    List[tuple]
        Sorted list of tuples
    """
    if _HAS_CYTHON:
        return _cy_fast_sort_tuples_by_index(data, index, reverse)  # type: ignore
    return _py_fast_sort_tuples_by_index(data, index, reverse)


def fast_sort_dicts_by_key(
    data: Sequence[dict], dict_key: str, reverse: bool = False
) -> List[dict]:
    """Sort dictionaries by a specific key.

    This is optimized for sorting lists of dicts, common in data processing.

    Parameters
    ----------
    data : Sequence[dict]
        List of dictionaries to sort
    dict_key : str
        Dictionary key to sort by
    reverse : bool
        If True, sort in descending order

    Returns
    -------
    List[dict]
        Sorted list of dictionaries
    """
    if _HAS_CYTHON:
        return _cy_fast_sort_dicts_by_key(data, dict_key, reverse)  # type: ignore
    return _py_fast_sort_dicts_by_key(data, dict_key, reverse)
