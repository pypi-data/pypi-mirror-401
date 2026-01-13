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
    Tuple[str, None],  # ("distinct", None) or ("order_by_key", None)
    Tuple[str, "LazyListMapper[Any]"],  # ("union", other_lazy)
    Tuple[
        str, Tuple[Optional[Callable[[Any], Any]], bool, Optional["BaseBackend"]]
    ],  # ("sort", (key_func, reverse, backend))
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

    def _iter_python(self) -> Iterator[Any]:  # pylint: disable=too-many-locals
        """Iterate by applying the recorded ops in pure Python.

        This is the reference implementation for lazy execution.
        """

        it: Iterable[Any] = self.iterable

        for op in self._ops:
            kind = op[0]
            fn = op[1] if len(op) > 1 else None

            if kind == "map":
                map_fn = cast(Callable[[Any], Any], fn)

                def _map_gen(
                    src: Iterable[Any], f: Callable[[Any], Any]
                ) -> Iterator[Any]:
                    for x in src:
                        yield f(x)

                it = _map_gen(it, map_fn)

            elif kind == "filter":
                filter_fn = cast(Callable[[Any], bool], fn)

                def _filter_gen(
                    src: Iterable[Any], p: Callable[[Any], bool]
                ) -> Iterator[Any]:
                    for x in src:
                        if p(x):
                            yield x

                it = _filter_gen(it, filter_fn)

            elif kind == "flat_map":
                flat_fn = cast(Callable[[Any], Iterable[Any]], fn)

                def _flat_map_gen(
                    src: Iterable[Any], f: Callable[[Any], Iterable[Any]]
                ) -> Iterator[Any]:
                    for x in src:
                        yield from f(x)

                it = _flat_map_gen(it, flat_fn)

            elif kind == "distinct":

                def _distinct_gen(src: Iterable[Any]) -> Iterator[Any]:
                    seen = set()
                    seen_unhashable = []
                    for x in src:
                        # Use hashable check
                        try:
                            if x not in seen:
                                seen.add(x)
                                yield x
                        except TypeError:
                            # Unhashable type, use list-based check (slower)
                            if x not in seen_unhashable:
                                seen_unhashable.append(x)
                                yield x

                it = _distinct_gen(it)

            elif kind == "union":
                # Union operation: chain this iterable with another
                other_lazy = cast("LazyListMapper[Any]", cast(object, fn))

                def _union_gen(
                    src: Iterable[Any], other: "LazyListMapper[Any]"
                ) -> Iterator[Any]:
                    # Yield all from source first
                    yield from src
                    # Then yield all from other
                    yield from other

                it = _union_gen(it, other_lazy)

            elif kind == "sort":
                # Sort operation: must materialize to a list, sort, then iterate
                sort_params = cast(
                    Tuple[Optional[Callable[[Any], Any]], bool, Optional[Any]],
                    cast(object, fn),
                )
                key_func, reverse, _backend = sort_params
                # Note: backend is ignored in pure Python iteration mode

                # Materialize remaining items
                materialized = list(it)
                # Sort them
                materialized.sort(key=key_func, reverse=reverse)
                # Create iterator from sorted list
                it = iter(materialized)

            elif kind == "order_by_key":
                # Natural ordering sort: materialize, sort, iterate
                materialized = list(it)
                materialized.sort()
                it = iter(materialized)

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

    def distinct(self) -> "LazyListMapper[T]":
        """Lazily remove duplicate elements, preserving first occurrence order.

        Returns
        -------
        LazyListMapper
            A new lazy pipeline that will yield only unique elements.

        Example
        -------
        >>> from functional_list import ListMapper
        >>> lazy = ListMapper(1, 2, 2, 3, 1, 4).lazy().distinct()
        >>> lazy.to_list()
        [1, 2, 3, 4]
        """
        return LazyListMapper(self.iterable, self._ops + (("distinct", None),))

    def union(self, other: "LazyListMapper[T]") -> "LazyListMapper[T]":
        """Lazily combine this LazyListMapper with another LazyListMapper.

        Elements from this LazyListMapper will be yielded first, followed by
        elements from the other LazyListMapper. Does not remove duplicates.

        Parameters
        ----------
        other : LazyListMapper[T]
            Another LazyListMapper to union with. Must be a LazyListMapper instance.

        Returns
        -------
        LazyListMapper[T]
            A new lazy pipeline that will yield elements from both iterables.

        Raises
        ------
        TypeError
            If other is not a LazyListMapper instance.

        Notes
        -----
        - The union is lazy and will not execute until materialization
        - Type checking is deferred until materialization (unlike eager union)
        - To remove duplicates, use .union(other).distinct()

        Examples
        --------
        >>> from functional_list import ListMapper
        >>> lazy1 = ListMapper(1, 2, 3).lazy()
        >>> lazy2 = ListMapper(4, 5, 6).lazy()
        >>> result = lazy1.union(lazy2).to_list()
        >>> result
        [1, 2, 3, 4, 5, 6]

        >>> # With transformations
        >>> lazy1 = ListMapper(1, 2, 3).lazy().map(lambda x: x * 2)
        >>> lazy2 = ListMapper(4, 5, 6).lazy().map(lambda x: x * 3)
        >>> result = lazy1.union(lazy2).to_list()
        >>> result
        [2, 4, 6, 12, 15, 18]

        >>> # Remove duplicates after union
        >>> lazy1 = ListMapper(1, 2, 3).lazy()
        >>> lazy2 = ListMapper(3, 4, 5).lazy()
        >>> result = lazy1.union(lazy2).distinct().to_list()
        >>> result
        [1, 2, 3, 4, 5]
        """
        # Type check: ensure other is a LazyListMapper
        if not isinstance(other, LazyListMapper):
            raise TypeError(
                f"union() requires another LazyListMapper, got {type(other).__name__}"
            )

        # Record the union operation
        # Note: Type compatibility is checked at materialization time, not here
        return LazyListMapper(self.iterable, self._ops + (("union", other),))

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

    def to_list(  # pylint: disable=too-many-locals
        self, *, backend: Optional["BaseBackend"] = None
    ) -> List[T]:
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
            fn = op[1] if len(op) > 1 else None
            if kind == "map":
                map_fn = cast(Callable[[Any], Any], fn)
                data = list(backend.map(data, map_fn))
            elif kind == "filter":
                filter_fn = cast(Callable[[Any], Any], fn)
                data = list(backend.filter(data, filter_fn))
            elif kind == "flat_map":
                flat_fn = cast(Callable[[Any], Any], fn)
                mapped = backend.map(data, flat_fn)
                # Flatten after mapping. This is local flattening of results.
                flat: List[Any] = []
                for part in mapped:
                    flat.extend(list(part))
                data = flat
            elif kind == "distinct":
                data = list(backend.distinct(data))
            elif kind == "union":
                # Union with another lazy mapper - materialize it and combine
                other_lazy = cast("LazyListMapper[Any]", cast(object, fn))
                other_data = other_lazy.to_list(backend=backend)
                data = data + other_data
            elif kind == "sort":
                # Sort operation using backend
                sort_params = cast(
                    Tuple[Optional[Callable[[Any], Any]], bool, Optional[Any]],
                    cast(object, fn),
                )
                key_func, reverse, sort_backend = sort_params
                # Use the backend specified in sort(), or fall back to to_list's backend
                backend_to_use = sort_backend if sort_backend is not None else backend
                data = list(backend_to_use.sort(data, key=key_func, reverse=reverse))
            elif kind == "order_by_key":
                # Natural ordering sort using backend
                data = list(backend.sort(data, key=None, reverse=False))
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

    def order_by_key(self) -> "LazyListMapper[T]":
        """Lazily record a sort by natural ordering operation.

        The sort is **not** executed immediately. It's recorded and will be
        applied when the pipeline is materialized.

        Returns
        -------
        LazyListMapper[T]
            A new lazy pipeline with the sort operation recorded

        Notes
        -----
        This is equivalent to calling sort() without a key function.
        The operation is deferred until an action method (to_list, collect, etc.)
        is called.

        Example
        -------
        >>> from functional_list import ListMapper
        >>> lazy = ListMapper(3, 1, 4, 1, 5, 9).lazy()
        >>> sorted_lazy = lazy.order_by_key()  # Operation recorded, not executed
        >>> result = sorted_lazy.map(lambda x: x * 2).to_list()  # Now executes
        [2, 2, 6, 8, 10, 18]
        """
        # Record the operation as ("order_by_key", None)
        return LazyListMapper(self.iterable, self._ops + (("order_by_key", None),))

    def sort(
        self,
        *,
        key: Optional[Callable[[T], Any]] = None,
        reverse: bool = False,
        backend: Optional["BaseBackend"] = None,
    ) -> "LazyListMapper[T]":
        """Lazily record a sort operation.

        The sort is **not** executed immediately. It's recorded and will be
        applied when the pipeline is materialized (via to_list(), collect(), etc.).

        Parameters
        ----------
        key : Optional[Callable[[T], Any]]
            Optional function to extract comparison key from each element
        reverse : bool
            If True, sort in descending order
        backend : Optional[BaseBackend]
            Optional backend for execution (used during materialization)

        Returns
        -------
        LazyListMapper[T]
            A new lazy pipeline with the sort operation recorded

        Notes
        -----
        Unlike map/filter/distinct which can stream, sort requires seeing all
        elements, so it will force materialization during execution, but the
        operation itself is deferred until an action method is called.

        Examples
        --------
        >>> from functional_list import ListMapper
        >>> lazy = ListMapper(3, 1, 4, 1, 5, 9).lazy()
        >>> sorted_lazy = lazy.sort()  # Operation recorded, not executed!
        >>> sorted_lazy.map(lambda x: x * 2)  # Can continue chaining
        >>> result = sorted_lazy.to_list()  # Now executes: sort, then map
        [2, 2, 6, 8, 10, 18]

        >>> # With key function
        >>> lazy = ListMapper(
        ...     {"name": "Alice", "score": 85},
        ...     {"name": "Bob", "score": 92}
        ... ).lazy()
        >>> sorted_lazy = lazy.sort(key=lambda x: x["score"])  # Recorded
        >>> result = sorted_lazy.map(lambda x: x["name"]).to_list()  # Executed
        ['Alice', 'Bob']
        """
        # Store backend in the operation tuple so it can be used during materialization
        return LazyListMapper(
            self.iterable, self._ops + (("sort", (key, reverse, backend)),)
        )
