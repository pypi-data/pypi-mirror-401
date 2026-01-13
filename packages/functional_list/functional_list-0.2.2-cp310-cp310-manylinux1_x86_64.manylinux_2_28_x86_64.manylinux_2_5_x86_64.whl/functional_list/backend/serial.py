"""Serial backend (default).

Runs all operations in-process.
"""

from __future__ import annotations

from typing import Any, Callable, List, Sequence, TypeVar

from functional_list.backend.base import BaseBackend

T = TypeVar("T")
U = TypeVar("U")


class SerialBackend(BaseBackend):
    """Serial backend (default).

    Executes all operations in-process and in-order.
    """

    name = "serial"

    def map(self, data: Sequence[T], func: Callable[[T], U]) -> List[U]:
        return [func(x) for x in data]

    def filter(self, data: Sequence[T], pred: Callable[[T], bool]) -> List[T]:
        return [x for x in data if pred(x)]

    def foreach(self, data: Sequence[T], func: Callable[[T], Any]) -> None:
        for x in data:
            func(x)
