"""Backend base definitions.

This file defines the backend interface used by ListMapper.
"""

from __future__ import annotations

from typing import Any, Callable, List, Sequence, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class BackendError(RuntimeError):
    """Raised when a backend is misconfigured or missing optional deps."""


class BaseBackend:
    """Common contract for backends.

    Notes
    -----
    The `func`/`pred` callables are typed as returning `Any` to allow backends
    like AsyncBackend that expect coroutine functions.
    """

    name: str = "base"

    def map(self, data: Sequence[T], func: Callable[[T], Any]) -> List[Any]:
        """Apply `func` to each element and return a list of results."""
        raise NotImplementedError

    def filter(self, data: Sequence[T], pred: Callable[[T], Any]) -> List[T]:
        """Filter elements according to `pred` and return kept elements."""
        raise NotImplementedError

    def foreach(self, data: Sequence[T], func: Callable[[T], Any]) -> None:
        """Apply `func` to each element, discarding results."""
        raise NotImplementedError

    def reduce(self, data: Sequence[T], func: Callable[[T, T], T]) -> T:
        """Fold the sequence into a single value using `func`.

        Preserves ListMapper semantics: `acc = func(current, acc)`.
        """
        if not data:
            raise ValueError("Cannot reduce an empty ListMapper")
        acc = data[0]
        for i in range(1, len(data)):
            acc = func(data[i], acc)
        return acc
