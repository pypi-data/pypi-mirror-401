from __future__ import annotations

import argparse
import datetime

from git_surgeon.git_utils import GitSurgeonError, run_git


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "stashless",
        help="Save WIP as a temporary commit on a branch.",
    )
    parser.add_argument(
        "--message",
        "-m",
        default="WIP",
        help="Commit message for the temporary commit.",
    )
    parser.add_argument(
        "--branch",
        "-b",
        help="Branch name to store the commit.",
    )
    parser.add_argument(
        "--keep-branch",
        "-k",
        action="store_true",
        help="Keep the current branch at the temporary commit.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    status = run_git(["status", "--porcelain"], capture=True) or ""
    if not status.strip():
        raise GitSurgeonError("No local changes to stashless.")

    run_git(["add", "-A"])
    run_git(["commit", "-m", args.message])

    branch = args.branch
    if not branch:
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        branch = f"wip/{stamp}"

    run_git(["branch", branch])
    if args.keep_branch:
        print(f"Saved WIP commit on branch {branch} (kept on current branch).")
        return

    run_git(["reset", "--hard", "HEAD~1"])
    print(f"Saved WIP commit on branch {branch}.")
