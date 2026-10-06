from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ColumnType(str, Enum):
    """The type we infer for a column's values"""
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    STRING = "string"
    EMPTY = "empty"      # a column with no non-null values


@dataclass(frozen=True)
class Dataset:
    """Raw CSV content: a header plus rows of untyped string cells."""
    header: list[str]
    rows: list[list[str]]

    @property
    def row_count(self) -> int:
        return len(self.rows)

    def column(self, name: str) -> list[str]:
        """All cell values for one column, in row order."""
        idx = self.header.index(name)
        return [row[idx] for row in self.rows]


@dataclass(frozen=True)
class NumericStats:
    """Stats that only make sense for numeric columns."""
    minimum: float
    maximum: float
    mean: float


@dataclass(frozen=True)
class ColumnProfile:
    """The profile of a single column"""
    name: str
    inferred_type: ColumnType
    total_count: int
    null_count: int
    numeric: NumericStats | None = None   # present only for numeric columns

    @property
    def null_rate(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.null_count / self.total_count


@dataclass(frozen=True)
class DatasetProfile:
    """The profile of a whole dataset: one ColumnProfile per column."""
    source: str
    row_count: int
    columns: list[ColumnProfile]

    @property
    def column_count(self) -> int:
        return len(self.columns)
