import logging
import subprocess
from datetime import datetime
from pathlib import Path

from src.agent import CCEAgent
from src.models import CycleResult
from src.tools.git_ops import GitOps
from src.tools.shell_runner import ShellRunner


def init_repo(repo_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True, capture_output=True)
    (repo_path / "README.md").write_text("init\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo_path, check=True, capture_output=True, text=True)


def git_head_sha(repo_path: Path) -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_path, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def git_commit_message(repo_path: Path) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"], cwd=repo_path, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def make_agent(repo_path: Path) -> CCEAgent:
    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("test_reconcile_commit_step")
    agent.git_ops = GitOps(ShellRunner(str(repo_path)))
    return agent


def test_format_commit_message_includes_summary_and_tests():
    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("test_reconcile_commit_step")
    cycle_result = CycleResult(
        cycle_number=2,
        status="success",
        orientation="focus",
        start_time=datetime.now(),
        final_summary="Did work\nNext focus: Add coverage",
    )

    message = agent._format_commit_message(
        cycle_number=2,
        cycle_result=cycle_result,
        test_results="**Passed Tests**: 2\n**Failed Tests**: 0",
        evaluation_result=None,
    )

    assert message.startswith("chore: reconcile cycle 2")
    assert "Summary: Did work" in message
    assert "Tests: 2 passed, 0 failed" in message
    assert "Next focus: Add coverage" in message


def test_commit_cycle_work_commits_when_tests_pass(tmp_path: Path):
    init_repo(tmp_path)
    (tmp_path / "README.md").write_text("init\nupdate\n", encoding="utf-8")

    agent = make_agent(tmp_path)
    cycle_result = CycleResult(
        cycle_number=1,
        status="success",
        orientation="focus",
        start_time=datetime.now(),
        final_summary="Updated README\nNext focus: Review changes",
    )

    commit_sha = agent._commit_cycle_work(
        cycle_number=1,
        cycle_result=cycle_result,
        test_results="**Passed Tests**: 1\n**Failed Tests**: 0",
        evaluation_result=None,
    )

    assert commit_sha
    assert commit_sha == git_head_sha(tmp_path)
    assert git_commit_message(tmp_path).startswith("chore: reconcile cycle 1")


def test_commit_cycle_work_skips_when_tests_fail(tmp_path: Path):
    init_repo(tmp_path)
    (tmp_path / "README.md").write_text("init\nupdate\n", encoding="utf-8")

    agent = make_agent(tmp_path)
    cycle_result = CycleResult(
        cycle_number=1,
        status="failure",
        orientation="focus",
        start_time=datetime.now(),
        final_summary="Updated README\nNext focus: Fix tests",
    )

    head_before = git_head_sha(tmp_path)
    commit_sha = agent._commit_cycle_work(
        cycle_number=1,
        cycle_result=cycle_result,
        test_results="**Passed Tests**: 0\n**Failed Tests**: 1",
        evaluation_result=None,
    )

    assert commit_sha is None
    assert git_head_sha(tmp_path) == head_before


def test_commit_cycle_work_creates_multiple_commits(tmp_path: Path):
    init_repo(tmp_path)
    agent = make_agent(tmp_path)

    (tmp_path / "README.md").write_text("init\ncycle one\n", encoding="utf-8")
    cycle_one = CycleResult(
        cycle_number=1,
        status="success",
        orientation="focus",
        start_time=datetime.now(),
        final_summary="Cycle one update\nNext focus: Continue work",
    )
    first_sha = agent._commit_cycle_work(
        cycle_number=1,
        cycle_result=cycle_one,
        test_results="**Passed Tests**: 1\n**Failed Tests**: 0",
        evaluation_result=None,
    )

    (tmp_path / "README.md").write_text("init\ncycle one\ncycle two\n", encoding="utf-8")
    cycle_two = CycleResult(
        cycle_number=2,
        status="success",
        orientation="focus",
        start_time=datetime.now(),
        final_summary="Cycle two update\nNext focus: Wrap up",
    )
    second_sha = agent._commit_cycle_work(
        cycle_number=2,
        cycle_result=cycle_two,
        test_results="**Passed Tests**: 1\n**Failed Tests**: 0",
        evaluation_result=None,
    )

    assert first_sha
    assert second_sha
    assert first_sha != second_sha
