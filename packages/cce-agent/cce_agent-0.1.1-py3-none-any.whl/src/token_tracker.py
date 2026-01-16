"""
Token usage tracking for CCE Agent.

Instruments OpenAI LLM calls to capture detailed token usage
with minimal performance overhead.
"""

import logging
from datetime import datetime
from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.language_models.llms import LLMResult
from langchain_core.messages import BaseMessage

from src.models import TokenUsage


class TokenTrackingCallback(BaseCallbackHandler):
    """
    LangChain callback handler to track token usage from OpenAI calls.
    """

    def __init__(self, model_name: str = "unknown"):
        self.token_usage_records: list[TokenUsage] = []
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Called when LLM ends running."""
        if response.llm_output and "token_usage" in response.llm_output:
            token_data = response.llm_output["token_usage"]

            # Use the model name from initialization
            model = self.model_name

            token_usage = TokenUsage(
                prompt_tokens=token_data.get("prompt_tokens", 0),
                completion_tokens=token_data.get("completion_tokens", 0),
                total_tokens=token_data.get("total_tokens", 0),
                model_name=model,
                operation="llm_call",
                timestamp=datetime.now(),
            )

            self.token_usage_records.append(token_usage)

            self.logger.debug(f"Token usage recorded: {token_usage.total_tokens} tokens ({model})")

    def get_usage_records(self) -> list[TokenUsage]:
        """Get all recorded token usage."""
        return self.token_usage_records.copy()

    def clear_records(self) -> None:
        """Clear all recorded token usage."""
        self.token_usage_records.clear()

    def get_total_tokens(self) -> int:
        """Get total tokens across all recorded usage."""
        return sum(record.total_tokens for record in self.token_usage_records)


class TokenTrackingLLM:
    """
    Wrapper around LLM that provides token usage tracking.
    """

    def __init__(self, model: str = "claude-sonnet-4-20250514", temperature: float = 0):
        """
        Initialize the token tracking LLM.

        Args:
            model: Model name to use (automatically selects provider)
            temperature: Temperature for generation
        """
        self.callback_handler = TokenTrackingCallback(model_name=model)

        # Automatically choose the correct LLM provider based on model name
        if model.startswith("gpt-"):
            # Use OpenAI for GPT models
            from langchain_openai import ChatOpenAI

            self.llm = ChatOpenAI(model=model, temperature=temperature, callbacks=[self.callback_handler])
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Using OpenAI ChatOpenAI with model: {model}")
        else:
            # Use Anthropic for Claude models
            self.llm = ChatAnthropic(model=model, temperature=temperature, callbacks=[self.callback_handler])
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Using Anthropic ChatAnthropic with model: {model}")

        self.model = model

    def invoke(self, messages: list[BaseMessage], **kwargs) -> Any:
        """
        Invoke the LLM and track token usage.

        Args:
            messages: Messages to send to the LLM
            **kwargs: Additional arguments for the LLM

        Returns:
            LLM response
        """
        return self.llm.invoke(messages, **kwargs)

    async def ainvoke(self, messages: list[BaseMessage], **kwargs) -> Any:
        """
        Async invoke the LLM and track token usage.

        Args:
            messages: Messages to send to the LLM
            **kwargs: Additional arguments for the LLM

        Returns:
            LLM response
        """
        return await self.llm.ainvoke(messages, **kwargs)

    def bind_tools(self, tools: list[Any]) -> Any:
        """
        Bind tools to the LLM.

        Args:
            tools: Tools to bind

        Returns:
            LLM with bound tools
        """
        return self.llm.bind_tools(tools)

    def with_structured_output(self, schema: Any, **kwargs) -> Any:
        """
        Create a structured output version of the LLM.

        Args:
            schema: The schema to use for structured output
            **kwargs: Additional arguments

        Returns:
            LLM configured for structured output
        """
        return self.llm.with_structured_output(schema, **kwargs)

    def get_usage_records(self) -> list[TokenUsage]:
        """Get all recorded token usage."""
        return self.callback_handler.get_usage_records()

    def clear_usage_records(self) -> None:
        """Clear all recorded token usage."""
        self.callback_handler.clear_records()

    def get_total_tokens(self) -> int:
        """Get total tokens used since last clear."""
        return self.callback_handler.get_total_tokens()

    def get_usage_summary(self) -> dict[str, Any]:
        """
        Get a summary of token usage.

        Returns:
            Dictionary with usage statistics
        """
        records = self.get_usage_records()

        if not records:
            return {"total_calls": 0, "total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0, "models": []}

        total_tokens = sum(r.total_tokens for r in records)
        prompt_tokens = sum(r.prompt_tokens for r in records)
        completion_tokens = sum(r.completion_tokens for r in records)
        models = list(set(r.model for r in records))

        return {
            "total_calls": len(records),
            "total_tokens": total_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "models": models,
            "average_tokens_per_call": total_tokens / len(records) if records else 0,
        }


def create_token_tracking_llm(model: str = "claude-sonnet-4-20250514", temperature: float = 0) -> TokenTrackingLLM:
    """
    Factory function to create a token tracking LLM.

    Args:
        model: OpenAI model to use
        temperature: Temperature for generation

    Returns:
        TokenTrackingLLM instance
    """
    return TokenTrackingLLM(model=model, temperature=temperature)
