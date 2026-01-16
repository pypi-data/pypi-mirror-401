import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("."))

from src.tools.git_ops import GitOps
from src.tools.shell_runner import ShellResult


class FakeShell:
    def __init__(self) -> None:
        self.commands: list[str] = []

    def execute(self, command: str, cwd: str | None = None) -> ShellResult:
        self.commands.append(command)
        if command.startswith("gh --version"):
            return ShellResult(command=command, exit_code=0, stdout="gh version 2.0.0", stderr="", duration=0.0)
        if command.startswith("gh pr create"):
            return ShellResult(
                command=command, exit_code=0, stdout="https://example.com/pr/1", stderr="", duration=0.0
            )
        return ShellResult(command=command, exit_code=0, stdout="", stderr="", duration=0.0)


class TrackingGitOps(GitOps):
    def __init__(self, shell: FakeShell, commits: list[dict[str, str]], rebased: bool = True) -> None:
        super().__init__(shell)
        self._commits = commits
        self._rebased = rebased
        self.rebase_calls: list[tuple[str, str | None, str]] = []
        self.push_calls: list[tuple[str, bool, str]] = []

    def get_current_branch(self) -> str | None:
        return "feature-branch"

    def resolve_pr_base_branch(self, base_branch: str | None, remote: str = "origin") -> str:
        return base_branch or "main"

    def ensure_local_branch(self, branch: str, remote: str = "origin") -> bool:
        return True

    def rebase_onto_base(self, base_branch: str, head_branch: str | None = None, remote: str = "origin"):
        self.rebase_calls.append((base_branch, head_branch, remote))
        return {"success": True, "rebased": self._rebased, "message": "rebased"}

    def get_commits_since_base(self, base_branch: str, head_branch: str | None = None) -> list[dict[str, str]]:
        return list(self._commits)

    def push_branch(self, branch_name: str, force: bool = False, remote: str = "origin") -> bool:
        self.push_calls.append((branch_name, force, remote))
        return True


def test_create_pull_request_summarizes_commits_and_forces_push(monkeypatch):
    captured: dict[str, str] = {}

    def fake_unlink(path: str) -> None:
        captured["body"] = Path(path).read_text(encoding="utf-8")

    monkeypatch.setattr(os, "unlink", fake_unlink)

    shell = FakeShell()
    git_ops = TrackingGitOps(
        shell,
        commits=[
            {"sha": "aaaa1111", "message": "chore: reconcile cycle 1"},
            {"sha": "bbbb2222", "message": "chore: reconcile cycle 2"},
        ],
    )

    result = git_ops.create_pull_request(
        title="Test PR",
        body="",
        head_branch="feature-branch",
        base_branch="main",
    )

    assert result["success"] is True
    assert git_ops.rebase_calls == [("main", "feature-branch", "origin")]
    assert git_ops.push_calls == [("feature-branch", True, "origin")]
    assert "chore: reconcile cycle 1" in captured["body"]
    assert "chore: reconcile cycle 2" in captured["body"]
    assert any("gh pr create" in command for command in shell.commands)


def test_create_pull_request_skips_when_no_commits():
    shell = FakeShell()
    git_ops = TrackingGitOps(shell, commits=[])

    result = git_ops.create_pull_request(
        title="Test PR",
        body="",
        head_branch="feature-branch",
        base_branch="main",
    )

    assert result["skipped"] is True
    assert git_ops.push_calls == []
    assert not any("gh pr create" in command for command in shell.commands)
