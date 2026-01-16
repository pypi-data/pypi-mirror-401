from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    rebase_in_progress,
    resolve_pre_rebase_ref,
    run_git,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "pre-rebase",
        help="Reset to the commit before the last rebase.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--soft", action="store_true", help="Keep changes staged.")
    mode.add_argument("--mixed", action="store_true", help="Keep changes unstaged.")
    mode.add_argument("--hard", action="store_true", help="Discard changes (default).")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    if args.soft:
        mode = "--soft"
    elif args.mixed:
        mode = "--mixed"
    else:
        mode = "--hard"

    target = resolve_pre_rebase_ref()
    run_git(["reset", mode, target])
