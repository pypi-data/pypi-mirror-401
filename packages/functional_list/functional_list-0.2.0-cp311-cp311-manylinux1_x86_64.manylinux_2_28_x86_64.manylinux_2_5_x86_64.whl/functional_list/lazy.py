"""functional_list.lazy

Lazy evaluation utilities for the functional_list package.

`ListMapper` is eager (it stores a Python list). For large datasets or when you
want to compose transformations without materializing intermediate lists, you
can use `LazyListMapper`.

Key characteristics
-------------------
- LazyListMapper stores an *iterable* (often a generator).
- Operations like map/filter/flat_map are lazy and return a new LazyListMapper.
- The pipeline is executed only when you materialize via `to_list()` / `collect()`
  or when you iterate over the LazyListMapper.

This is similar to how Spark RDDs or Python's `itertools` pipelines behave.

Limitations
-----------
- A LazyListMapper backed by a generator is generally single-use: once consumed,
  it can't be replayed unless the source iterable is re-iterable.
- Some operations like order_by_key require materialization.

Example
-------
>>> from functional_list import ListMapper
>>>
>>> eager = ListMapper[int](1, 2, 3, 4)
>>> lazy = eager.lazy().map(lambda x: x * x).filter(lambda x: x > 5)
>>> lazy.to_list()
[9, 16]
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)

T = TypeVar("T")
U = TypeVar("U")

if TYPE_CHECKING:
    from functional_list import ListMapper
    from functional_list.backend import BaseBackend

_Op = Union[
    Tuple[str, Callable[[Any], Any]],  # ("map", func)
    Tuple[str, Callable[[Any], bool]],  # ("filter", pred)
    Tuple[str, Callable[[Any], Iterable[Any]]],  # ("flat_map", func)
]


@dataclass(frozen=True)
class LazyListMapper(Generic[T]):
    """A lazy, iterable pipeline of transformations.

    This class supports two execution modes:

    1) Pure Python iteration (always works)
       - Used when you iterate over the object directly.
       - Used when you call `to_list()` / `collect()` without a backend.

    2) Backend materialization (optional)
       - If you call `to_list(backend=...)` / `collect(backend=...)`, the pipeline
         can be executed via the selected backend.
       - This requires the LazyListMapper to have been built using the methods
         on this class (map/filter/flat_map), so it has an internal plan.

    Parameters
    ----------
    iterable:
        The source iterable.

    Notes
    -----
    - If `iterable` is a generator, it will be consumed once.
    - Backend materialization must still *materialize* to a list, so the main
      speed-up comes from parallel/distributed execution of transformations.
    """

    iterable: Iterable[Any]
    _ops: Tuple[_Op, ...] = ()

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the underlying iterable (pure Python execution)."""
        return cast(Iterator[T], self._iter_python())

    def _iter_python(self) -> Iterator[Any]:
        """Iterate by applying the recorded ops in pure Python.

        This is the reference implementation for lazy execution.
        """

        it: Iterable[Any] = self.iterable

        for op in self._ops:
            kind = op[0]
            fn = op[1]

            if kind == "map":

                def _map_gen(
                    src: Iterable[Any], f: Callable[[Any], Any]
                ) -> Iterator[Any]:
                    for x in src:
                        yield f(x)

                it = _map_gen(it, fn)

            elif kind == "filter":

                def _filter_gen(
                    src: Iterable[Any], p: Callable[[Any], bool]
                ) -> Iterator[Any]:
                    for x in src:
                        if p(x):
                            yield x

                it = _filter_gen(it, cast(Callable[[Any], bool], fn))

            elif kind == "flat_map":
                fm = cast(Callable[[Any], Iterable[Any]], fn)

                def _flat_map_gen(
                    src: Iterable[Any], f: Callable[[Any], Iterable[Any]]
                ) -> Iterator[Any]:
                    for x in src:
                        yield from f(x)

                it = _flat_map_gen(it, fm)

            else:  # pragma: no cover
                raise ValueError(f"Unknown lazy op: {kind}")

        return iter(it)

    def map(self, func: Callable[[T], U]) -> "LazyListMapper[U]":
        """Lazily apply `func` to each element."""
        return LazyListMapper(self.iterable, self._ops + (("map", func),))

    def filter(self, pred: Callable[[T], bool]) -> "LazyListMapper[T]":
        """Lazily keep only elements where `pred(x)` is True."""
        return LazyListMapper(self.iterable, self._ops + (("filter", pred),))

    def flat_map(self, func: Callable[[T], Iterable[U]]) -> "LazyListMapper[U]":
        """Lazily apply `func` and flatten one level."""
        return LazyListMapper(self.iterable, self._ops + (("flat_map", func),))

    def foreach(self, func: Callable[[T], Any]) -> None:
        """Execute a side-effecting function for each element (forces evaluation).

        Notes
        -----
        This uses pure Python iteration. If you want backend execution, call
        `collect(backend=...).foreach(...)`.
        """
        for x in self:
            func(x)

    def reduce(self, func: Callable[[T, T], T]) -> T:
        """Reduce the iterable to a single value (forces evaluation).

        Preserves ListMapper semantics: `acc = func(current, acc)`.

        Notes
        -----
        Reduction is performed in pure Python to preserve deterministic order.
        """
        it = iter(self)
        try:
            acc = next(it)
        except StopIteration as e:
            raise ValueError("Cannot reduce an empty LazyListMapper") from e

        for x in it:
            acc = func(x, acc)
        return acc

    def _to_sequence(self) -> Sequence[Any]:
        """Materialize the source iterable to a sequence for backends.

        Prefers returning the iterable itself if it's already a Sequence.
        """
        if isinstance(self.iterable, Sequence):
            return self.iterable
        return list(self.iterable)

    def to_list(self, *, backend: Optional["BaseBackend"] = None) -> List[T]:
        """Materialize the pipeline into a Python list.

        Parameters
        ----------
        backend:
            If provided, execute the recorded pipeline using the backend.
            If omitted, execute using pure Python iteration.

        Returns
        -------
        list
            The materialized elements.
        """
        if backend is None:
            return list(self)

        # Backend path: apply the recorded plan using backend primitives.
        data: List[Any] = list(self._to_sequence())
        for op in self._ops:
            kind = op[0]
            fn = op[1]
            if kind == "map":
                data = list(backend.map(data, fn))
            elif kind == "filter":
                data = list(backend.filter(data, fn))
            elif kind == "flat_map":
                mapped = backend.map(data, fn)
                # Flatten after mapping. This is local flattening of results.
                flat: List[Any] = []
                for part in mapped:
                    flat.extend(list(part))
                data = flat
            else:  # pragma: no cover
                raise ValueError(f"Unknown lazy op: {kind}")

        return cast(List[T], data)

    def collect(self, *, backend: Optional["BaseBackend"] = None) -> "ListMapper[T]":
        """Materialize into an eager ListMapper.

        Parameters
        ----------
        backend:
            Optional backend used to materialize the lazy pipeline before building
            the ListMapper. If not provided, this will use ListMapper's current
            default backend.
        """
        lm_mod = importlib.import_module("functional_list.list_functional_mapper")
        list_mapper_cls = lm_mod.ListMapper

        b = backend if backend is not None else list_mapper_cls.get_default_backend()
        return list_mapper_cls(*self.to_list(backend=b))

    def order_by_key(self) -> "ListMapper[T]":
        """Materialize and sort using eager ListMapper semantics."""
        eager = self.collect()
        return eager.order_by_key()
