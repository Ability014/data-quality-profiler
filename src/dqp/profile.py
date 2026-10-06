from __future__ import annotations

from dqp.models import (
    ColumnProfile,
    ColumnType,
    Dataset,
    DatasetProfile,
    NumericStats,
)

_BOOLEANS = {"true", "false"}


def is_null(cell: str) -> bool:
    """A CSV cell is 'null' when it's empty or only whitespace."""
    return cell.strip() == ""


def _is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def _is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def _is_bool(s: str) -> bool:
    return s.strip().lower() in _BOOLEANS


def infer_type(non_null_values: list[str]) -> ColumnType:
    """Infer a column's type from its non-null values. Precedence matters."""
    if not non_null_values:
        return ColumnType.EMPTY
    if all(_is_bool(v) for v in non_null_values):
        return ColumnType.BOOLEAN
    if all(_is_int(v) for v in non_null_values):
        return ColumnType.INTEGER
    if all(_is_float(v) for v in non_null_values):
        return ColumnType.FLOAT
    return ColumnType.STRING


def _numeric_stats(non_null_values: list[str]) -> NumericStats:
    nums = [float(v) for v in non_null_values]
    return NumericStats(minimum=min(nums), maximum=max(nums), mean=sum(nums) / len(nums))


def profile_column(name: str, values: list[str]) -> ColumnProfile:
    """Profile one column from its raw string cells (nulls included)."""
    total = len(values)
    non_null = [v for v in values if not is_null(v)]
    col_type = infer_type(non_null)
    numeric = None
    if col_type in (ColumnType.INTEGER, ColumnType.FLOAT) and non_null:
        numeric = _numeric_stats(non_null)
    return ColumnProfile(
        name=name,
        inferred_type=col_type,
        total_count=total,
        null_count=total - len(non_null),
        numeric=numeric,
    )


def profile_dataset(dataset: Dataset, source: str = "<dataset>") -> DatasetProfile:
    """Profile every column. Pure: no file access, no output."""
    columns = [profile_column(name, dataset.column(name)) for name in dataset.header]
    return DatasetProfile(source=source, row_count=dataset.row_count, columns=columns)
