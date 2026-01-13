"""functional_list.mixins

Mixins used by the public ListMapper class.

Why mixins?
-----------
We want `ListMapper` to expose a rich API while keeping pylint's
`--max-public-methods` under control.

Since ListMapperIO always uses DEFAULT_FACTORY internally, these constructors
always return ListMapper.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from functional_list.io import CSVReadOptions, ListMapperIO, TextReadOptions


class ListMapperIOMixin:
    """I/O constructors exposed as classmethods on ListMapper."""

    @classmethod
    def from_csv(
        cls,
        file_path: str,
        options: CSVReadOptions = CSVReadOptions(),
        transform: Optional[Callable[[List[str]], Any]] = None,
    ):
        """Create a ListMapper from a CSV file."""
        return ListMapperIO.read_csv(file_path, options=options, transform=transform)

    @classmethod
    def from_text(
        cls,
        file_path: str,
        options: TextReadOptions = TextReadOptions(),
        transform: Optional[Callable[[str], Any]] = None,
    ):
        """Create a ListMapper from a text file."""
        return ListMapperIO.read_text(file_path, options=options, transform=transform)

    @classmethod
    def from_json(
        cls,
        file_path: str,
        encoding: str = "utf-8",
        transform: Optional[Callable[[Any], Any]] = None,
    ):
        """Create a ListMapper from a JSON file."""
        return ListMapperIO.read_json(file_path, encoding=encoding, transform=transform)

    @classmethod
    def from_jsonl(
        cls,
        file_path: str,
        encoding: str = "utf-8",
        transform: Optional[Callable[[Any], Any]] = None,
    ):
        """Create a ListMapper from a JSONL file."""
        return ListMapperIO.read_jsonl(
            file_path, encoding=encoding, transform=transform
        )

    @classmethod
    def from_parquet(
        cls,
        file_path: str,
        columns: Optional[List[str]] = None,
        transform: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ):
        """Create a ListMapper from a Parquet file."""
        return ListMapperIO.read_parquet(
            file_path, columns=columns, transform=transform
        )
