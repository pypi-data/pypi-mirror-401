from __future__ import annotations

import argparse

from git_surgeon.git_utils import GitSurgeonError, rebase_in_progress, run_git


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "new",
        help="Create a new empty commit.",
    )
    parser.add_argument(
        "--message",
        "-m",
        help="Commit message. If omitted, opens the editor.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    command = ["commit", "--allow-empty"]
    if args.message:
        command += ["-m", args.message]

    run_git(command)
