from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    parent_commit,
    rebase_in_progress,
    resolve_commit,
    resolve_revision_arg,
    start_rebase_action,
    try_rev_parse,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "fixup",
        aliases=["f"],
        help="Fixup a commit into its parent.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to fix up.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to fix up.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    commit = resolve_commit(
        resolve_revision_arg(args.commit, args.commit_ref, option_name="--commit")
    )
    parent = parent_commit(commit)
    base = try_rev_parse(f"{parent}^") or "--root"
    start_rebase_action(commit, base, "fixup")
