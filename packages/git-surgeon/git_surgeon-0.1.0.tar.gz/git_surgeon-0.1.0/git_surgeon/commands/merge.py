from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    rebase_in_progress,
    resolve_revision_arg,
    run_git,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "merge",
        aliases=["m"],
        help="Merge another commit or branch into the current branch.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to merge.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to merge.",
    )
    parser.add_argument(
        "--message",
        "-m",
        help="Commit message for the merge.",
    )
    parser.add_argument(
        "--no-ff",
        action="store_true",
        help="Create a merge commit even if fast-forward is possible.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    command = ["merge"]
    if args.no_ff:
        command.append("--no-ff")
    if args.message:
        command += ["-m", args.message]
    commit = resolve_revision_arg(args.commit, args.commit_ref, option_name="--commit")
    command.append(commit)
    run_git(command)
