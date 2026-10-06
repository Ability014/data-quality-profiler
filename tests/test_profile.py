import pytest

from dqp.models import ColumnType, Dataset
from dqp.profile import infer_type, is_null, profile_column, profile_dataset


@pytest.mark.parametrize(
    "cell, expected",
    [
        ("", True),
        ("   ", True),
        ("0", False),
        ("x", False),
    ],
)
def test_is_null(cell, expected):
    assert is_null(cell) is expected


@pytest.mark.parametrize(
    "values, expected",
    [
        (["1", "2", "3"], ColumnType.INTEGER),
        (["1.5", "2", "3"], ColumnType.FLOAT),  # mixed int+float -> float
        (["true", "FALSE"], ColumnType.BOOLEAN),  # case-insensitive
        (["-3", "4", "0"], ColumnType.INTEGER),  # negatives still integer
        (["a", "1", "x"], ColumnType.STRING),
        ([], ColumnType.EMPTY),  # no non-null values
    ],
)
def test_infer_type(values, expected):
    assert infer_type(values) == expected


def test_profile_column_nulls_and_numeric_stats():
    col = profile_column("score", ["9.5", "", "7.0"])
    assert col.inferred_type == ColumnType.FLOAT
    assert col.total_count == 3
    assert col.null_count == 1
    assert col.null_rate == pytest.approx(1 / 3)
    assert col.numeric is not None
    assert col.numeric.minimum == 7.0
    assert col.numeric.maximum == 9.5
    assert col.numeric.mean == pytest.approx(8.25)


def test_all_null_column_is_empty_with_no_stats():
    col = profile_column("blank", ["", "  ", ""])
    assert col.inferred_type == ColumnType.EMPTY
    assert col.null_rate == 1.0
    assert col.numeric is None


def test_profile_dataset_shape_and_source():
    ds = Dataset(header=["id", "name"], rows=[["1", "a"], ["2", "b"]])
    prof = profile_dataset(ds, source="t.csv")
    assert prof.source == "t.csv"
    assert prof.row_count == 2
    assert prof.column_count == 2
    assert [c.name for c in prof.columns] == ["id", "name"]
