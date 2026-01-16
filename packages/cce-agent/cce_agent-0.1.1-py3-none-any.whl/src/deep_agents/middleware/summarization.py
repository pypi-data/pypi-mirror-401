"""
Summarization middleware helpers for CCE deep agents.
"""

from __future__ import annotations

from typing import Any

from langchain.agents.middleware.summarization import SummarizationMiddleware
from langchain_core.language_models import BaseChatModel


def create_cce_summarization_middleware(model: BaseChatModel) -> SummarizationMiddleware:
    """Create summarization middleware configured for CCE deep agents."""
    if (
        getattr(model, "profile", None) is not None
        and isinstance(model.profile, dict)
        and isinstance(model.profile.get("max_input_tokens"), int)
    ):
        trigger = ("fraction", 0.85)
        keep = ("fraction", 0.10)
    else:
        trigger = ("tokens", 170000)
        keep = ("messages", 6)

    return SummarizationMiddleware(
        model=model,
        trigger=trigger,
        keep=keep,
        trim_tokens_to_summarize=None,
    )
