"""Internal chunking helpers for backends.

This module centralizes small utility helpers used by multiple backends.
It is intentionally not part of the public API.
"""

from __future__ import annotations

from typing import List, Sequence, TypeVar

T = TypeVar("T")


def chunked(seq: Sequence[T], chunk_size: int) -> List[Sequence[T]]:
    """Split a sequence into contiguous chunks.

    Parameters
    ----------
    seq:
        Input sequence.
    chunk_size:
        Chunk size. Values <= 0 are treated as 1.

    Returns
    -------
    list
        A list of slices of the original sequence.

    Notes
    -----
    This project runs both `black` and `flake8` with `E203` enabled.
    Black formats slices as ``a[i : j]``, which triggers E203. To keep both
    tools happy, we build slices using the `slice()` builtin.
    """
    if chunk_size <= 0:
        chunk_size = 1
    return [seq[slice(i, i + chunk_size)] for i in range(0, len(seq), chunk_size)]


def flatten(nested: Sequence[Sequence[T]]) -> List[T]:
    """Flatten a sequence of sequences into a single list."""
    out: List[T] = []
    for part in nested:
        out.extend(part)
    return out
