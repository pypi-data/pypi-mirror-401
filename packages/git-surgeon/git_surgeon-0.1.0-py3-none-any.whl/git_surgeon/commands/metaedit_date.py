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
        "date",
        help="Set commit dates without changing content.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to update.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to update.",
    )
    parser.add_argument("date", nargs="?", help="Date value (RFC2822 or RFC3339).")
    parser.add_argument(
        "--date",
        dest="date_flag",
        help="Date value (RFC2822 or RFC3339).",
    )
    parser.add_argument(
        "-c",
        "--committer",
        action="store_true",
        help="Update committer date (default).",
    )
    parser.add_argument(
        "-a",
        "--author",
        action="store_true",
        help="Update author date.",
    )
    parser.set_defaults(func=run)


def resolve_date_value(args: argparse.Namespace) -> str:
    if args.date and args.date_flag:
        raise GitSurgeonError("Provide the date once, not both positional and --date.")
    date_value = args.date_flag or args.date
    if not date_value:
        raise GitSurgeonError("Provide a date value.")
    return date_value


def amend_with_dates(author_date: str, committer_date: str) -> None:
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = author_date
    env["GIT_COMMITTER_DATE"] = committer_date
    run_git(["commit", "--amend", "--no-edit", "--date", author_date], env=env)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    date_value = resolve_date_value(args)
    set_author = args.author
    set_committer = args.committer or not set_author

    commit = resolve_commit(
        resolve_revision_arg(args.commit, args.commit_ref, option_name="--commit")
    )
    original_author_date, original_committer_date = commit_dates(commit)

    author_date = original_author_date
    committer_date = original_committer_date

    if set_author:
        author_date = original_committer_date if date_value == "commit" else date_value
    if set_committer:
        committer_date = original_author_date if date_value == "author" else date_value

    if commit == resolve_commit("HEAD"):
        amend_with_dates(author_date, committer_date)
        return

    parent = parent_commit(commit)
    start_rebase_action(commit, parent, "edit")

    if not rebase_in_progress():
        raise GitSurgeonError("Rebase did not stop at the target commit.")

    amend_with_dates(author_date, committer_date)
    run_git(["rebase", "--continue"])
