"""
Context Auditor for Deep Agents

This module provides comprehensive context auditing to track context size
at every step of deep agent execution, including LLM calls, post-hooks,
and tool calls. This helps identify where context explosion occurs.
"""

import hashlib
import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class ContextAuditor:
    """
    Comprehensive context auditor that logs input/output context sizes
    for every LLM call, post-hook execution, and tool call.
    """

    def __init__(
        self,
        workspace_root: str,
        session_id: str | None = None,
        default_include_content: bool = False,
        max_content_size: int = 10000,
        compress_large_content: bool = True,
    ):
        """
        Initialize the context auditor.

        Args:
            workspace_root: Root workspace directory
            session_id: Optional session ID for grouping logs
            default_include_content: Whether to include full content by default
            max_content_size: Maximum size (chars) for content before compression
            compress_large_content: Whether to compress/summarize large content
        """
        self.workspace_root = Path(workspace_root)
        self.session_id = session_id or f"session_{int(time.time())}"
        self.audit_dir = self.workspace_root / ".artifacts" / "context_audit" / self.session_id
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        # Content filtering settings
        self.default_include_content = default_include_content
        self.max_content_size = max_content_size
        self.compress_large_content = compress_large_content

        # Counter for unique IDs
        self.call_counter = 0
        self.llm_call_counter = 0
        self.hook_call_counter = 0
        self.tool_call_counter = 0

        # Context tracking
        self.context_history: list[dict[str, Any]] = []

        logger.info(f"🔍 [CONTEXT AUDITOR] Initialized for session: {self.session_id}")
        logger.info(f"   📁 Audit directory: {self.audit_dir}")
        logger.info(f"   📝 Content inclusion: {self.default_include_content}")
        logger.info(f"   📏 Max content size: {self.max_content_size} chars")

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()

    def _filter_content(self, content: Any, content_type: str = "unknown") -> Any:
        """
        Filter and compress content based on size and settings.

        Args:
            content: Content to filter
            content_type: Type of content for logging

        Returns:
            Filtered content
        """
        if not self.compress_large_content:
            return content

        # Convert to string for size checking
        if hasattr(content, "content") and hasattr(content, "type"):
            # LangChain message object
            content_str = str(content.content) if content.content else ""
        elif isinstance(content, (dict, list)):
            try:
                content_str = json.dumps(content, indent=2, default=str)
            except (TypeError, ValueError):
                content_str = str(content)
        else:
            content_str = str(content)

        # Check if content is too large
        if len(content_str) > self.max_content_size:
            # Create a summary instead of full content
            summary = {
                "_content_type": content_type,
                "_original_size": len(content_str),
                "_truncated": True,
                "_summary": content_str[: self.max_content_size] + "... [TRUNCATED]",
                "_first_100_chars": content_str[:100] if content_str else "",
                "_last_100_chars": content_str[-100:] if len(content_str) > 100 else "",
                "_line_count": content_str.count("\n") + 1 if content_str else 0,
            }

            # Calculate compression ratio after creating summary
            summary_str = str(summary)
            summary["_compression_ratio"] = round(len(summary_str) / len(content_str), 3)

            logger.debug(
                f"🔍 [CONTEXT AUDITOR] Content filtered: {content_type} "
                f"({len(content_str)} -> {len(summary_str)} chars, "
                f"compression: {summary['_compression_ratio']:.1%})"
            )
            return summary

        return content

    def _filter_messages(self, messages: list[Any]) -> list[Any]:
        """
        Filter a list of messages, applying size limits to each.

        Args:
            messages: List of messages to filter

        Returns:
            Filtered list of messages
        """
        if not messages:
            return messages

        filtered_messages = []
        for i, message in enumerate(messages):
            filtered_msg = self._filter_content(message, f"message_{i}")
            filtered_messages.append(filtered_msg)

        return filtered_messages

    def _filter_state(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Filter a state dictionary, applying size limits to large fields.

        Args:
            state: State dictionary to filter

        Returns:
            Filtered state dictionary
        """
        if not state:
            return state

        filtered_state = {}
        for field_name, field_value in state.items():
            # Always include small fields, filter large ones
            field_str = str(field_value)
            if len(field_str) > self.max_content_size:
                filtered_state[field_name] = self._filter_content(field_value, f"state_field_{field_name}")
            else:
                filtered_state[field_name] = field_value

        return filtered_state

    def _calculate_context_size(self, content: Any) -> dict[str, int]:
        """
        Calculate context size metrics for given content.

        Args:
            content: Content to analyze (string, dict, list, etc.)

        Returns:
            Dictionary with size metrics
        """
        if content is None:
            return {"characters": 0, "tokens_estimate": 0, "type": "None"}

        # Handle LangChain message objects
        if hasattr(content, "content") and hasattr(content, "type"):
            # This is likely a LangChain message object
            content_str = str(content.content) if content.content else ""
            content_type = f"LangChain_{type(content).__name__}"
        elif isinstance(content, (dict, list)):
            # Try to serialize, but handle non-serializable objects
            try:
                content_str = json.dumps(content, indent=2, default=str)
            except (TypeError, ValueError):
                # Fallback to string representation
                content_str = str(content)
            content_type = type(content).__name__
        else:
            content_str = str(content)
            content_type = type(content).__name__

        # Basic metrics
        char_count = len(content_str)

        # Rough token estimate (4 chars per token average)
        token_estimate = char_count // 4

        return {
            "characters": char_count,
            "tokens_estimate": token_estimate,
            "type": content_type,
            "lines": content_str.count("\n") + 1 if content_str else 0,
        }

    def _write_audit_file(self, filename: str, data: dict[str, Any]) -> str:
        """
        Write audit data to a file.

        Args:
            filename: Name of the audit file
            data: Data to write

        Returns:
            Path to the written file
        """
        file_path = self.audit_dir / filename

        # Custom JSON encoder to handle non-serializable objects
        def json_serializer(obj):
            """Custom JSON serializer for non-serializable objects."""
            if hasattr(obj, "content") and hasattr(obj, "type"):
                # LangChain message object
                return {
                    "type": type(obj).__name__,
                    "content": str(obj.content) if obj.content else "",
                    "additional_kwargs": getattr(obj, "additional_kwargs", {}),
                }
            elif hasattr(obj, "__dict__"):
                # Generic object with attributes
                return {
                    "type": type(obj).__name__,
                    "attributes": {k: v for k, v in obj.__dict__.items() if not k.startswith("_")},
                }
            else:
                return str(obj)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=json_serializer)
        return str(file_path)

    def audit_llm_call(
        self,
        input_messages: list[Any],
        output_message: Any,
        model_name: str,
        call_type: str = "llm_call",
        metadata: dict[str, Any] | None = None,
        include_input_content: bool | None = None,
    ) -> str:
        """
        Audit an LLM call with input/output context analysis.

        Args:
            input_messages: Input messages to the LLM
            output_message: Output message from the LLM
            model_name: Name of the LLM model
            call_type: Type of call (e.g., "llm_call", "sub_agent_call")
            metadata: Additional metadata
            include_input_content: Whether to include full content (None = use default)

        Returns:
            Path to the audit file
        """
        self.llm_call_counter += 1
        self.call_counter += 1

        # Use default if not specified
        if include_input_content is None:
            include_input_content = self.default_include_content

        # Analyze input context
        input_analysis = self._analyze_messages(input_messages)

        # Analyze output context
        output_analysis = self._calculate_context_size(output_message)

        # Create audit record
        audit_data = {
            "audit_type": "llm_call",
            "call_id": f"llm_{self.llm_call_counter:04d}",
            "global_call_id": f"call_{self.call_counter:04d}",
            "timestamp": self._get_timestamp(),
            "model_name": model_name,
            "call_type": call_type,
            "input_analysis": input_analysis,
            "output_analysis": output_analysis,
            "metadata": metadata or {},
            "context_delta": {
                "input_tokens": input_analysis["total_tokens"],
                "output_tokens": output_analysis["tokens_estimate"],
                "net_change": output_analysis["tokens_estimate"] - input_analysis["total_tokens"],
            },
        }

        # Include actual input content if requested (with filtering)
        if include_input_content:
            audit_data["input_content"] = {
                "messages": self._filter_messages(input_messages),
                "message_count": len(input_messages),
            }
            audit_data["output_content"] = self._filter_content(output_message, "llm_output")

        # Add to history
        self.context_history.append(audit_data)

        # Write audit file
        filename = f"llm_call_{self.llm_call_counter:04d}_{int(time.time())}.json"
        file_path = self._write_audit_file(filename, audit_data)

        logger.info(f"🔍 [CONTEXT AUDITOR] LLM call audited: {audit_data['call_id']}")
        logger.info(f"   📊 Input: {input_analysis['total_tokens']} tokens, {input_analysis['message_count']} messages")
        logger.info(f"   📤 Output: {output_analysis['tokens_estimate']} tokens")
        logger.info(f"   📁 Audit file: {filename}")

        return file_path

    def audit_post_hook(
        self,
        hook_name: str,
        input_state: dict[str, Any],
        output_state: dict[str, Any],
        execution_time: float,
        metadata: dict[str, Any] | None = None,
        include_input_content: bool | None = None,
    ) -> str:
        """
        Audit a post-hook execution with input/output state analysis.

        Args:
            hook_name: Name of the post-hook
            input_state: Input state to the hook
            output_state: Output state from the hook
            execution_time: Time taken to execute the hook
            metadata: Additional metadata
            include_input_content: Whether to include full content (None = use default)

        Returns:
            Path to the audit file
        """
        self.hook_call_counter += 1
        self.call_counter += 1

        # Use default if not specified
        if include_input_content is None:
            include_input_content = self.default_include_content

        # Analyze input state
        input_analysis = self._analyze_state(input_state)

        # Analyze output state
        output_analysis = self._analyze_state(output_state)

        # Create audit record
        audit_data = {
            "audit_type": "post_hook",
            "call_id": f"hook_{self.hook_call_counter:04d}",
            "global_call_id": f"call_{self.call_counter:04d}",
            "timestamp": self._get_timestamp(),
            "hook_name": hook_name,
            "execution_time_ms": execution_time * 1000,
            "input_analysis": input_analysis,
            "output_analysis": output_analysis,
            "metadata": metadata or {},
            "context_delta": {
                "input_tokens": input_analysis["total_tokens"],
                "output_tokens": output_analysis["total_tokens"],
                "net_change": output_analysis["total_tokens"] - input_analysis["total_tokens"],
            },
        }

        # Include actual input/output content if requested (with filtering)
        if include_input_content:
            audit_data["input_content"] = self._filter_state(input_state)
            audit_data["output_content"] = self._filter_state(output_state)

        # Add to history
        self.context_history.append(audit_data)

        # Write audit file
        filename = f"post_hook_{self.hook_call_counter:04d}_{int(time.time())}.json"
        file_path = self._write_audit_file(filename, audit_data)

        logger.info(f"🔍 [CONTEXT AUDITOR] Post-hook audited: {audit_data['call_id']}")
        logger.info(f"   🪝 Hook: {hook_name}")
        logger.info(f"   📊 Input: {input_analysis['total_tokens']} tokens")
        logger.info(f"   📤 Output: {output_analysis['total_tokens']} tokens")
        logger.info(f"   ⏱️  Time: {execution_time * 1000:.1f}ms")
        logger.info(f"   📁 Audit file: {filename}")

        return file_path

    def audit_tool_call(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        tool_output: Any,
        execution_time: float,
        metadata: dict[str, Any] | None = None,
        include_input_content: bool | None = None,
    ) -> str:
        """
        Audit a tool call with input/output analysis.

        Args:
            tool_name: Name of the tool
            tool_input: Input to the tool
            tool_output: Output from the tool
            execution_time: Time taken to execute the tool
            metadata: Additional metadata
            include_input_content: Whether to include full content (None = use default)

        Returns:
            Path to the audit file
        """
        self.tool_call_counter += 1
        self.call_counter += 1

        # Use default if not specified
        if include_input_content is None:
            include_input_content = self.default_include_content

        # Analyze input
        input_analysis = self._calculate_context_size(tool_input)

        # Analyze output
        output_analysis = self._calculate_context_size(tool_output)

        # Create audit record
        audit_data = {
            "audit_type": "tool_call",
            "call_id": f"tool_{self.tool_call_counter:04d}",
            "global_call_id": f"call_{self.call_counter:04d}",
            "timestamp": self._get_timestamp(),
            "tool_name": tool_name,
            "execution_time_ms": execution_time * 1000,
            "input_analysis": input_analysis,
            "output_analysis": output_analysis,
            "metadata": metadata or {},
            "context_delta": {
                "input_tokens": input_analysis["tokens_estimate"],
                "output_tokens": output_analysis["tokens_estimate"],
                "net_change": output_analysis["tokens_estimate"] - input_analysis["tokens_estimate"],
            },
        }

        # Include actual input/output content if requested (with filtering)
        if include_input_content:
            audit_data["input_content"] = self._filter_content(tool_input, f"tool_input_{tool_name}")
            audit_data["output_content"] = self._filter_content(tool_output, f"tool_output_{tool_name}")

        # Add to history
        self.context_history.append(audit_data)

        # Write audit file
        filename = f"tool_call_{self.tool_call_counter:04d}_{int(time.time())}.json"
        file_path = self._write_audit_file(filename, audit_data)

        logger.info(f"🔍 [CONTEXT AUDITOR] Tool call audited: {audit_data['call_id']}")
        logger.info(f"   🔧 Tool: {tool_name}")
        logger.info(f"   📊 Input: {input_analysis['tokens_estimate']} tokens")
        logger.info(f"   📤 Output: {output_analysis['tokens_estimate']} tokens")
        logger.info(f"   ⏱️  Time: {execution_time * 1000:.1f}ms")
        logger.info(f"   📁 Audit file: {filename}")

        return file_path

    def _analyze_messages(self, messages: list[Any]) -> dict[str, Any]:
        """
        Analyze a list of messages for context metrics.

        Args:
            messages: List of messages to analyze

        Returns:
            Analysis dictionary
        """
        if not messages:
            return {
                "message_count": 0,
                "total_tokens": 0,
                "total_characters": 0,
                "message_types": {},
                "largest_message": {"size": 0, "type": "None"},
            }

        total_tokens = 0
        total_characters = 0
        message_types = {}
        largest_message = {"size": 0, "type": "None", "index": -1}

        for i, message in enumerate(messages):
            # Get message type
            msg_type = type(message).__name__
            message_types[msg_type] = message_types.get(msg_type, 0) + 1

            # Calculate size
            size_metrics = self._calculate_context_size(message)
            total_tokens += size_metrics["tokens_estimate"]
            total_characters += size_metrics["characters"]

            # Track largest message
            if size_metrics["tokens_estimate"] > largest_message["size"]:
                largest_message = {"size": size_metrics["tokens_estimate"], "type": msg_type, "index": i}

        return {
            "message_count": len(messages),
            "total_tokens": total_tokens,
            "total_characters": total_characters,
            "message_types": message_types,
            "largest_message": largest_message,
        }

    def _analyze_state(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Analyze a state dictionary for context metrics.

        Args:
            state: State dictionary to analyze

        Returns:
            Analysis dictionary
        """
        if not state:
            return {
                "total_tokens": 0,
                "total_characters": 0,
                "field_count": 0,
                "largest_field": {"name": "None", "size": 0},
            }

        total_tokens = 0
        total_characters = 0
        largest_field = {"name": "None", "size": 0}

        for field_name, field_value in state.items():
            size_metrics = self._calculate_context_size(field_value)
            total_tokens += size_metrics["tokens_estimate"]
            total_characters += size_metrics["characters"]

            # Track largest field
            if size_metrics["tokens_estimate"] > largest_field["size"]:
                largest_field = {"name": field_name, "size": size_metrics["tokens_estimate"]}

        return {
            "total_tokens": total_tokens,
            "total_characters": total_characters,
            "field_count": len(state),
            "largest_field": largest_field,
        }

    def generate_summary_report(self) -> str:
        """
        Generate a summary report of all audited calls.

        Returns:
            Path to the summary report file
        """
        # Calculate summary statistics
        total_llm_calls = self.llm_call_counter
        total_hook_calls = self.hook_call_counter
        total_tool_calls = self.tool_call_counter
        total_calls = self.call_counter

        # Calculate token usage
        total_input_tokens = sum(call.get("context_delta", {}).get("input_tokens", 0) for call in self.context_history)
        total_output_tokens = sum(
            call.get("context_delta", {}).get("output_tokens", 0) for call in self.context_history
        )
        net_token_change = total_output_tokens - total_input_tokens

        # Find largest calls
        largest_llm_call = max(
            [call for call in self.context_history if call["audit_type"] == "llm_call"],
            key=lambda x: x.get("context_delta", {}).get("input_tokens", 0),
            default=None,
        )

        largest_hook_call = max(
            [call for call in self.context_history if call["audit_type"] == "post_hook"],
            key=lambda x: x.get("context_delta", {}).get("input_tokens", 0),
            default=None,
        )

        largest_tool_call = max(
            [call for call in self.context_history if call["audit_type"] == "tool_call"],
            key=lambda x: x.get("context_delta", {}).get("input_tokens", 0),
            default=None,
        )

        # Create summary report
        summary_data = {
            "session_id": self.session_id,
            "timestamp": self._get_timestamp(),
            "summary": {
                "total_calls": total_calls,
                "llm_calls": total_llm_calls,
                "hook_calls": total_hook_calls,
                "tool_calls": total_tool_calls,
            },
            "token_usage": {
                "total_input_tokens": total_input_tokens,
                "total_output_tokens": total_output_tokens,
                "net_token_change": net_token_change,
                "average_input_tokens_per_call": total_input_tokens / total_calls if total_calls > 0 else 0,
                "average_output_tokens_per_call": total_output_tokens / total_calls if total_calls > 0 else 0,
            },
            "largest_calls": {
                "llm_call": largest_llm_call,
                "hook_call": largest_hook_call,
                "tool_call": largest_tool_call,
            },
            "context_history": self.context_history,
        }

        # Write summary report
        filename = f"context_audit_summary_{int(time.time())}.json"
        file_path = self._write_audit_file(filename, summary_data)

        logger.info(f"📊 [CONTEXT AUDITOR] Summary report generated")
        logger.info(
            f"   📈 Total calls: {total_calls} (LLM: {total_llm_calls}, Hooks: {total_hook_calls}, Tools: {total_tool_calls})"
        )
        logger.info(f"   🧮 Total tokens: {total_input_tokens} input, {total_output_tokens} output")
        logger.info(f"   📁 Summary file: {filename}")

        return file_path

    @classmethod
    def create_lightweight_auditor(cls, workspace_root: str, session_id: str | None = None) -> "ContextAuditor":
        """
        Create a lightweight auditor optimized for production use.

        This auditor:
        - Excludes content by default (only stores metrics)
        - Uses aggressive compression for any included content
        - Has a small max content size for summaries

        Args:
            workspace_root: Root workspace directory
            session_id: Optional session ID for grouping logs

        Returns:
            Lightweight ContextAuditor instance
        """
        return cls(
            workspace_root=workspace_root,
            session_id=session_id,
            default_include_content=False,
            max_content_size=5000,  # Smaller limit for summaries
            compress_large_content=True,
        )

    @classmethod
    def create_debug_auditor(cls, workspace_root: str, session_id: str | None = None) -> "ContextAuditor":
        """
        Create a debug auditor that includes more content for debugging.

        This auditor:
        - Includes content by default
        - Uses moderate compression
        - Has a larger max content size

        Args:
            workspace_root: Root workspace directory
            session_id: Optional session ID for grouping logs

        Returns:
            Debug ContextAuditor instance
        """
        return cls(
            workspace_root=workspace_root,
            session_id=session_id,
            default_include_content=True,
            max_content_size=20000,  # Larger limit for debugging
            compress_large_content=True,
        )


# Global auditor instance
_global_auditor: ContextAuditor | None = None


def get_global_auditor(
    workspace_root: str,
    default_include_content: bool = False,
    max_content_size: int = 10000,
    compress_large_content: bool = True,
) -> ContextAuditor:
    """Get or create the global context auditor instance."""
    global _global_auditor
    if _global_auditor is None:
        _global_auditor = ContextAuditor(
            workspace_root,
            default_include_content=default_include_content,
            max_content_size=max_content_size,
            compress_large_content=compress_large_content,
        )
    return _global_auditor


def audit_llm_call(
    input_messages: list[Any],
    output_message: Any,
    model_name: str,
    call_type: str = "llm_call",
    metadata: dict[str, Any] | None = None,
    workspace_root: str | None = None,
    include_input_content: bool | None = None,
) -> str:
    """Convenience function to audit an LLM call."""
    if workspace_root:
        auditor = ContextAuditor(workspace_root)
    else:
        auditor = get_global_auditor(".")
    return auditor.audit_llm_call(
        input_messages, output_message, model_name, call_type, metadata, include_input_content
    )


def audit_post_hook(
    hook_name: str,
    input_state: dict[str, Any],
    output_state: dict[str, Any],
    execution_time: float,
    metadata: dict[str, Any] | None = None,
    workspace_root: str | None = None,
    include_input_content: bool | None = None,
) -> str:
    """Convenience function to audit a post-hook."""
    if workspace_root:
        auditor = ContextAuditor(workspace_root)
    else:
        auditor = get_global_auditor(".")
    return auditor.audit_post_hook(
        hook_name, input_state, output_state, execution_time, metadata, include_input_content
    )


def audit_tool_call(
    tool_name: str,
    tool_input: dict[str, Any],
    tool_output: Any,
    execution_time: float,
    metadata: dict[str, Any] | None = None,
    workspace_root: str | None = None,
    include_input_content: bool | None = None,
) -> str:
    """Convenience function to audit a tool call."""
    if workspace_root:
        auditor = ContextAuditor(workspace_root)
    else:
        auditor = get_global_auditor(".")
    return auditor.audit_tool_call(tool_name, tool_input, tool_output, execution_time, metadata, include_input_content)
