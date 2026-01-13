"""Shared utilities for distributed backends (Ray and Dask).

This module contains common helper functions to reduce code duplication
between Ray and Dask backend implementations.
"""

from __future__ import annotations

import heapq
from abc import ABC, abstractmethod
from typing import Any, Callable, List, Sequence, TypeVar

from functional_list.backend._chunking import chunked

T = TypeVar("T")
U = TypeVar("U")


def chunk_reduce_function(chunk: Sequence[T], func: Callable[[T, T], T]) -> Any:
    """Reduce a single chunk of data.

    This is a pure function that can be distributed to Ray/Dask workers.

    Parameters
    ----------
    chunk : Sequence[T]
        Chunk of data to reduce
    func : Callable[[T, T], T]
        Reduction function

    Returns
    -------
    Any
        Reduced value or None if chunk is empty
    """
    if not chunk:
        return None
    acc = chunk[0]
    for x in chunk[1:]:
        acc = func(x, acc)
    return acc


def chunk_distinct_function(chunk: Sequence[T]) -> List[T]:
    """Get unique elements from a chunk.

    This is a pure function that can be distributed to Ray/Dask workers.

    Parameters
    ----------
    chunk : Sequence[T]
        Chunk of data to deduplicate

    Returns
    -------
    List[T]
        List of unique elements from chunk
    """
    return list(dict.fromkeys(chunk))


def chunk_sort_function(
    chunk: Sequence[T],
    key: Any = None,
    reverse: bool = False,
) -> List[T]:
    """Sort a single chunk of data.

    This is a pure function that can be distributed to Ray/Dask workers.

    Parameters
    ----------
    chunk : Sequence[T]
        Chunk of data to sort
    key : Any, optional
        Key function for sorting
    reverse : bool
        If True, sort in descending order

    Returns
    -------
    List[T]
        Sorted chunk
    """
    return sorted(chunk, key=key, reverse=reverse)


def merge_pair_function(pair: tuple, func: Callable[[T, T], T]) -> T:
    """Merge a pair of reduced results.

    This is a pure function that can be distributed to Ray/Dask workers
    for tree reduction.

    Parameters
    ----------
    pair : tuple
        Tuple of 1 or 2 values to merge
    func : Callable[[T, T], T]
        Reduction function

    Returns
    -------
    T
        Merged result
    """
    return pair[0] if len(pair) == 1 else func(pair[1], pair[0])


