import asyncio
import logging
from types import SimpleNamespace

import pytest

from src.agent import CCEAgent


class DummyGitOps:
    def get_modified_files(self):
        return ["src/example.py"]

    def get_changed_files(self, *_args, **_kwargs):
        return ["src/example.py"]


class DummyTestResult:
    def __init__(self, tests_run: int, tests_passed: int, tests_failed: int):
        self.framework = "pytest"
        self.command = ["pytest", "tests/test_example.py"]
        self.selected_tests = ["tests/test_example.py"]
        self.tests_run = tests_run
        self.tests_passed = tests_passed
        self.tests_failed = tests_failed
        self.tests_skipped = 0

    def to_dict(self):
        return {
            "framework": self.framework,
            "command": self.command,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "tests_skipped": self.tests_skipped,
        }


class DummyFrameworkTestManager:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.calls = []

    def run_tests(self, target_files=None, fast_mode=False):
        self.calls.append({"target_files": target_files, "fast_mode": fast_mode})
        if target_files is not None:
            return {"pytest": [DummyTestResult(tests_run=1, tests_passed=0, tests_failed=1)]}
        return {"pytest": [DummyTestResult(tests_run=1, tests_passed=1, tests_failed=0)]}

    def suggest_test_plan(self, target_files=None):
        return "Run pytest"


@pytest.mark.asyncio
async def test_testing_phase_records_fix_applied_on_retry(monkeypatch, tmp_path):
    async def _run_phase():
        agent = SimpleNamespace(
            workspace_root=str(tmp_path),
            logger=logging.getLogger("test"),
            git_ops=DummyGitOps(),
        )
        execution_state = {}
        final_state = {}
        return await CCEAgent._execute_testing_phase(
            agent,
            execution_state,
            final_state,
            "Ticket title",
            "Ticket description",
        )

    monkeypatch.setattr(
        "src.tools.validation.testing.FrameworkTestManager",
        DummyFrameworkTestManager,
    )
    monkeypatch.setattr(
        "src.agent_testing_improvements.SmartTestDiscovery.discover_relevant_tests",
        lambda _self, _files: ["tests/test_example.py"],
    )
    monkeypatch.setattr("src.agent_testing_improvements.get_max_test_retries", lambda _default=5: 2)

    results = await _run_phase()
    assert results["retries"] == 1
    assert results["attempts"]
    assert results["attempts"][1]["fix_applied"] == "expanded from scoped tests to full test suite"
