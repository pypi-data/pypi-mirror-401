from __future__ import annotations

import argparse
import os

from git_surgeon.git_utils import (
    GitSurgeonError,
    commit_dates,
    commit_identities,
    parent_commit,
    rebase_in_progress,
    resolve_commit,
    resolve_revision_arg,
    run_git,
    start_rebase_action,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "author",
        help="Set commit author name.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to update.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to update.",
    )
    parser.add_argument("name", help="Author name.")
    parser.set_defaults(func=run)


def amend_with_author(
    *,
    name: str,
    author_email: str,
    committer_name: str,
    committer_email: str,
    author_date: str,
    committer_date: str,
) -> None:
    env = os.environ.copy()
    env["GIT_COMMITTER_NAME"] = committer_name
    env["GIT_COMMITTER_EMAIL"] = committer_email
    env["GIT_AUTHOR_DATE"] = author_date
    env["GIT_COMMITTER_DATE"] = committer_date
    author_value = f"{name} <{author_email}>"
    run_git(
        [
            "commit",
            "--amend",
            "--no-edit",
            "--author",
            author_value,
            "--date",
            author_date,
        ],
        env=env,
    )


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    commit = resolve_commit(
        resolve_revision_arg(args.commit, args.commit_ref, option_name="--commit")
    )
    author_date, committer_date = commit_dates(commit)
    _, author_email, committer_name, committer_email = commit_identities(commit)

    if commit == resolve_commit("HEAD"):
        amend_with_author(
            name=args.name,
            author_email=author_email,
            committer_name=committer_name,
            committer_email=committer_email,
            author_date=author_date,
            committer_date=committer_date,
        )
        return

    parent = parent_commit(commit)
    start_rebase_action(commit, parent, "edit")

    if not rebase_in_progress():
        raise GitSurgeonError("Rebase did not stop at the target commit.")

    amend_with_author(
        name=args.name,
        author_email=author_email,
        committer_name=committer_name,
        committer_email=committer_email,
        author_date=author_date,
        committer_date=committer_date,
    )
    run_git(["rebase", "--continue"])
