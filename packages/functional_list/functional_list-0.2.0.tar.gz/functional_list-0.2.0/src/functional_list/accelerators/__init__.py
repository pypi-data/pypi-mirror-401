"""Optional acceleration utilities.

This package contains optional, performance-oriented implementations (Cython if
available, otherwise pure Python fallbacks).

The public API is intentionally tiny so backends can depend on it without
creating hard build-time requirements.
"""

from __future__ import annotations

from functional_list.accelerators.local_accel import (
    chunked_map,
    chunked_predicate,
    filter_by_flags,
)
from functional_list.accelerators.reduce_accel import fast_reduce_numeric

__all__ = [
    "chunked_map",
    "chunked_predicate",
    "filter_by_flags",
    "fast_reduce_numeric",
]
