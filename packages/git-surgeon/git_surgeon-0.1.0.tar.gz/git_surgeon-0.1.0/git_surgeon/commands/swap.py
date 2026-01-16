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
    run_git,
)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "swap",
        help="Swap two commits in a linear history.",
    )
    parser.add_argument("commit_a", help="First commit hash or ref.")
    parser.add_argument("commit_b", help="Second commit hash or ref.")
    parser.set_defaults(func=run)


def build_swap_editor_script() -> str:
    return """
import os
import sys
from pathlib import Path

swap_a = os.environ.get("SURGEON_SWAP_A", "")
swap_b = os.environ.get("SURGEON_SWAP_B", "")
todo_path = Path(sys.argv[1])
lines = todo_path.read_text().splitlines()
actions = {"pick", "edit", "reword", "squash", "fixup", "drop"}
indexes = {}

for index, line in enumerate(lines):
    parts = line.split()
    if len(parts) >= 2 and parts[0] in actions:
        sha = parts[1]
        if sha.startswith(swap_a) or swap_a.startswith(sha):
            indexes["a"] = index
        if sha.startswith(swap_b) or swap_b.startswith(sha):
            indexes["b"] = index

if "a" not in indexes or "b" not in indexes:
    raise SystemExit("Swap commits not found in rebase todo list.")

lines[indexes["a"]], lines[indexes["b"]] = lines[indexes["b"]], lines[indexes["a"]]
todo_path.write_text("\\n".join(lines) + "\\n")
""".strip()


def start_rebase_swap(base: str, commit_a: str, commit_b: str) -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as script_file:
        script_file.write(build_swap_editor_script())
        script_path = script_file.name

    env = os.environ.copy()
    env["SURGEON_SWAP_A"] = commit_a
    env["SURGEON_SWAP_B"] = commit_b
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

    commit_a = resolve_commit(args.commit_a)
    commit_b = resolve_commit(args.commit_b)

    if commit_a == commit_b:
        raise GitSurgeonError("Commits to swap must be different.")

    if is_ancestor(commit_a, commit_b):
        older, newer = commit_a, commit_b
    elif is_ancestor(commit_b, commit_a):
        older, newer = commit_b, commit_a
    else:
        raise GitSurgeonError("Commits must be on the same ancestry path.")

    base = parent_commit(older)
    start_rebase_swap(base, older, newer)
