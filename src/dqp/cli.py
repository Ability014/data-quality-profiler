from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dqp import __version__
from dqp.errors import DqpError
from dqp.io import read_csv
from dqp.profile import profile_dataset
from dqp.render import render_json, render_text


def cmd_profile(args: argparse.Namespace) -> None:
    dataset = read_csv(args.path)
    profile = profile_dataset(dataset, source=str(args.path))
    output = render_json(profile) if args.format == "json" else render_text(profile)
    print(output)                      # the one place results go to stdout
    return


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dqp",
        description="Profile a dataset: row/column counts, types, null rates, numeric stats.",
    )

    parser.add_argument(
        "--version",
        action="version",                     # built-in action: print and exit(0)
        version=f"%(prog)s {__version__}",     # %(prog)s expands to "dqp"
    )

    sub = parser.add_subparsers(dest="command", required=True)
    profile_p = sub.add_parser("profile", help="profile a CSV file")
    profile_p.add_argument("path", type=Path, help="path to the CSV file")
    profile_p.add_argument(
        "--format", choices=("text", "json"), default="text",
        help="output format (default: text)",
    )
    profile_p.set_defaults(func=cmd_profile)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)   # handles --version itself and exits

    try:
        args.func(args)                 # run the chosen subcommand
        return 0
    except (DqpError, OSError) as exc:          # the single error boundary
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
