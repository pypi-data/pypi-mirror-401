"""
This module provides I/O operations for reading data from various file formats
into ListMapper objects.

Supported formats:
- CSV files
- JSON files
- Parquet files
- Text files
"""

import csv
import importlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

try:
    import pyarrow.parquet as pq  # type: ignore
except ImportError:  # pragma: no cover
    pq = None  # type: ignore[assignment]

if TYPE_CHECKING:
    from functional_list import ListMapper


@dataclass(frozen=True)
class CSVReadOptions:
    """Options for reading CSV files."""

    delimiter: str = ","
    skip_header: bool = False
    encoding: str = "utf-8"


@dataclass(frozen=True)
class TextReadOptions:
    """Options for reading text files."""

    encoding: str = "utf-8"
    strip_lines: bool = True
    skip_empty: bool = False


class ListMapperIO:
    """I/O operations for reading data into ListMapper objects.

    This class does not require pandas.

    Implementation note:
        To avoid circular imports, ListMapper is resolved lazily.
    """

    @staticmethod
    def create(*items: Any) -> "ListMapper":
        """Create a ListMapper from positional items.

        This is the single place where ListMapper is imported, and it is done
        lazily to avoid circular-import issues.
        """

        lm_mod = importlib.import_module("functional_list.list_functional_mapper")
        list_mapper_cls = lm_mod.ListMapper
        return list_mapper_cls(*items)

    @staticmethod
    def read_csv(
        file_path: Union[str, Path],
        options: CSVReadOptions = CSVReadOptions(),
        transform: Optional[Callable[[List[str]], Any]] = None,
    ) -> "ListMapper":
        """
        Read data from a CSV file into a ListMapper.

        :param file_path: Path to the CSV file
        :param options: CSV read options (delimiter, skip_header, encoding)
        :param transform: Optional function to transform each row
        :return: ListMapper containing the CSV data

        Example:
        >> data = ListMapperIO.read_csv('data.csv')
        >> # With transformation
        >> data = ListMapperIO.read_csv('data.csv',
        ..                               transform=lambda row: {'name': row[0], 'age': int(row[1])})
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        rows: List[Any] = []
        with open(file_path, "r", encoding=options.encoding, newline="") as f:
            reader = csv.reader(f, delimiter=options.delimiter)
            if options.skip_header:
                next(reader, None)

            for row in reader:
                rows.append(transform(row) if transform else row)

        return ListMapperIO.create(*rows)

    @staticmethod
    def read_json(
        file_path: Union[str, Path],
        encoding: str = "utf-8",
        transform: Optional[Callable[[Any], Any]] = None,
    ) -> "ListMapper":
        """
        Read data from a JSON file into a ListMapper.
        Expects JSON to be an array or converts single object to single-element list.

        :param file_path: Path to the JSON file
        :param encoding: File encoding (default: 'utf-8')
        :param transform: Optional function to transform each item
        :return: ListMapper containing the JSON data

        Example:
        >> data = ListMapperIO.read_json('data.json')
        >> # With transformation
        >> data = ListMapperIO.read_json('data.json', transform=lambda x: x['name'])
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding=encoding) as f:
            data = json.load(f)

        # Handle both array and single object
        if isinstance(data, list):
            items = data
        else:
            items = [data]

        if transform:
            items = [transform(item) for item in items]

        return ListMapperIO.create(*items)

    @staticmethod
    def read_text(
        file_path: Union[str, Path],
        options: TextReadOptions = TextReadOptions(),
        transform: Optional[Callable[[str], Any]] = None,
    ) -> "ListMapper":
        """
        Read data from a text file into a ListMapper (one line per element).

        :param file_path: Path to the text file
        :param options: Text read options (encoding, strip_lines, skip_empty)
        :param transform: Optional function to transform each line
        :return: ListMapper containing the text lines

        Example:
        >> data = ListMapperIO.read_text('data.txt')
        >> # With transformation
        >> data = ListMapperIO.read_text('data.txt', transform=lambda line: line.upper())
        >> # Skip empty lines and strip
        >> data = ListMapperIO.read_text('data.txt', strip_lines=True, skip_empty=True)
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        lines: List[Any] = []
        with open(file_path, "r", encoding=options.encoding) as f:
            for line in f:
                if options.strip_lines:
                    line = line.strip()
                if options.skip_empty and not line:
                    continue
                lines.append(transform(line) if transform else line)

        return ListMapperIO.create(*lines)

    @staticmethod
    def read_jsonl(
        file_path: Union[str, Path],
        encoding: str = "utf-8",
        transform: Optional[Callable[[Any], Any]] = None,
    ) -> "ListMapper":
        """
        Read data from a JSON Lines file (JSONL/NDJSON) into a ListMapper.
        Each line should be a valid JSON object.

        :param file_path: Path to the JSONL file
        :param encoding: File encoding (default: 'utf-8')
        :param transform: Optional function to transform each JSON object
        :return: ListMapper containing the JSON objects

        Example:
        >> data = ListMapperIO.read_jsonl('data.jsonl')
        >> # With transformation
        >> data = ListMapperIO.read_jsonl('data.jsonl', transform=lambda obj: obj['id'])
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        items: List[Any] = []
        with open(file_path, "r", encoding=encoding) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                obj = json.loads(line)
                if transform:
                    items.append(transform(obj))
                else:
                    items.append(obj)

        return ListMapperIO.create(*items)

    @staticmethod
    def read_parquet(
        file_path: Union[str, Path],
        columns: Optional[List[str]] = None,
        transform: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ) -> "ListMapper":
        """
        Read data from a Parquet file into a ListMapper.
        Requires 'pyarrow' to be installed.

        :param file_path: Path to the Parquet file
        :param columns: Optional list of columns to read (reads all if None)
        :param transform: Optional function to transform each row (dict)
        :return: ListMapper containing the Parquet data

        Example:
        >> data = ListMapperIO.read_parquet('data.parquet')
        >> # With specific columns
        >> data = ListMapperIO.read_parquet('data.parquet', columns=['name', 'age'])
        >> # With transformation
        >> data = ListMapperIO.read_parquet('data.parquet', transform=lambda row: row['name'])
        """
        if pq is None:
            raise ImportError(
                "Reading Parquet files requires 'pyarrow'. "
                "Install with: uv add pyarrow  OR  pip install pyarrow"
            )

        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        table = pq.read_table(file_path, columns=columns)
        rows = table.to_pylist()
        if transform:
            rows = [transform(row) for row in rows]

        return ListMapperIO.create(*rows)
