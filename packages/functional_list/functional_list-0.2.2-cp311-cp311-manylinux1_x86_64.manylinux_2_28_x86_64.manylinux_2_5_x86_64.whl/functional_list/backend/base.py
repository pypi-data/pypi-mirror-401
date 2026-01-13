"""Backend base definitions.

This file defines the backend interface used by ListMapper.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class BackendError(RuntimeError):
    """Raised when a backend is misconfigured or missing optional deps."""


class BaseBackend:
    """Abstract base for all backends.

    Backends define how to execute map/filter/foreach/reduce operations.
    """

    name = "base"

    def map(self, data: Sequence[T], func: Callable[[T], U]) -> List[U]:
        """Apply a function to each element.

        The default implementation uses a list comprehension.
        """
        return [func(x) for x in data]

    def filter(self, data: Sequence[T], pred: Callable[[T], bool]) -> List[T]:
        """Keep only elements where pred(x) is True."""
        return [x for x in data if pred(x)]

    def foreach(self, data: Sequence[T], func: Callable[[T], Any]) -> None:
        """Execute a side-effecting function for each element."""
        for x in data:
            func(x)

    def reduce(self, data: Sequence[T], func: Callable[[T, T], T]) -> T:
        """Reduce a sequence to a single value.

        The reduction follows the semantics: acc = func(current, acc).
        """
        if not data:
            raise ValueError("Cannot reduce an empty ListMapper")
        acc = data[0]
        for i in range(1, len(data)):
            acc = func(data[i], acc)
        return acc

    def distinct(self, data: Sequence[T]) -> List[T]:
        """Return unique elements preserving first occurrence order.

        Default implementation uses dict.fromkeys() for order preservation.
        Backends can override for optimized implementations.
        """
        return list(dict.fromkeys(data))

    def sort(
        self,
        data: Sequence[T],
        key: Optional[Callable[[T], Any]] = None,
        reverse: bool = False,
    ) -> List[T]:
        """Sort elements using a key function.

        Parameters
        ----------
        data : Sequence[T]
            Input sequence to sort
        key : Optional[Callable[[T], Any]]
            Optional key function for sorting. If None, uses natural ordering.
        reverse : bool
            If True, sort in descending order

        Returns
        -------
        List[T]
            Sorted list
        """
        return sorted(data, key=key, reverse=reverse)  # type: ignore
