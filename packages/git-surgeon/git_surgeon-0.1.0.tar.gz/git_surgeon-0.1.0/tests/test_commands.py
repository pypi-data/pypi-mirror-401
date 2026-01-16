from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from git_surgeon.commands import split as split_cmd  # noqa


@contextlib.contextmanager
def temp_env(env: dict[str, str]) -> None:
    original = os.environ.copy()
    os.environ.update(env)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original)


@contextlib.contextmanager
def chdir(path: Path) -> None:
    original = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original)


class GitRepo:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)
        self.gitconfig = self.path / "gitconfig"
        self.gitconfig.write_text("")
        self.env = {
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.com",
            "GIT_CONFIG_GLOBAL": str(self.gitconfig),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_SEQUENCE_EDITOR": ":",
            "GIT_EDITOR": ":",
        }
        self.git("init")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.com")

    def cleanup(self) -> None:
        self.tmp.cleanup()

    def git(
        self, *args: str, input_text: str | None = None, env: dict | None = None
    ) -> str:
        merged_env = os.environ.copy()
        merged_env.update(self.env)
        if env:
            merged_env.update(env)
        result = subprocess.run(
            ["git", *args],
            cwd=self.path,
            env=merged_env,
            text=True,
            input=input_text,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()

    def write(self, relpath: str, content: str) -> None:
        path = self.path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def surgeon(
        self, *args: str, input_text: str | None = None, env: dict | None = None
    ) -> str:
        merged_env = os.environ.copy()
        merged_env.update(self.env)
        if env:
            merged_env.update(env)
        merged_env["PYTHONPATH"] = str(REPO_ROOT)
        result = subprocess.run(
            [sys.executable, "-m", "git_surgeon", *args],
            cwd=self.path,
            env=merged_env,
            text=True,
            input=input_text,
            capture_output=True,
            check=True,
        )
        return result.stdout


class CommandTests(unittest.TestCase):
    def test_diff_show_oplog(self) -> None:
        repo = GitRepo()
        try:
            repo.write("file.txt", "one\n")
            first = repo.commit("first")
            repo.write("file.txt", "two\n")
            second = repo.commit("second")

            diff_output = repo.surgeon("diff", second)
            self.assertIn("+two", diff_output)
            diff_head_output = repo.surgeon("diff", first, "--head")
            self.assertIn("+two", diff_head_output)
            show_output = repo.surgeon("show", first, "file.txt")
            self.assertEqual(show_output.strip(), "one")
            oplog_output = repo.surgeon("op", "log", "--count", "5")
            self.assertIn("commit", oplog_output)
        finally:
            repo.cleanup()

    def test_stashless_new_undo(self) -> None:
        repo = GitRepo()
        try:
            repo.write("file.txt", "base\n")
            repo.commit("base")
            repo.write("file.txt", "wip\n")
            repo.surgeon(
                "stashless", "--message", "WIP", "--branch", "wip/test", "--keep-branch"
            )
            self.assertEqual(repo.git("log", "-1", "--format=%s"), "WIP")
            self.assertEqual(repo.git("log", "-1", "--format=%s", "wip/test"), "WIP")

            repo.surgeon("new", "-m", "Empty")
            self.assertEqual(repo.git("log", "-1", "--format=%s"), "Empty")

            repo.surgeon("undo", "--hard", "--steps", "1")
            self.assertEqual(repo.git("log", "-1", "--format=%s"), "WIP")
        finally:
            repo.cleanup()

    def test_pre_rebase_and_resolve(self) -> None:
        repo = GitRepo()
        try:
            repo.write("file.txt", "one\n")
            repo.commit("one")
            repo.write("file.txt", "two\n")
            repo.commit("two")
            original = repo.git("rev-parse", "HEAD")

            script = repo.path / "edit-rebase.sh"
            script.write_text("sed -i -e 's/^pick /edit /' \"$1\"\n")
            script.chmod(0o755)
            repo.git("rebase", "-i", "HEAD~1", env={"GIT_SEQUENCE_EDITOR": str(script)})

            repo.surgeon("resolve", "--abort")
            self.assertEqual(repo.git("rev-parse", "HEAD"), original)

            repo.write("file.txt", "three\n")
            repo.commit("three")
            repo.git("rebase", "-i", "HEAD~2")
            orig_head = repo.git("rev-parse", "ORIG_HEAD")
            repo.surgeon("pre-rebase", "--hard")
            self.assertEqual(repo.git("rev-parse", "HEAD"), orig_head)
        finally:
            repo.cleanup()

    def test_reword_describe_edit_date(self) -> None:
        repo = GitRepo()
        try:
            repo.write("file.txt", "one\n")
            repo.commit("one")
            repo.write("file.txt", "two\n")
            repo.commit("two")

            repo.surgeon("reword", "HEAD", "reworded")
            self.assertEqual(repo.git("log", "-1", "--format=%s"), "reworded")

            repo.surgeon("describe", "HEAD", "-m", "described")
            self.assertEqual(repo.git("log", "-1", "--format=%s"), "described")

            repo.surgeon("edit", "HEAD", "-m", "edited")
            self.assertEqual(repo.git("log", "-1", "--format=%s"), "edited")

            repo.surgeon("metaedit", "date", "HEAD", "2024-01-01T12:00:00Z")
            committer_date = repo.git("show", "-s", "--format=%cI", "HEAD")
            self.assertIn(
                committer_date, {"2024-01-01T12:00:00Z", "2024-01-01T12:00:00+00:00"}
            )

            repo.surgeon("metaedit", "date", "HEAD", "-a", "2024-02-02T12:00:00Z")
            author_date = repo.git("show", "-s", "--format=%aI", "HEAD")
            self.assertIn(
                author_date, {"2024-02-02T12:00:00Z", "2024-02-02T12:00:00+00:00"}
            )

            repo.surgeon("metaedit", "date", "HEAD", "-c", "author")
            swapped_committer = repo.git("show", "-s", "--format=%cI", "HEAD")
            self.assertEqual(swapped_committer, author_date)

            repo.surgeon("metaedit", "author", "HEAD", "New Author")
            self.assertEqual(
                repo.git("show", "-s", "--format=%aN", "HEAD"), "New Author"
            )

            repo.surgeon("metaedit", "mail", "HEAD", "new@example.com")
            self.assertEqual(
                repo.git("show", "-s", "--format=%aE", "HEAD"), "new@example.com"
            )
        finally:
            repo.cleanup()

    def test_absorb_squash_fixup_drop(self) -> None:
        repo = GitRepo()
        try:
            repo.write("file.txt", "one\n")
            repo.commit("one")
            repo.write("other.txt", "base\n")
            repo.commit("two")

            repo.write("file.txt", "one updated\n")
            repo.git("add", "file.txt")
            repo.surgeon("absorb")
            log_output = repo.git("log", "--format=%s")
            self.assertNotIn("fixup!", log_output)
            self.assertEqual(repo.git("show", "HEAD:file.txt").strip(), "one updated")

            repo.write("other.txt", "more\n")
            repo.commit("three")
            commit_count = int(repo.git("rev-list", "--count", "HEAD"))
            repo.surgeon("squash", "HEAD", "--into", "HEAD~1")
            self.assertEqual(
                int(repo.git("rev-list", "--count", "HEAD")), commit_count - 1
            )

            repo.write("other.txt", "more again\n")
            repo.commit("four")
            count_before = int(repo.git("rev-list", "--count", "HEAD"))
            repo.surgeon("fixup", "HEAD")
            self.assertEqual(
                int(repo.git("rev-list", "--count", "HEAD")), count_before - 1
            )

            repo.write("file.txt", "final\n")
            repo.commit("five")
            count_before = int(repo.git("rev-list", "--count", "HEAD"))
            repo.surgeon("drop", "HEAD")
            self.assertEqual(
                int(repo.git("rev-list", "--count", "HEAD")), count_before - 1
            )
        finally:
            repo.cleanup()

    def test_merge_swap_move_untrack(self) -> None:
        repo = GitRepo()
        try:
            repo.write("file.txt", "one\n")
            repo.commit("one")

            repo.git("checkout", "-b", "feature")
            repo.write("feature.txt", "feat\n")
            repo.commit("feature")
            repo.git("checkout", "master")
            repo.surgeon("merge", "feature", "--no-ff", "-m", "merge feature")
            self.assertEqual(repo.git("log", "-1", "--format=%s"), "merge feature")
            repo.git("rev-parse", "HEAD^2")

            repo.write("swap_a.txt", "two\n")
            commit_b = repo.commit("two")
            repo.write("swap_b.txt", "three\n")
            commit_c = repo.commit("three")
            repo.surgeon("swap", commit_b, commit_c)
            order = repo.git("log", "--format=%s", "-3").splitlines()
            self.assertEqual(order[0], "two")
            self.assertEqual(order[1], "three")

            repo.write("move.txt", "four\n")
            commit_d = repo.commit("four")
            repo.surgeon("move", commit_d, "HEAD~1", "--before")
            order = repo.git("log", "--format=%s", "-3").splitlines()
            self.assertEqual(order[0], "two")
            self.assertEqual(order[1], "four")

            repo.write("tracked.txt", "keep\n")
            repo.commit("tracked")
            repo.surgeon("file", "untrack", "tracked.txt", "--no-history")
            tracked = repo.git("ls-files", "tracked.txt")
            self.assertEqual(tracked.strip(), "")
            self.assertTrue((repo.path / "tracked.txt").exists())
        finally:
            repo.cleanup()

    def test_split_and_split_interactive(self) -> None:
        repo = GitRepo()
        try:
            repo.write("base.txt", "base\n")
            repo.commit("base")
            repo.write("a.txt", "one\n")
            repo.write("b.txt", "two\n")
            combined = repo.commit("combined")

            args = type(
                "Args",
                (),
                {
                    "commit": combined,
                    "first_message": "first",
                    "second_message": "second",
                },
            )
            input_calls = {"count": 0}

            def split_input(_: str) -> str:
                input_calls["count"] += 1
                if input_calls["count"] == 1:
                    repo.git("add", "a.txt")
                else:
                    repo.git("add", "b.txt")
                return ""

            with temp_env(repo.env), chdir(repo.path):
                with unittest.mock.patch("builtins.input", split_input):
                    split_cmd.run(args)

            log_messages = repo.git("log", "--format=%s", "-2").splitlines()
            self.assertEqual(log_messages[0], "second")
            self.assertEqual(log_messages[1], "first")

            repo.write("c.txt", "three\n")
            repo.write("d.txt", "four\n")
            combined = repo.commit("combined-two")
            args = type(
                "Args",
                (),
                {
                    "commit": combined,
                    "first_message": "first-two",
                    "second_message": "second-two",
                },
            )

            original_run_git = split_cmd.run_git

            def patched_run_git(
                command: list[str], *, capture: bool = False, env: dict | None = None
            ) -> str | None:
                if command == ["add", "-p"]:
                    return original_run_git(["add", "c.txt"], capture=capture, env=env)
                return original_run_git(command, capture=capture, env=env)

            def split_interactive_input(_: str) -> str:
                repo.git("add", "d.txt")
                return ""

            with temp_env(repo.env), chdir(repo.path):
                with unittest.mock.patch("builtins.input", split_interactive_input):
                    with unittest.mock.patch(
                        "git_surgeon.commands.split.run_git",
                        patched_run_git,
                    ):
                        args.interactive = True
                        split_cmd.run(args)

            log_messages = repo.git("log", "--format=%s", "-2").splitlines()
            self.assertEqual(log_messages[0], "second-two")
            self.assertEqual(log_messages[1], "first-two")
        finally:
            repo.cleanup()


if __name__ == "__main__":
    unittest.main()
