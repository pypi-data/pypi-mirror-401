from __future__ import annotations

import argparse

from git_surgeon.git_utils import GitSurgeonError, run_git


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "undo",
        help="Reset branch to a previous HEAD from reflog.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--soft", action="store_true", help="Keep changes staged.")
    mode.add_argument("--mixed", action="store_true", help="Keep changes unstaged.")
    mode.add_argument("--hard", action="store_true", help="Discard changes (default).")
    parser.add_argument(
        "--steps",
        "-n",
        type=int,
        default=1,
        help="How many HEAD positions to rewind (default: 1).",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if args.steps < 1:
        raise GitSurgeonError("--steps must be >= 1")

    if args.soft:
        mode = "--soft"
    elif args.mixed:
        mode = "--mixed"
    else:
        mode = "--hard"

    target = f"HEAD@{{{args.steps}}}"
    run_git(["reset", mode, target])
