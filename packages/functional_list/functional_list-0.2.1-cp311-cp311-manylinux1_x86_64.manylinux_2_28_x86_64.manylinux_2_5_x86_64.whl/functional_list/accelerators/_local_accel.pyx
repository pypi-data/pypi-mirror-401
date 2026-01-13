# cython: language_level=3
"""Cython implementation for LocalBackend helper operations.

This module is optional. Builds only when the project is configured to compile
extensions. The code is intentionally conservative and does not assume numeric
inputs.

Important
---------
We still call back into Python for `func`/`pred`, so speed-ups are modest unless
combined with fast-paths for builtin operations in the future.
"""

from cpython.list cimport PyList_Append


def chunked_map(object data, object func, int chunk_size):
    """Map `func` over `data` using chunked loops."""
    cdef Py_ssize_t n = len(data)
    if chunk_size <= 0:
        chunk_size = 1
    cdef list out = []
    cdef Py_ssize_t i
    cdef Py_ssize_t j
    cdef Py_ssize_t end
    for i in range(0, n, chunk_size):
        end = i + chunk_size
        if end > n:
            end = n
        for j in range(i, end):
            PyList_Append(out, func(data[j]))
    return out


def chunked_predicate(object data, object pred, int chunk_size):
    """Compute boolean predicate flags for `data` using chunked loops."""
    cdef Py_ssize_t n = len(data)
    if chunk_size <= 0:
        chunk_size = 1
    cdef list flags = []
    cdef Py_ssize_t i
    cdef Py_ssize_t j
    cdef Py_ssize_t end
    for i in range(0, n, chunk_size):
        end = i + chunk_size
        if end > n:
            end = n
        for j in range(i, end):
            PyList_Append(flags, bool(pred(data[j])))
    return flags


def filter_by_flags(object data, object flags):
    """Filter `data` by a boolean mask."""
    cdef Py_ssize_t n = len(data)
    cdef list out = []
    cdef Py_ssize_t i
    for i in range(n):
        if flags[i]:
            PyList_Append(out, data[i])
    return out

