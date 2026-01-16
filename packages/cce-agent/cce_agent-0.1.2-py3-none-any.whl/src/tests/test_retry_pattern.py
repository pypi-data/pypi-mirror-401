import os
import sys

sys.path.insert(0, os.path.abspath("."))

from src.agent_testing_improvements import (
    build_test_attempt,
    get_max_test_retries,
    should_retry_test_failure,
)


def test_get_max_test_retries_default(monkeypatch):
    monkeypatch.delenv("CCE_MAX_TEST_RETRIES", raising=False)
    assert get_max_test_retries() == 5


def test_get_max_test_retries_invalid(monkeypatch):
    monkeypatch.setenv("CCE_MAX_TEST_RETRIES", "not-a-number")
    assert get_max_test_retries() == 5


def test_get_max_test_retries_minimum(monkeypatch):
    monkeypatch.setenv("CCE_MAX_TEST_RETRIES", "0")
    assert get_max_test_retries() == 1


def test_should_retry_test_failure():
    assert should_retry_test_failure(1, 3, True) is True
    assert should_retry_test_failure(3, 3, True) is False
    assert should_retry_test_failure(1, 3, False) is False


def test_build_test_attempt_records_fields():
    attempt = build_test_attempt(
        test_path="pytest tests/test_retry.py",
        attempt_number=2,
        passed=False,
        failure_reason="AssertionError",
        fix_applied="Adjusted expected output",
    )

    assert attempt.test_path == "pytest tests/test_retry.py"
    assert attempt.attempt_number == 2
    assert attempt.passed is False
    assert attempt.failure_reason == "AssertionError"
    assert attempt.fix_applied == "Adjusted expected output"
    assert attempt.timestamp is not None
