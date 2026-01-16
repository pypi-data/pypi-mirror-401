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
        "abandon",
        help="Force-abandon a rebase and reset to its starting point.",
    )
    parser.set_defaults(func=run)


def run(_: argparse.Namespace) -> None:
    target = resolve_pre_rebase_ref()
    if rebase_in_progress():
        try:
            run_git(["rebase", "--abort"])
        except GitSurgeonError:
            pass
    run_git(["reset", "--hard", target])
