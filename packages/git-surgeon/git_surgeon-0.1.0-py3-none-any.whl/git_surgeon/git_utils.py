from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


class GitSurgeonError(RuntimeError):
    pass


def resolve_revision_arg(
    commit: str | None,
    ref: str | None,
    *,
    label: str = "commit",
    option_name: str = "--commit",
) -> str:
    if commit and ref:
        raise GitSurgeonError(
            f"Provide {label} as a positional argument or with {option_name}, not both."
        )
    if ref:
        return ref
    if commit:
        return commit
    raise GitSurgeonError(f"Missing {label} argument.")


def run_git(
    args: list[str], *, capture: bool = False, env: dict | None = None
) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            text=True,
            capture_output=capture,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() if exc.stderr else str(exc)
        raise GitSurgeonError(message) from exc
    return result.stdout.strip() if capture else None


def try_rev_parse(ref: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", ref],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def empty_tree_hash() -> str:
    return run_git(["hash-object", "-t", "tree", "/dev/null"], capture=True) or ""


def is_ancestor(older: str, newer: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    message = result.stderr.strip() if result.stderr else "Unknown error"
    raise GitSurgeonError(message)


def ensure_git_repo() -> None:
    try:
        run_git(["rev-parse", "--git-dir"], capture=True)
    except GitSurgeonError as exc:
        raise GitSurgeonError("Not inside a git repository.") from exc


def resolve_commit(commit: str) -> str:
    return run_git(["rev-parse", commit], capture=True) or ""


def commit_dates(commit: str) -> tuple[str, str]:
    author_date = run_git(["show", "-s", "--format=%aI", commit], capture=True) or ""
    committer_date = run_git(["show", "-s", "--format=%cI", commit], capture=True) or ""
    return author_date, committer_date


def commit_identities(commit: str) -> tuple[str, str, str, str]:
    author_name = run_git(["show", "-s", "--format=%aN", commit], capture=True) or ""
    author_email = run_git(["show", "-s", "--format=%aE", commit], capture=True) or ""
    committer_name = run_git(["show", "-s", "--format=%cN", commit], capture=True) or ""
    committer_email = (
        run_git(["show", "-s", "--format=%cE", commit], capture=True) or ""
    )
    return author_name, author_email, committer_name, committer_email


def resolve_pre_rebase_ref() -> str:
    orig_head = try_rev_parse("ORIG_HEAD")
    if orig_head:
        return orig_head

    reflog_entry = run_git(
        [
            "reflog",
            "--grep-reflog=rebase.*start",
            "-n",
            "1",
            "--format=%H",
        ],
        capture=True,
    )
    if not reflog_entry:
        raise GitSurgeonError("No rebase start found in reflog.")

    return reflog_entry.splitlines()[0]


def parent_commit(commit: str) -> str:
    return run_git(["rev-parse", f"{commit}^"], capture=True) or ""


def git_dir() -> Path:
    return Path(run_git(["rev-parse", "--git-dir"], capture=True) or ".")


def rebase_in_progress() -> bool:
    directory = git_dir()
    return (directory / "rebase-merge").exists() or (
        directory / "rebase-apply"
    ).exists()


def merge_in_progress() -> bool:
    return (git_dir() / "MERGE_HEAD").exists()


def cherry_pick_in_progress() -> bool:
    return (git_dir() / "CHERRY_PICK_HEAD").exists()


def revert_in_progress() -> bool:
    return (git_dir() / "REVERT_HEAD").exists()


def build_sequence_editor_script() -> str:
    return """
import os
import sys
from pathlib import Path

target = os.environ.get("SURGEON_TARGET", "")
action = os.environ.get("SURGEON_ACTION", "edit")
todo_path = Path(sys.argv[1])
lines = todo_path.read_text().splitlines()
new_lines = []
updated = False

for line in lines:
    if line.startswith("pick "):
        parts = line.split()
        if len(parts) >= 2:
            sha = parts[1]
            if sha.startswith(target) or target.startswith(sha):
                line = f"{action} " + " ".join(parts[1:])
                updated = True
    new_lines.append(line)

if not updated:
    raise SystemExit("Target commit not found in rebase todo list.")

todo_path.write_text("\\n".join(new_lines) + "\\n")
""".strip()


def start_rebase_action(commit: str, parent: str, action: str) -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as script_file:
        script_file.write(build_sequence_editor_script())
        script_path = script_file.name

    env = os.environ.copy()
    env["SURGEON_TARGET"] = commit
    env["SURGEON_ACTION"] = action
    env["GIT_SEQUENCE_EDITOR"] = f"{sys.executable} {script_path}"
    try:
        run_git(["rebase", "-i", parent], env=env)
    finally:
        try:
            os.unlink(script_path)
        except FileNotFoundError:
            pass


def print_manual_instructions(header: str, steps: list[str]) -> None:
    print(header)
    for step in steps:
        print(f"  - {step}")


def amend_commit(message: str | None, dates: tuple[str, str]) -> None:
    author_date, committer_date = dates
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = author_date
    env["GIT_COMMITTER_DATE"] = committer_date

    command = ["commit", "--amend"]
    if message:
        command += ["-m", message]

    run_git(command, env=env)
