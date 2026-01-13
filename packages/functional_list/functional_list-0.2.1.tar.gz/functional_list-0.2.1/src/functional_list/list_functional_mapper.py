"""This module provides the eager `ListMapper` container.

`ListMapper` behaves like a Python list but supports functional-style
operations such as `map`, `filter`, `flat_map`, and `reduce`, with optional
execution backends.
"""

import sys
from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, TypeVar

from functional_list.backend import BaseBackend
from functional_list.backend.serial import SerialBackend
from functional_list.lazy import LazyListMapper
from functional_list.mixins import ListMapperIOMixin
from functional_list.ops import ListMapperEdit
from functional_list.utils.tools_for_main_class import ListMapperIterator

sys.setrecursionlimit(150000)

T = TypeVar("T")


class ListMapper(ListMapperIOMixin, Generic[T]):
    """
    This class object aim to emulate the same behavior of a list object
    but the difference is that we will use it to make a functional
    programming.
    """

    ma_list: List[T]

    # Default backend (class-level) for all ListMapper operations
    _default_backend: BaseBackend = SerialBackend()

    @classmethod
    def set_default_backend(cls, backend: BaseBackend) -> None:
        """Set the default backend used by ListMapper operations."""
        cls._default_backend = backend

    @classmethod
    def get_default_backend(cls) -> BaseBackend:
        """Get the current default backend."""
        return cls._default_backend

    @classmethod
    def using_backend(cls, backend: BaseBackend):
        """Context manager to temporarily override the default backend.

        Example:
        >>> from functional_list.backend import LocalBackend
        >>> with ListMapper.using_backend(LocalBackend(mode="threads")):
        ...     out = ListMapper(1,2,3).map(lambda x: x*x)
        """

        class _BackendContext:
            def __init__(self, b: BaseBackend):
                self._backend = b
                self._prev: Optional[BaseBackend] = None

            def __enter__(self):
                self._prev = cls._default_backend
                cls._default_backend = self._backend
                return self._backend

            def __exit__(self, exc_type, exc, tb):
                if self._prev is not None:
                    cls._default_backend = self._prev
                return False

        return _BackendContext(backend)

    def _backend_or_default(self, backend: Optional[BaseBackend]) -> BaseBackend:
        """Return the provided backend or the current default backend."""
        return backend if backend is not None else type(self).get_default_backend()

    def __init__(self, *args: T):
        self.ma_list = list(args)

    def __str__(self):
        return f"List{self.ma_list}"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return ListMapperIterator(self)

    def __setitem__(self, idx, data):
        self.ma_list[idx] = data

    def __getitem__(self, idx):
        return self.ma_list[idx]

    def copy(self) -> "ListMapper":
        """
        Copy a ListMapper
        :return: an object of ListMapper type
        """
        return ListMapper(*self.ma_list)

    def to_list(self) -> Optional[List[T]]:
        """
        :return a list
        Example:
        >> ListMapper(1,2).tolist()
        >> [1,2]
        """
        # Return a shallow copy to avoid external accidental mutations of internal list
        return self.ma_list[:]

    @property
    def length(self) -> int:
        """
        return length of ListMapper object.
        """
        return len(self.ma_list)

    def map(
        self,
        function: Callable[[T], Any],
        *,
        backend: Optional[BaseBackend] = None,
    ) -> "ListMapper":
        """
        :function a function as params
        :return ListMapper
        Example:
        >> test=ListMapper(2,3,4)
        >> test.map(lambda x:x*x)
        >> List[4, 9, 16]
        """
        b = self._backend_or_default(backend)
        return ListMapper(*b.map(self.ma_list, function))

    @property
    def flatten(self) -> "ListMapper":
        """
        :return ListMapper
        Example:
        >> test = ListMapper([1,2,4], ListMapper(3,5,6))
        >> test.flatten()
        >> List[1, 2, 4, 3, 5, 6]
        """
        # Iterative flatten without sorting to improve performance and keep responsibility of ordering to other methods
        flattened: List[Any] = []
        for data in self.ma_list:
            if isinstance(data, ListMapper):
                flattened.extend(data.ma_list)
            elif isinstance(data, Iterable) and not isinstance(data, (str, bytes)):
                flattened.extend(list(data))
            else:
                flattened.append(data)
        return ListMapper(*flattened)

    def flat_map(
        self,
        function: Callable[[T], Iterable[Any]],
        *,
        backend: Optional[BaseBackend] = None,
    ) -> "ListMapper":
        """
        :param function: function
        :return: ListMapper
        Example:
        >> test = ListMapper("where are you?","I am here")
        >> test.flat_map(lambda x: x.split(" ")
        >> List["where","are","you","I","am","here"]
        """
        b = self._backend_or_default(backend)
        mapped = b.map(self.ma_list, function)
        return ListMapper(*ListMapper(*mapped).flatten.ma_list)

    def reduce(
        self, function: Callable[[T, T], T], *, backend: Optional[BaseBackend] = None
    ) -> Any:
        """
        :param function:
        :return: Any
        Example:
        >> test=ListMapper(1,2,3,4)
        >> test.reduce(lambda x,y:x+y)
        >> 10
        """
        b = self._backend_or_default(backend)
        return b.reduce(self.ma_list, function)

    def order_by_key(self) -> "ListMapper[T]":
        """
        :return: ListMapper
        Example:
        >> test = ListMapper(("I", 1), ("a", 6), ("am", 5), ("here", 4))
        >> test.reduce_by_key()
        >> List[('I', 1), ('a', 6), ('am', 5), ('here', 4)]
        """
        # Use built-in sorted for performance and stability
        sorted_list: List[T] = sorted(self.ma_list)  # type: ignore[type-var]
        return ListMapper(*sorted_list)

    def group_by_key(self) -> "ListMapper":
        """
        :return: ListMapper
        Example:
        >> test= ListMapper(("I",2),("am",1),("here",1),("here",4),("am",1),("I",1))
        >> test.group_by_key()
        >> List[("I",List[2,1]),("am",List[1, 1]),("here",List[4,1]))
        """
        # Efficient grouping using dictionary accumulation
        groups: Dict[Any, List[Any]] = {}
        for item in self.ma_list:
            # Type narrowing: assume items are tuples with at least 2 elements
            key: Any
            value: Any
            key, value = item  # type: ignore[misc]
            groups.setdefault(key, []).append(value)
        result_pairs = [(k, ListMapper(*v)) for k, v in groups.items()]
        return ListMapper(*result_pairs)

    def reduce_by_key(self, function: Callable[[Any, Any], Any]) -> "ListMapper":
        """
        :param function:
        :return: ListMapper
        Example:
        >> test= ListMapper(("I",2),("am",1),("here",1),("here",4),("am",1),("I",1))
        >> test.reduce_by_key(lambda x,y:x+y)
        >> List[("I",3),("am",2),("here",5)]
        """
        grouped = self.group_by_key()
        return grouped.map(lambda x: (x[0], x[1].reduce(function)))

    def foreach(
        self,
        function: Callable[[T], Any],
        *,
        backend: Optional[BaseBackend] = None,
    ) -> None:
        """
        Apply a function to each element.

        Backend notes:
        - serial: executes in current process
        - threads/processes: executes in executor (function must be pickleable for processes)
        - ray/dask: executes remotely
        """
        b = self._backend_or_default(backend)
        b.foreach(self.ma_list, function)

    @property
    def unique(self) -> "ListMapper":
        """
        :return: ListMapper
        Example:
        >> test = ListMapper(1,2,3,3,2,1)
        >> test.unique
        >> List[1, 2, 3]
        """
        # Preserve order of first occurrence
        seen_ordered = list(dict.fromkeys(self.ma_list))
        return ListMapper(*seen_ordered)

    def filter(
        self,
        function: Callable[[T], Any],
        *,
        backend: Optional[BaseBackend] = None,
    ) -> "ListMapper":
        """
        :param function:
        :return: ListMapper
        Example:
        >> test=ListMapper(1,2,3,4,5,6)
        >> test.filter(lambda x: x%2==0)
        >> List[2, 4, 6]
        """
        b = self._backend_or_default(backend)
        return ListMapper(*b.filter(self.ma_list, function))

    @property
    def head(self) -> T:
        """
        :return Any
        Example:
        >> test=ListMapper(10,30,42,89)
        >> test.head
        >> 10
        """
        return self.ma_list[0]

    @property
    def tail(self) -> T:
        """
        :return Any
        Example:
        >> test=ListMapper(10,30,42,89)
        >> test.head
        >> 89
        """
        return self.ma_list[-1]

    def lazy(self) -> "LazyListMapper[T]":
        """Return a lazy view of this ListMapper."""
        return LazyListMapper(self.ma_list)

    @property
    def edit(self) -> ListMapperEdit[T]:
        """Editing namespace for in-place list-like operations.

        Example:
            lm.edit.append(1).edit.remove_index(0)
        """
        return ListMapperEdit(self)
