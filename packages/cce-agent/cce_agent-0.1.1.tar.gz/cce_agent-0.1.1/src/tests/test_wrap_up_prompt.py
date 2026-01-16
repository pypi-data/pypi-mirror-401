import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath("."))

from langchain_core.messages import SystemMessage

from src.prompts.wrap_up_prompt import build_wrap_up_message, format_wrap_up_prompt


def test_wrap_up_prompt_includes_counts():
    prompt = format_wrap_up_prompt(step_count=25, soft_limit=20, previous_cycles=None)

    assert "25" in prompt
    assert "20" in prompt


def test_wrap_up_prompt_no_previous_cycles():
    prompt = format_wrap_up_prompt(step_count=20, soft_limit=20, previous_cycles=None)

    assert "No previous cycles" in prompt


def test_wrap_up_prompt_formats_previous_cycles():
    cycles = [
        SimpleNamespace(
            cycle_number=1,
            step_count=10,
            steps_in_main_phase=8,
            steps_in_wrap_up_phase=2,
        )
    ]

    prompt = format_wrap_up_prompt(step_count=12, soft_limit=10, previous_cycles=cycles)

    assert "Cycle 1" in prompt
    assert "main: 8" in prompt


def test_wrap_up_prompt_template_override(tmp_path, monkeypatch):
    template_path = tmp_path / "wrap_up.txt"
    template_path.write_text(
        "CUSTOM {step_count} {soft_limit}\n{previous_cycle_stats}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CCE_WRAP_UP_PROMPT_PATH", str(template_path))

    prompt = format_wrap_up_prompt(step_count=3, soft_limit=7, previous_cycles=None)

    assert "CUSTOM 3 7" in prompt
    assert "No previous cycles" in prompt


def test_build_wrap_up_message_returns_system_message():
    message = build_wrap_up_message(step_count=5, soft_limit=10, previous_cycles=None)

    assert isinstance(message, SystemMessage)
    assert "SOFT LIMIT REACHED" in message.content
