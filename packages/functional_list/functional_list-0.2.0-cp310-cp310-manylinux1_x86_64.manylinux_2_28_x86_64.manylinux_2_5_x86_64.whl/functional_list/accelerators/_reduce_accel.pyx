# cython: language_level=3
"""Cython numeric reductions.

This module implements numeric reductions on Python sequences by coercing each
value to ``double``.

Supported operations
-------------------
code:
- 0: add
- 1: mul
- 2: min
- 3: max

Notes
-----
- We still read Python objects from the sequence, so this is not zero-overhead.
- The main benefit is reducing Python-level loop overhead.
"""


def reduce_double(object data, int op_code):
    cdef Py_ssize_t n = len(data)
    if n == 0:
        raise ValueError("Cannot reduce an empty ListMapper")

    cdef double acc
    cdef double v
    cdef Py_ssize_t i

    acc = float(data[0])

    if op_code == 0:  # add
        for i in range(1, n):
            acc += float(data[i])
        return acc

    if op_code == 1:  # mul
        for i in range(1, n):
            acc *= float(data[i])
        return acc

    if op_code == 2:  # min
        for i in range(1, n):
            v = float(data[i])
            if v < acc:
                acc = v
        return acc

    if op_code == 3:  # max
        for i in range(1, n):
            v = float(data[i])
            if v > acc:
                acc = v
        return acc

    raise ValueError(f"Unknown op_code: {op_code}")

