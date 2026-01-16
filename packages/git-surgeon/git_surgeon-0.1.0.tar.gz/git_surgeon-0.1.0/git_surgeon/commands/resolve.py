from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    cherry_pick_in_progress,
    merge_in_progress,
    rebase_in_progress,
    revert_in_progress,
    run_git,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "resolve",
        help="Continue, skip, or abort the current operation.",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--continue", dest="continue_op", action="store_true")
    action.add_argument("--abort", dest="abort_op", action="store_true")
    action.add_argument("--skip", dest="skip_op", action="store_true")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if not (
        rebase_in_progress()
        or merge_in_progress()
        or cherry_pick_in_progress()
        or revert_in_progress()
    ):
        raise GitSurgeonError("No rebase, merge, cherry-pick, or revert in progress.")

    if args.abort_op:
        command = "--abort"
    elif args.skip_op:
        command = "--skip"
    else:
        command = "--continue"

    if rebase_in_progress():
        run_git(["rebase", command])
        return
    if merge_in_progress():
        run_git(["merge", command])
        return
    if cherry_pick_in_progress():
        run_git(["cherry-pick", command])
        return
    if revert_in_progress():
        run_git(["revert", command])
