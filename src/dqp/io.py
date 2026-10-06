from __future__ import annotations

import csv
from pathlib import Path

from dqp.models import Dataset


def read_csv(path: Path) -> Dataset:
    """Read a CSV file into a Dataset of raw string cells.

    No type inference and no friendly error handling yet — a missing file
    raises FileNotFoundError, which we'll turn into a clean CLI message on Day 5.
    """
    with path.open(newline="", encoding="utf-8") as f:   # newline="" is the csv-correct way to open
        reader = csv.reader(f)
        try:
            header = next(reader)          # first row is the header
        except StopIteration:
            return Dataset(header=[], rows=[])   # empty file -> empty dataset
        rows = [row for row in reader]     # everything else is data
    return Dataset(header=header, rows=rows)
