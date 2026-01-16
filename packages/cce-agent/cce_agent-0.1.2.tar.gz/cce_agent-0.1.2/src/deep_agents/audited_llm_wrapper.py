"""
Audited LLM Wrapper for Deep Agents

This module provides an LLM wrapper that automatically audits all LLM calls
with comprehensive context tracking for debugging context explosion issues.
"""

import logging
import time
from typing import Any, Dict, List, Optional, Union

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable

from .context_auditor import audit_llm_call, get_global_auditor

logger = logging.getLogger(__name__)


class AuditedLLMWrapper:
    """
    Wrapper around any LLM that automatically audits all calls for context analysis.
    """

    def __init__(self, llm: BaseLanguageModel, workspace_root: str):
        """
        Initialize the audited LLM wrapper.

        Args:
            llm: The underlying LLM to wrap
            workspace_root: Root workspace directory for audit logs
        """
        self._llm = llm
        self.workspace_root = workspace_root
        self.auditor = get_global_auditor(workspace_root)

        # Copy important attributes from the wrapped LLM
        self.model_name = getattr(llm, "model_name", "unknown")
        self.temperature = getattr(llm, "temperature", 0)
        self.max_tokens = getattr(llm, "max_tokens", None)

        logger.info(f"🔍 [AUDITED LLM WRAPPER] Initialized for model: {self.model_name}")

    @property
    def _llm_type(self) -> str:
        """Return type of language model."""
        return f"audited_{getattr(self._llm, '_llm_type', 'unknown')}"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs,
    ) -> Any:
        """Generate a response using the wrapped LLM with auditing."""
        start_time = time.time()

        try:
            # Call the underlying LLM
            response = self._llm._generate(messages, stop=stop, run_manager=run_manager, **kwargs)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Audit the call
            audit_metadata = {
                "execution_time_ms": execution_time * 1000,
                "kwargs": {k: str(v) for k, v in kwargs.items()},
                "method": "_generate",
            }

            audit_llm_call(
                input_messages=messages,
                output_message=response,
                model_name=self.model_name,
                call_type="llm_generate",
                metadata=audit_metadata,
                workspace_root=self.workspace_root,
            )

            return response

        except Exception as e:
            # Audit failed calls too
            execution_time = time.time() - start_time

            audit_metadata = {
                "execution_time_ms": execution_time * 1000,
                "kwargs": {k: str(v) for k, v in kwargs.items()},
                "method": "_generate",
                "error": str(e),
                "error_type": type(e).__name__,
            }

            audit_llm_call(
                input_messages=messages,
                output_message=f"ERROR: {e}",
                model_name=self.model_name,
                call_type="llm_generate_error",
                metadata=audit_metadata,
                workspace_root=self.workspace_root,
            )

            raise

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs,
    ) -> Any:
        """Async generate a response using the wrapped LLM with auditing."""
        start_time = time.time()

        try:
            # Call the underlying LLM
            response = await self._llm._agenerate(messages, stop=stop, run_manager=run_manager, **kwargs)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Audit the call
            audit_metadata = {
                "execution_time_ms": execution_time * 1000,
                "kwargs": {k: str(v) for k, v in kwargs.items()},
                "method": "_agenerate",
            }

            audit_llm_call(
                input_messages=messages,
                output_message=response,
                model_name=self.model_name,
                call_type="llm_agenerate",
                metadata=audit_metadata,
                workspace_root=self.workspace_root,
            )

            return response

        except Exception as e:
            # Audit failed calls too
            execution_time = time.time() - start_time

            audit_metadata = {
                "execution_time_ms": execution_time * 1000,
                "kwargs": {k: str(v) for k, v in kwargs.items()},
                "method": "_agenerate",
                "error": str(e),
                "error_type": type(e).__name__,
            }

            audit_llm_call(
                input_messages=messages,
                output_message=f"ERROR: {e}",
                model_name=self.model_name,
                call_type="llm_agenerate_error",
                metadata=audit_metadata,
                workspace_root=self.workspace_root,
            )

            raise

    def invoke(self, messages: list[BaseMessage], **kwargs) -> BaseMessage:
        """Invoke the LLM with automatic context auditing."""
        return self._llm.invoke(messages, **kwargs)

    async def ainvoke(self, messages: list[BaseMessage], **kwargs) -> BaseMessage:
        """Async invoke the LLM with automatic context auditing."""
        return await self._llm.ainvoke(messages, **kwargs)

    def predict(self, text: str, **kwargs) -> str:
        """Predict text using the wrapped LLM."""
        return self._llm.predict(text, **kwargs)

    async def apredict(self, text: str, **kwargs) -> str:
        """Async predict text using the wrapped LLM."""
        return await self._llm.apredict(text, **kwargs)

    def predict_messages(self, messages: list[BaseMessage], **kwargs) -> BaseMessage:
        """Predict messages using the wrapped LLM."""
        return self._llm.predict_messages(messages, **kwargs)

    async def apredict_messages(self, messages: list[BaseMessage], **kwargs) -> BaseMessage:
        """Async predict messages using the wrapped LLM."""
        return await self._llm.apredict_messages(messages, **kwargs)

    def generate_prompt(self, prompts: list[Any], **kwargs) -> Any:
        """Generate prompt using the wrapped LLM."""
        return self._llm.generate_prompt(prompts, **kwargs)

    async def agenerate_prompt(self, prompts: list[Any], **kwargs) -> Any:
        """Async generate prompt using the wrapped LLM."""
        return await self._llm.agenerate_prompt(prompts, **kwargs)

    def __getattr__(self, name):
        """Delegate attribute access to the wrapped LLM."""
        return getattr(self._llm, name)


def wrap_llm_with_auditing(llm: BaseLanguageModel, workspace_root: str) -> AuditedLLMWrapper:
    """
    Wrap an LLM with automatic context auditing.

    Args:
        llm: The LLM to wrap
        workspace_root: Root workspace directory for audit logs

    Returns:
        Audited LLM wrapper
    """
    return AuditedLLMWrapper(llm, workspace_root)