def calculate_chunk_size(data_len: int, default_chunk_size: int | None) -> int:
    """Calculate appropriate chunk size for distributed processing.

    Parameters
    ----------
    data_len : int
        Length of data to process
    default_chunk_size : int | None
        User-specified chunk size, or None for auto

    Returns
    -------
    int
        Chunk size to use
    """
    if default_chunk_size is not None:
        return default_chunk_size
    return max(1, data_len // 100)


# Thresholds for when to use optimized implementations
REDUCE_THRESHOLD = 100
DISTINCT_THRESHOLD = 1000
SORT_THRESHOLD = 1000


class DistributedBackendMixin(ABC):
    """Mixin class providing common implementations for distributed backends.

    This mixin extracts common logic from Ray and Dask backends to reduce
    code duplication. Subclasses must implement:
    - map() method
    - _get_chunk_size() method
    - _create_reduce_tasks() method
    - _execute_reduce_tree() method
    - _create_distinct_tasks() method
    - _execute_distinct_tasks() method
    - _create_sort_tasks() method
    - _execute_sort_tasks() method
    """

    _chunk_size: int | None

    @abstractmethod
    def _execute_reduce_tree(
        self, partial_results: List[T], func: Callable[[T, T], T]
    ) -> T:
        """Execute tree reduction on partial results."""
        raise NotImplementedError("To be implemented by subclass")

    def filter(self, data: Sequence[T], pred: Callable[[T], bool]) -> List[T]:
        """Filter elements using a predicate.

        This is implemented as a distributed predicate evaluation followed by
        a local selection step.

        Parameters
        ----------
        data:
            Input sequence.
        pred:
            Predicate function returning True for elements to keep.

        Returns
        -------
        list
            The filtered elements (stable order).
        """
        flags = self.map(data, pred)  # type: ignore[attr-defined]
        return [x for x, keep in zip(data, flags) if keep]

    def foreach(self, data: Sequence[T], func: Callable[[T], Any]) -> None:
        """Execute a side-effecting function on each element."""
        _ = self.map(data, func)  # type: ignore[attr-defined]

    def reduce(self, data: Sequence[T], func: Callable[[T, T], T]) -> T:
        """Reduce using distributed tree reduction.

        For large datasets, this uses a distributed tree reduction pattern
        to minimize sequential bottlenecks.

        Parameters
        ----------
        data:
            Input sequence.
        func:
            Reduction function with signature (current, accumulator) -> accumulator.

        Returns
        -------
        T
            The reduced value.
        """
        if not data:
            raise ValueError("Cannot reduce an empty ListMapper")

        # For small datasets, use base implementation
        if len(data) < REDUCE_THRESHOLD:
            return super().reduce(data, func)  # type: ignore[misc]

        # For large datasets, use distributed tree reduction
        chunk_size = calculate_chunk_size(len(data), self._chunk_size)
        chunks = list(chunked(data, chunk_size))

        # First level: reduce each chunk
        partial_results = self._create_reduce_tasks(chunks, func)  # type: ignore[attr-defined]

        return self._execute_reduce_tree(partial_results, func)

    def distinct(self, data: Sequence[T]) -> List[T]:
        """Remove duplicates using distributed processing.

        For large datasets, this uses distributed processing to handle chunks
        in parallel, then combines unique elements locally.

        Parameters
        ----------
        data:
            Input sequence.

        Returns
        -------
        list
            List with duplicates removed, preserving first occurrence order.
        """
        # For small datasets, use base implementation
        if len(data) < DISTINCT_THRESHOLD:
            return super().distinct(data)  # type: ignore[misc]

        # For large datasets, use distributed deduplication
        chunk_size = calculate_chunk_size(len(data), self._chunk_size)
        chunks = list(chunked(data, chunk_size))

        # Get unique elements from each chunk in parallel
        chunk_results = self._create_distinct_tasks(chunks)  # type: ignore[attr-defined]
        chunk_results = self._execute_distinct_tasks(chunk_results)  # type: ignore[attr-defined]

        # Combine results and deduplicate globally (must be done locally for order)
        combined = []
        for chunk_uniques in chunk_results:
            combined.extend(chunk_uniques)

        return list(dict.fromkeys(combined))

    def sort(
        self,
        data: Sequence[T],
        key: Callable[[T], Any] | None = None,
        reverse: bool = False,
    ) -> List[T]:
        """Sort using distributed sorting capabilities.

        For large datasets, this uses a distributed sort pattern:
        1. Sort chunks in parallel
        2. Merge sorted chunks

        Parameters
        ----------
        data:
            Input sequence.
        key:
            Optional key function for sorting.
        reverse:
            If True, sort in descending order.

        Returns
        -------
        list
            Sorted list.
        """
        # For small datasets, use base implementation
        if len(data) < SORT_THRESHOLD:
            return super().sort(data, key=key, reverse=reverse)  # type: ignore[misc]

        # For large datasets, use distributed sort-merge
        chunk_size = calculate_chunk_size(len(data), self._chunk_size)
        chunks = list(chunked(data, chunk_size))

        # Sort each chunk in parallel
        sorted_chunks = self._create_sort_tasks(chunks, key, reverse)  # type: ignore[attr-defined]
        sorted_chunks = self._execute_sort_tasks(sorted_chunks)  # type: ignore[attr-defined]

        # Merge sorted chunks using heapq
        if reverse:
            return list(heapq.merge(*sorted_chunks, key=key, reverse=True))

        return list(heapq.merge(*sorted_chunks, key=key))
