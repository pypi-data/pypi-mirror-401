from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    rebase_in_progress,
    resolve_commit,
    run_git,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "show",
        help="Show a file as it existed at a commit.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref.",
    )
    parser.add_argument("path", nargs="?", help="File path to show.")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    commit = args.commit
    path = args.path
    if args.commit_ref:
        if commit and path:
            raise GitSurgeonError("Provide a path once when using --commit.")
        if commit and not path:
            path = commit
            commit = None
        commit = args.commit_ref

    if not commit or not path:
        raise GitSurgeonError("Specify a commit and path to show.")

    commit = resolve_commit(commit)
    run_git(["show", f"{commit}:{path}"])
