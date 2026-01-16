from __future__ import annotations

import argparse

from git_surgeon.git_utils import GitSurgeonError
from git_surgeon.commands.edit import run as edit_run


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "reword",
        aliases=["r"],
        help="Quickly edit a commit message.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to reword.")
    parser.add_argument("message", nargs="?", help="New commit message.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to reword.",
    )
    parser.add_argument(
        "-m",
        "--message",
        dest="message_flag",
        help="New commit message.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    commit = args.commit
    message = args.message
    if args.commit_ref:
        if commit and message:
            raise GitSurgeonError("Provide the message once when using --commit.")
        if commit and not message:
            message = commit
            commit = None
        commit = args.commit_ref

    if args.message_flag and message:
        raise GitSurgeonError(
            "Provide the message positionally or with --message, not both."
        )
    message = args.message_flag or message
    if not commit:
        raise GitSurgeonError("Missing commit argument for reword.")
    if not message:
        raise GitSurgeonError("A new message is required for reword.")

    args.commit = commit

    args.auto = True
    args.message = message
    edit_run(args)
