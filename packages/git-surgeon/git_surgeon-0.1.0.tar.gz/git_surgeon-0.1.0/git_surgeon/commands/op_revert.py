from __future__ import annotations

import argparse

from git_surgeon.git_utils import GitSurgeonError, resolve_pre_rebase_ref, run_git


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "revert",
        help="Create a new commit that reverts a prior one.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Commit to revert (default: HEAD).",
    )
    parser.add_argument(
        "--pre-rebase",
        action="store_true",
        help="Revert the commit before the last rebase.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if args.pre_rebase and args.target:
        raise GitSurgeonError("Provide a target or --pre-rebase, not both.")

    if args.pre_rebase or args.target == "pre-rebase":
        target = resolve_pre_rebase_ref()
    else:
        target = args.target or "HEAD"

    run_git(["revert", "--no-edit", target])
