from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    resolve_pre_rebase_ref,
    run_git,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "restore",
        help="Restore repository state to a reflog entry or commit.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Reflog entry or commit to restore.",
    )
    parser.add_argument(
        "--pre-rebase",
        action="store_true",
        help="Restore to the state before the last rebase.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--soft", action="store_true", help="Keep changes staged.")
    mode.add_argument("--mixed", action="store_true", help="Keep changes unstaged.")
    mode.add_argument("--hard", action="store_true", help="Discard changes (default).")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if args.pre_rebase and args.target:
        raise GitSurgeonError("Provide a target or --pre-rebase, not both.")

    if args.pre_rebase or args.target == "pre-rebase":
        target = resolve_pre_rebase_ref()
    else:
        if not args.target:
            raise GitSurgeonError("Provide a target to restore.")
        target = args.target

    if args.soft:
        mode = "--soft"
    elif args.mixed:
        mode = "--mixed"
    else:
        mode = "--hard"

    run_git(["reset", mode, target])
