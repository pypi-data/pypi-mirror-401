from __future__ import annotations

import argparse

from git_surgeon.git_utils import GitSurgeonError, rebase_in_progress, run_git


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "log",
        help="Show recent reflog entries.",
    )
    parser.add_argument(
        "--count",
        "-n",
        "--limit",
        dest="count",
        type=int,
        default=20,
        help="Number of entries to show (default: 20).",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    run_git(["reflog", "--date=iso", f"-n{args.count}"])
