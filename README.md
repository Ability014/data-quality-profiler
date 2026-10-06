# dqp — data quality profiler

![ci](https://github.com/<you>/dqp/actions/workflows/ci.yml/badge.svg)

Profile a CSV at the command line: row/column counts, inferred types,
null rates, and numeric summaries.

## Install
```bash
uv tool install .        # installs the `dqp` command onto your PATH
```

## Usage
```bash
dqp profile data.csv                 # formatted table
dqp profile data.csv --format json   # machine-readable
```

Example:

source: data.csv
rows: 3 columns: 3

column type nulls min max mean
id integer 0.0% - - -
name string 0.0% - - -
score float 33.3% 7.00 9.50 8.25


## Design
Three layers, deliberately separated:
- `models.py` — typed, frozen data containers (no logic)
- `io.py` — the only code that touches the filesystem
- `profile.py` — pure profiling logic (no IO, fully unit-tested)
- `render.py` / `cli.py` — formatting and the command-line boundary

Keeping the logic pure is why the test suite needs no files except in `test_io.py`.

## Development
```bash
uv pip install -e ".[dev]"
uv run pytest -q
uv run ruff check . && uv run mypy src
```
