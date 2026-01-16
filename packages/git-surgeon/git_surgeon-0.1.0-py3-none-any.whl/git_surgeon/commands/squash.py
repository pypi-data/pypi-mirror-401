from __future__ import annotations

import argparse

import os
import sys
import tempfile

from git_surgeon.git_utils import (
    GitSurgeonError,
    is_ancestor,
    parent_commit,
    rebase_in_progress,
    resolve_commit,
    resolve_revision_arg,
    run_git,
    start_rebase_action,
    try_rev_parse,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "squash",
        aliases=["s"],
        help="Squash a commit into its parent or another commit.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to squash.")
    parser.add_argument(
        "-r",
        "--commit",
        "-f",
        "--from",
        dest="commit_ref",
        help="Commit hash or ref to squash.",
    )
    parser.add_argument(
        "--into",
        "-t",
        "--to",
        dest="into",
        help="Commit hash or ref to squash into (must be an ancestor).",
    )
    parser.set_defaults(func=run)


def build_squash_into_script() -> str:
    return """
import os
import sys
from pathlib import Path

target = os.environ.get("SURGEON_SQUASH_TARGET", "")
commit = os.environ.get("SURGEON_SQUASH_COMMIT", "")
todo_path = Path(sys.argv[1])
lines = todo_path.read_text().splitlines()
actions = {"pick", "edit", "reword", "squash", "fixup", "drop"}
target_index = None
commit_index = None

for index, line in enumerate(lines):
    parts = line.split()
    if len(parts) >= 2 and parts[0] in actions:
        sha = parts[1]
        if sha.startswith(target) or target.startswith(sha):
            target_index = index
        if sha.startswith(commit) or commit.startswith(sha):
            commit_index = index

if target_index is None or commit_index is None:
    raise SystemExit("Target commit not found in rebase todo list.")

commit_line = lines.pop(commit_index)
if commit_index < target_index:
    target_index -= 1

parts = commit_line.split()
commit_line = "squash " + " ".join(parts[1:])
lines.insert(target_index + 1, commit_line)
todo_path.write_text("\\n".join(lines) + "\\n")
""".strip()


def start_rebase_squash(base: str, commit: str, target: str) -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as script_file:
        script_file.write(build_squash_into_script())
        script_path = script_file.name

    env = os.environ.copy()
    env["SURGEON_SQUASH_TARGET"] = target
    env["SURGEON_SQUASH_COMMIT"] = commit
    env["GIT_SEQUENCE_EDITOR"] = f"{sys.executable} {script_path}"
    try:
        run_git(["rebase", "-i", base], env=env)
    finally:
        try:
            os.unlink(script_path)
        except FileNotFoundError:
            pass


def run(args: argparse.Namespace) -> None:
    if rebase_in_progress():
        raise GitSurgeonError("A rebase is already in progress.")

    commit = resolve_commit(
        resolve_revision_arg(args.commit, args.commit_ref, option_name="--commit")
    )
    if args.into:
        target = resolve_commit(args.into)
        if commit == target:
            raise GitSurgeonError("Commit and target must be different.")
        if not is_ancestor(target, commit):
            raise GitSurgeonError("Target must be an ancestor of the commit.")
        base = parent_commit(target)
        start_rebase_squash(base, commit, target)
        return

    parent = parent_commit(commit)
    base = try_rev_parse(f"{parent}^") or "--root"
    start_rebase_action(commit, base, "squash")
