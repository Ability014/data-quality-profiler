from pathlib import Path

import pytest

from dqp.io import read_csv


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    p = tmp_path / "data.csv"
    p.write_text("id,name\n1,alice\n2,bob\n", encoding="utf-8")
    return p


def test_read_csv_roundtrip(csv_file):
    ds = read_csv(csv_file)
    assert ds.header == ["id", "name"]
    assert ds.row_count == 2
    assert ds.column("name") == ["alice", "bob"]


def test_empty_file_gives_empty_dataset(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("", encoding="utf-8")
    ds = read_csv(p)
    assert ds.header == [] and ds.rows == []


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_csv(tmp_path / "nope.csv")
