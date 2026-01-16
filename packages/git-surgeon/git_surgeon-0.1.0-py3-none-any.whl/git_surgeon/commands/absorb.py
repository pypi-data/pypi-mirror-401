from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    rebase_in_progress,
    run_git,
    try_rev_parse,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "absorb",
        help="Absorb staged changes into the latest touching commit.",
    )
    parser.set_defaults(func=run)


def latest_commit_for_paths(paths: list[str]) -> str:
    commit = run_git(["log", "-n", "1", "--format=%H", "--", *paths], capture=True)
    if not commit:
        raise GitSurgeonError("No commit found for staged paths.")
    return commit


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    staged = run_git(["diff", "--cached", "--name-only"], capture=True) or ""
    paths = [line for line in staged.splitlines() if line.strip()]
    if not paths:
        raise GitSurgeonError("Stage changes before running absorb.")

    target = latest_commit_for_paths(paths)
    run_git(["commit", "--fixup", target])

    base = try_rev_parse(f"{target}^")
    if base:
        run_git(["rebase", "-i", "--autosquash", base])
    else:
        run_git(["rebase", "-i", "--autosquash", "--root"])
