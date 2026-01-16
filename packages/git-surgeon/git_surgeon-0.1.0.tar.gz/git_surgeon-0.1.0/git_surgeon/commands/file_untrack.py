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
        "untrack",
        help="Remove files from the repo but keep them on disk.",
    )
    parser.add_argument("paths", nargs="+", help="File paths to untrack.")
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="Do not rewrite history (default behavior).",
    )
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

    run_git(["rm", "--cached", "--", *args.paths])

    if args.no_history or (not args.from_ref and not args.root):
        return

    if args.root and args.from_ref:
        raise GitSurgeonError("Use --root or --from, not both.")

    if args.root:
        rev_list = ["--all"]
    else:
        if args.from_ref:
            start_commit = resolve_commit(args.from_ref)
        else:
            history = run_git(
                [
                    "log",
                    "--diff-filter=A",
                    "--format=%H",
                    "--reverse",
                    "--",
                    *args.paths,
                ],
                capture=True,
            )
            start_commit = history.splitlines()[0] if history else ""
            if not start_commit:
                raise GitSurgeonError("No tracked history found for the paths.")
        parent = try_rev_parse(f"{start_commit}^")
        rev_list = ["HEAD"] if not parent else [f"{start_commit}^..HEAD"]

    quoted_paths = " ".join(shlex.quote(path) for path in args.paths)
    index_filter = f"git rm --cached --ignore-unmatch -- {quoted_paths}"
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
