from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    parent_commit,
    rebase_in_progress,
    resolve_commit,
    resolve_revision_arg,
    start_rebase_action,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "drop",
        aliases=["d"],
        help="Drop a commit from history.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to drop.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to drop.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    commit = resolve_commit(
        resolve_revision_arg(args.commit, args.commit_ref, option_name="--commit")
    )
    parent = parent_commit(commit)
    start_rebase_action(commit, parent, "drop")
