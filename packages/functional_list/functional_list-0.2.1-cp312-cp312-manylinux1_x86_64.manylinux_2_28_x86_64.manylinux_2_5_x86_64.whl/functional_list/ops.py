"""functional_list.ops

Helper namespaces attached to ListMapper to keep the public surface small.

Motivation
----------
Pylint's `--max-public-methods` is set to 25 for this project. As ListMapper
supports many list-like editing operations and several I/O constructors, we
expose those less-core capabilities via small helper objects:

- `lm.edit.*`  : in-place editing / mutation helpers
- `ListMapper.io.*`: file readers (CSV/JSON/JSONL/Text/Parquet)

This keeps the core functional API (`map`, `filter`, `reduce`, etc.) directly on
ListMapper while meeting the project's linting constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, List, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ListMapperEdit(Generic[T]):
    """In-place editing helpers for a ListMapper instance."""

    _lm: "ListMapper[T]"

    def append(self, value: T) -> "ListMapper[T]":
        """Append an element (in-place) and return the same ListMapper."""
        self._lm.ma_list.append(value)
        return self._lm

    def extend(self, *values: T) -> "ListMapper[T]":
        """Extend with elements (in-place) and return the same ListMapper."""
        self._lm.ma_list.extend(values)
        return self._lm

    def insert(self, index: int, value: T) -> "ListMapper[T]":
        """Insert an element at index (in-place) and return the same ListMapper."""
        self._lm.ma_list.insert(index, value)
        return self._lm

    def remove(self, elem: T) -> "ListMapper[T]":
        """Remove first occurrence of elem (in-place) and return the same ListMapper."""
        self._lm.ma_list.remove(elem)
        return self._lm

    def remove_all(self, value: T) -> "ListMapper[T]":
        """Remove all occurrences of value (in-place) and return the same ListMapper."""
        self._lm.ma_list = [val for val in self._lm.ma_list if val != value]
        return self._lm

    def remove_index(self, index: int) -> "ListMapper[T]":
        """Remove element by index (in-place) and return the same ListMapper."""
        if index < 0 or index >= len(self._lm.ma_list):
            raise IndexError("list index out of range")
        del self._lm.ma_list[index]
        return self._lm

    def remove_list_index(self, indices: List[int]) -> "ListMapper[T]":
        """Remove elements for all provided indices (in-place) and return the same ListMapper."""
        nb_element = len(self._lm.ma_list)
        if any(idx < 0 or idx >= nb_element for idx in indices):
            raise IndexError("list index out of range")
        to_remove = set(indices)
        self._lm.ma_list = [
            x for i, x in enumerate(self._lm.ma_list) if i not in to_remove
        ]
        return self._lm

    def remove_list_value(self, values: List[T]) -> "ListMapper[T]":
        """Remove all elements that appear in `values` (in-place) and return the same ListMapper."""
        to_remove = set(values)
        self._lm.ma_list = [val for val in self._lm.ma_list if val not in to_remove]
        return self._lm


if TYPE_CHECKING:  # pragma: no cover
    from functional_list.list_functional_mapper import ListMapper
