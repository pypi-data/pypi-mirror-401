from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    amend_commit,
    commit_dates,
    parent_commit,
    print_manual_instructions,
    rebase_in_progress,
    resolve_commit,
    resolve_revision_arg,
    run_git,
    start_rebase_action,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "describe",
        aliases=["desc"],
        help="Edit a commit message without changing content.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to describe.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to describe.",
    )
    parser.add_argument(
        "--message",
        "-m",
        help="New commit message. If omitted, open editor.",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Immediately amend with current content.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    commit = resolve_commit(
        resolve_revision_arg(args.commit, args.commit_ref, option_name="--commit")
    )
    dates = commit_dates(commit)
    parent = parent_commit(commit)

    start_rebase_action(commit, parent, "edit")

    if not rebase_in_progress():
        raise GitSurgeonError("Rebase did not stop at the target commit.")

    if args.message or args.auto:
        amend_commit(args.message, dates)
        run_git(["rebase", "--continue"])
        return

    author_date, committer_date = dates
    print_manual_instructions(
        "Rebase paused at the commit. To edit and keep the original date:",
        [
            f"GIT_AUTHOR_DATE='{author_date}' GIT_COMMITTER_DATE='{committer_date}' git commit --amend",
            "git rebase --continue",
        ],
    )
