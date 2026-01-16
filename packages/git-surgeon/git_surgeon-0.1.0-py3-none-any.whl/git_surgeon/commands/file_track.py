from __future__ import annotations

import argparse
import shlex

from git_surgeon.git_utils import (
    GitSurgeonError,
    rebase_in_progress,
    resolve_commit,
    run_git,
    try_rev_parse,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "track",
        help="Start tracking files.",
    )
    parser.add_argument("paths", nargs="+", help="File paths to track.")
    parser.add_argument(
        "-f",
        "--from",
        dest="from_ref",
        help="Start rewriting history from this commit.",
    )
    parser.add_argument(
        "--root",
        action="store_true",
        help="Rewrite history from the root commit.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    run_git(["add", "-f", "--", *args.paths])

    if not args.from_ref and not args.root:
        return

    if args.root and args.from_ref:
        raise GitSurgeonError("Use --root or --from, not both.")

    if args.root:
        rev_list = ["--all"]
    else:
        start_commit = resolve_commit(args.from_ref)
        parent = try_rev_parse(f"{start_commit}^")
        rev_list = ["HEAD"] if not parent else [f"{start_commit}^..HEAD"]

    quoted_paths = " ".join(shlex.quote(path) for path in args.paths)
    index_filter = f"git add -f -- {quoted_paths}"
    run_git(
        [
            "filter-branch",
            "--force",
            "--index-filter",
            index_filter,
            "--prune-empty",
            "--tag-name-filter",
            "cat",
            "--",
            *rev_list,
        ]
    )
