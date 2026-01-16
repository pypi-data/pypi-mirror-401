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
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "move",
        help="Move a commit relative to another commit.",
    )
    parser.add_argument("commit", nargs="?", help="Commit hash or ref to move.")
    parser.add_argument(
        "destination",
        nargs="?",
        help="Commit hash or ref to move relative to.",
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="commit_ref",
        help="Commit hash or ref to move.",
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="destination_ref",
        help="Commit hash or ref to move relative to.",
    )
    placement = parser.add_mutually_exclusive_group()
    placement.add_argument(
        "--before",
        "-B",
        action="store_true",
        help="Move the commit before the destination.",
    )
    placement.add_argument(
        "--after",
        "-A",
        action="store_true",
        help="Move the commit after the destination (default).",
    )
    parser.add_argument(
        "--onto",
        action="store_true",
        help="Move the commit and its descendants onto the destination.",
    )
    parser.set_defaults(func=run)


def build_move_editor_script() -> str:
    return """
import os
import sys
from pathlib import Path

move_commit = os.environ.get("SURGEON_MOVE_COMMIT", "")
destination = os.environ.get("SURGEON_MOVE_DEST", "")
before = os.environ.get("SURGEON_MOVE_BEFORE", "0") == "1"
todo_path = Path(sys.argv[1])
lines = todo_path.read_text().splitlines()
actions = {"pick", "edit", "reword", "squash", "fixup", "drop"}
commit_index = None
dest_index = None

for index, line in enumerate(lines):
    parts = line.split()
    if len(parts) >= 2 and parts[0] in actions:
        sha = parts[1]
        if sha.startswith(move_commit) or move_commit.startswith(sha):
            commit_index = index
        if sha.startswith(destination) or destination.startswith(sha):
            dest_index = index

if commit_index is None or dest_index is None:
    raise SystemExit("Move commits not found in rebase todo list.")

commit_line = lines.pop(commit_index)
if commit_index < dest_index:
    dest_index -= 1

insert_at = dest_index if before else dest_index + 1
lines.insert(insert_at, commit_line)
todo_path.write_text("\\n".join(lines) + "\\n")
""".strip()


def start_rebase_move(base: str, commit: str, destination: str, before: bool) -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as script_file:
        script_file.write(build_move_editor_script())
        script_path = script_file.name

    env = os.environ.copy()
    env["SURGEON_MOVE_COMMIT"] = commit
    env["SURGEON_MOVE_DEST"] = destination
    env["SURGEON_MOVE_BEFORE"] = "1" if before else "0"
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
        resolve_revision_arg(args.commit, args.commit_ref, option_name="--from")
    )
    destination = resolve_commit(
        resolve_revision_arg(
            args.destination,
            args.destination_ref,
            label="destination",
            option_name="--to",
        )
    )

    if commit == destination:
        raise GitSurgeonError("Commit and destination must be different.")

    before = args.before
    if args.after:
        before = False

    if args.onto:
        if not is_ancestor(commit, "HEAD"):
            raise GitSurgeonError("Commit must be an ancestor of HEAD for --onto.")
        run_git(["rebase", "--onto", destination, f"{commit}^"])
        return

    if is_ancestor(commit, destination):
        older = commit
    elif is_ancestor(destination, commit):
        older = destination
    else:
        raise GitSurgeonError("Commits must be on the same ancestry path.")

    base = parent_commit(older)
    start_rebase_move(base, commit, destination, before)
