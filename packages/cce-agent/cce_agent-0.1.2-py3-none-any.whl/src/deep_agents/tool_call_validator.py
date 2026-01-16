"""
Tool Call Validator for Deep Agents

This module provides validation for tool calls to ensure all required parameters
are present before execution, preventing message history corruption.
"""

import logging
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


class ToolCallValidator:
    """Validates tool calls to ensure all required parameters are present."""

    def __init__(self):
        self.tool_requirements = {
            "write_file": {"required": ["file_path", "content"], "optional": ["state"]},
            "hybrid_write_file": {"required": ["file_path", "content"], "optional": ["state"]},
            "edit_file": {
                "required": ["file_path", "old_string", "new_string"],
                "optional": ["state", "replace_all"],
            },
            "hybrid_edit_file": {
                "required": ["file_path", "old_string", "new_string"],
                "optional": ["state", "replace_all"],
            },
            "execute_bash_command": {"required": ["command"], "optional": ["timeout"]},
        }

    def validate_tool_call(self, tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
        """
        Validate a tool call to ensure all required parameters are present.

        Args:
            tool_name: Name of the tool
            tool_args: Arguments passed to the tool

        Returns:
            Validation result with success status and error message if failed
        """
        if tool_name not in self.tool_requirements:
            return {
                "valid": True,  # Unknown tools pass validation
                "error": None,
            }

        requirements = self.tool_requirements[tool_name]
        missing_params = []

        # Check required parameters
        for param in requirements["required"]:
            if param not in tool_args:
                missing_params.append(param)

        if missing_params:
            error_msg = f"""⚠️ Tool call validation failed for {tool_name}

Missing required parameters: {", ".join(missing_params)}

Please provide all required parameters:
- {tool_name}({", ".join(requirements["required"])})"""

            return {"valid": False, "error": error_msg, "missing_parameters": missing_params}

        return {"valid": True, "error": None}

    def validate_and_fix_tool_calls(self, messages: list[Any]) -> list[Any]:
        """
        Validate all tool calls in messages and fix any that are invalid.

        Args:
            messages: List of messages from the conversation

        Returns:
            Updated list of messages with validation fixes
        """
        updated_messages = []

        for message in messages:
            if isinstance(message, AIMessage) and hasattr(message, "tool_calls") and message.tool_calls:
                # Validate each tool call
                valid_tool_calls = []
                tool_messages = []

                for tool_call in message.tool_calls:
                    tool_name = tool_call.get("name", "")
                    tool_args = tool_call.get("args", {})

                    validation_result = self.validate_tool_call(tool_name, tool_args)

                    if validation_result["valid"]:
                        valid_tool_calls.append(tool_call)
                    else:
                        # Create a ToolMessage for the failed validation
                        tool_message = ToolMessage(
                            content=validation_result["error"], tool_call_id=tool_call.get("id", "unknown")
                        )
                        tool_messages.append(tool_message)
                        logger.warning(f"Tool call validation failed for {tool_name}: {validation_result['error']}")

                # Update the message with only valid tool calls
                if valid_tool_calls:
                    updated_message = AIMessage(
                        content=message.content,
                        tool_calls=valid_tool_calls,
                        additional_kwargs=message.additional_kwargs,
                    )
                    updated_messages.append(updated_message)

                # Add any validation error messages
                updated_messages.extend(tool_messages)
            else:
                updated_messages.append(message)

        return updated_messages


def create_tool_call_validator() -> ToolCallValidator:
    """Create a new tool call validator instance."""
    return ToolCallValidator()
