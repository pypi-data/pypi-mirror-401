from __future__ import annotations

import argparse

from git_surgeon.git_utils import (
    GitSurgeonError,
    empty_tree_hash,
    rebase_in_progress,
    resolve_commit,
    run_git,
    try_rev_parse,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "diff",
        help="Show differences for a commit against its parent or HEAD.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to compare.")
    parser.add_argument(
        "-r",
        "--commit",
        dest="commit_ref",
        help="Commit hash or ref to compare.",
    )
    parser.add_argument(
        "--head",
        action="store_true",
        help="Compare the commit against HEAD instead of its parent.",
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="from_ref",
        help="Commit hash or ref to diff from.",
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="to_ref",
        help="Commit hash or ref to diff to.",
    )
    parser.add_argument("paths", nargs="*", help="Optional file paths to diff.")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    paths = list(args.paths)

    if args.from_ref or args.to_ref:
        if not args.from_ref or not args.to_ref:
            raise GitSurgeonError("Provide both --from and --to for diff.")
        if args.commit or args.commit_ref:
            raise GitSurgeonError("Use positional commit or --from/--to, not both.")
        from_commit = resolve_commit(args.from_ref)
        to_commit = resolve_commit(args.to_ref)
        command = ["diff", from_commit, to_commit]
    else:
        commit = args.commit
        if args.commit_ref:
            if commit:
                paths = [commit, *paths]
            commit = args.commit_ref
        if not commit:
            raise GitSurgeonError("Specify a commit to diff.")

        commit = resolve_commit(commit)

        if args.head:
            command = ["diff", commit, "HEAD"]
        else:
            parent = try_rev_parse(f"{commit}^")
            if not parent:
                parent = empty_tree_hash()
            command = ["diff", parent, commit]

    if paths:
        command += ["--", *paths]

    run_git(command)
