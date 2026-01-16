import subprocess
from datetime import datetime
from pathlib import Path

from src.cli import _build_pr_body, _format_cycle_summary_section
from src.models import CycleResult, Ticket
from src.tools.git_ops import GitOps
from src.tools.shell_runner import ShellRunner


def init_repo(repo_path: Path) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=repo_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True, capture_output=True)
    (repo_path / "README.md").write_text("init\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo_path, check=True, capture_output=True, text=True)


def commit_change(repo_path: Path, message: str, content: str) -> str:
    (repo_path / "README.md").write_text(content, encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True, capture_output=True, text=True)
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_path, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def test_build_pr_body_includes_multi_commit_summary(tmp_path: Path) -> None:
    init_repo(tmp_path)
    subprocess.run(["git", "checkout", "-b", "feature/test"], cwd=tmp_path, check=True, capture_output=True)

    first_sha = commit_change(tmp_path, "feat: cycle one", "init\ncycle one\n")
    second_sha = commit_change(tmp_path, "feat: cycle two", "init\ncycle one\ncycle two\n")

    git_ops = GitOps(ShellRunner(str(tmp_path)))
    commits = git_ops.get_commits_since_base("main", "feature/test")

    ticket = Ticket(
        number=105,
        title="Update Git workflow for frequent commits",
        description="Test ticket",
        url="https://github.com/jkbrooks/cce-agent/issues/105",
    )
    body = _build_pr_body(ticket=ticket, cycles=None, commits=commits)

    assert first_sha[:8] in body
    assert second_sha[:8] in body
    assert "feat: cycle one" in body
    assert "feat: cycle two" in body


def test_cycle_summary_section_includes_commit_and_tests() -> None:
    cycle = CycleResult(
        cycle_number=1,
        status="success",
        orientation="focus",
        start_time=datetime.now(),
        cycle_summary="Updated workflow",
        commit_sha="abc12345",
        tests_run=3,
        tests_passed=3,
        tests_failed=0,
    )

    section = _format_cycle_summary_section([cycle], commits=[])

    assert "Cycle 1" in section
    assert "Summary: Updated workflow" in section
    assert "Commit: `abc12345`" in section
    assert "Tests: 3/3 passed" in section
