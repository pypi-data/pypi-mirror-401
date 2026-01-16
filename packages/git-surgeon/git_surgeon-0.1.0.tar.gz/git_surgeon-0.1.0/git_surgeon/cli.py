from __future__ import annotations

import argparse
import sys

from git_surgeon.commands import (
    absorb,
    describe,
    diff,
    drop,
    edit,
    file,
    fixup,
    merge,
    metaedit,
    move,
    new,
    op,
    pre_rebase,
    resolve,
    reword,
    show,
    split,
    squash,
    stashless,
    swap,
    undo,
)
from git_surgeon.git_utils import GitSurgeonError, ensure_git_repo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="git-surgeon",
        description="Streamline commit-centric workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    diff.add_parser(subparsers)
    show.add_parser(subparsers)
    op.add_parser(subparsers)
    stashless.add_parser(subparsers)
    new.add_parser(subparsers)
    undo.add_parser(subparsers)
    pre_rebase.add_parser(subparsers)
    resolve.add_parser(subparsers)
    reword.add_parser(subparsers)
    describe.add_parser(subparsers)
    edit.add_parser(subparsers)
    metaedit.add_parser(subparsers)
    absorb.add_parser(subparsers)
    squash.add_parser(subparsers)
    fixup.add_parser(subparsers)
    drop.add_parser(subparsers)
    merge.add_parser(subparsers)
    split.add_parser(subparsers)
    swap.add_parser(subparsers)
    move.add_parser(subparsers)
    file.add_parser(subparsers)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        ensure_git_repo()
        args.func(args)
    except GitSurgeonError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
