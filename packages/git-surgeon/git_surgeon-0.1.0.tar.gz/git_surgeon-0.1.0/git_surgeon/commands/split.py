from __future__ import annotations

import argparse
import os
from git_surgeon.git_utils import (
    GitSurgeonError,
    commit_dates,
    parent_commit,
    rebase_in_progress,
    resolve_commit,
    resolve_revision_arg,
    run_git,
    start_rebase_action,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "split",
        help="Split a commit into two, keeping dates.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to split.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to split.",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Use interactive staging for the first split.",
    )
    parser.add_argument("--first-message", help="Message for first commit.")
    parser.add_argument("--second-message", help="Message for second commit.")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    commit = resolve_commit(
        resolve_revision_arg(args.commit, getattr(args, "commit_ref", None))
    )
    dates = commit_dates(commit)
    parent = parent_commit(commit)
    start_rebase_action(commit, parent, "edit")

    if not rebase_in_progress():
        raise GitSurgeonError("Rebase did not stop at the target commit.")

    run_git(["reset", "HEAD^"])

    author_date, committer_date = dates
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = author_date
    env["GIT_COMMITTER_DATE"] = committer_date

    if getattr(args, "interactive", False):
        print("Commit split mode: use interactive staging for the first commit.")
        run_git(["add", "-p"])
    else:
        print("Commit split mode: stage changes for the first commit.")
        input("Press Enter after staging the first part...")

    first_command = ["commit"]
    if args.first_message:
        first_command += ["-m", args.first_message]
    run_git(first_command, env=env)

    print("Stage remaining changes for the second commit.")
    input("Press Enter after staging the second part...")
    second_command = ["commit"]
    if args.second_message:
        second_command += ["-m", args.second_message]
    run_git(second_command, env=env)

    run_git(["rebase", "--continue"])
