"""Optional accelerated reductions.

Goal
----
Provide a small set of *fast paths* for reductions that are common and can be
implemented efficiently in Cython.

Important limitation
--------------------
A completely generic reduction cannot be meaningfully accelerated because it
must call a Python function for every element.

So this module focuses on identifying a few well-known reductions and routing
those to optimized implementations:
- sum
- product
- min
- max

If we can't confidently identify the operation (or the input isn't numeric), we
return ``None`` and callers should fall back to regular Python reduction.
"""

from __future__ import annotations

import dis
from typing import Callable, Optional, Sequence, TypeVar, cast

# This module uses conservative early returns to keep correctness.
# pylint: disable=too-many-return-statements,consider-using-min-builtin,consider-using-max-builtin

T = TypeVar("T")


def _looks_like_lambda(func: object) -> bool:
    """Return True if `func` looks like a lambda."""
    try:
        return getattr(func, "__name__", "") == "<lambda>"
    except AttributeError:
        return False


def _identify_numeric_reduce_op(
    func: Callable[[object, object], object]
) -> Optional[str]:
    """Identify common numeric reduce ops.

    Returns
    -------
    str | None
        One of "add", "mul", "min", "max" or None if unknown.

    Notes
    -----
    We keep this intentionally conservative to avoid changing semantics.
    """
    # For lambdas like: lambda x, y: x + y
    if _looks_like_lambda(func):
        # On Python 3.12, addition/mul often appear as BINARY_OP with argrepr "+" / "*".
        for inst in dis.get_instructions(func):
            if inst.opname == "BINARY_OP":
                sym = inst.argrepr.strip()
                if sym == "+":
                    return "add"
                if sym == "*":
                    return "mul"

    # Support common named callables
    name = getattr(func, "__name__", None)
    if name in {"add", "sum"}:
        return "add"
    if name in {"mul", "product"}:
        return "mul"
    if name == "min":
        return "min"
    if name == "max":
        return "max"

    return None


def _py_fast_reduce_numeric(data: Sequence[float], op: str) -> float:
    """Pure-Python fast reduction for numeric sequences."""
    if not data:
        raise ValueError("Cannot reduce an empty ListMapper")

    if op == "add":
        s = 0.0
        for x in data:
            s += float(x)
        return s

    if op == "mul":
        p = 1.0
        for x in data:
            p *= float(x)
        return p

    if op == "min":
        m = float(data[0])
        for x in data[1:]:
            fx = float(x)
            if fx < m:
                m = fx
        return m

    if op == "max":
        m = float(data[0])
        for x in data[1:]:
            fx = float(x)
            if fx > m:
                m = fx
        return m

    raise ValueError(f"Unknown op: {op}")


# Import optional extension at module load to avoid pylint import-outside-toplevel.
try:  # pragma: no cover
    # pylint: disable=import-error,no-name-in-module
    from functional_list.accelerators._reduce_accel import (  # type: ignore[import-untyped]
        reduce_double,
    )

    def _cy_reduce_double(data: Sequence[float], op: str) -> float:
        code = {"add": 0, "mul": 1, "min": 2, "max": 3}[op]
        return reduce_double(data, code)

except ImportError:  # pragma: no cover

    def _cy_reduce_double(data: Sequence[float], op: str) -> float:
        return _py_fast_reduce_numeric(data, op)


def fast_reduce_numeric(data: Sequence[T], func: Callable[[T, T], T]) -> Optional[T]:
    """Try to reduce using a fast numeric path.

    Parameters
    ----------
    data:
        Input sequence.
    func:
        Reduction function.

    Returns
    -------
    T | None
        If we can apply a supported numeric fast path, returns the reduced
        result. Otherwise returns ``None``.

    Safety
    ------
    We only attempt this if:
    - the operation can be identified as add/mul/min/max, AND
    - the data looks numeric (int/float/bool), AND
    - the callable behaves like the identified operation on a small probe set.

    Anything else returns None to preserve semantics.
    """
    op = _identify_numeric_reduce_op(cast(Callable[[object, object], object], func))
    if op is None:
        return None

    if not data:
        raise ValueError("Cannot reduce an empty ListMapper")

    # Very conservative numeric check.
    first = data[0]
    if not isinstance(first, (int, float, bool)):
        return None

    # Probe the function on small integers to avoid false positives from
    # heuristic detection (e.g. lambdas like `(x + y) * 2`).
    try:
        probe = cast(Callable[[int, int], object], func)
        if op == "add" and probe(2, 1) != 3:
            return None
        if op == "mul" and probe(2, 3) != 6:
            return None
        # min/max are harder to guess safely; we don't accelerate them unless
        # the function is literally the builtins.
        if op in {"min", "max"} and getattr(func, "__name__", "") not in {"min", "max"}:
            return None
    except (TypeError, ValueError):
        return None

    # Reduce as float; cast back when reasonable.
    result_f = _cy_reduce_double(cast(Sequence[float], data), op)

    # If all inputs are ints/bools and op is add/mul/min/max, casting back to int
    # is safe *for these operations*.
    if all(isinstance(x, (int, bool)) for x in data):
        return cast(T, int(result_f))

    return cast(T, float(result_f))
