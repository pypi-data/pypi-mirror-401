"""
Audited Tool Wrapper for Deep Agents

This module provides tool wrappers that automatically audit all tool calls
with comprehensive context tracking for debugging context explosion issues.
"""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, Dict, Optional

from .context_auditor import audit_tool_call, get_global_auditor

logger = logging.getLogger(__name__)


def audited_tool(tool_name: str, workspace_root: str):
    """
    Decorator to wrap a tool function with automatic context auditing.

    Args:
        tool_name: Name of the tool for audit logs
        workspace_root: Root workspace directory for audit logs

    Returns:
        Decorated tool function
    """

    def decorator(tool_func: Callable) -> Callable:
        @wraps(tool_func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            # Capture input
            tool_input = {"args": args, "kwargs": kwargs}

            try:
                # Execute the original tool
                result = tool_func(*args, **kwargs)

                # Calculate execution time
                execution_time = time.time() - start_time

                # Audit the tool call
                audit_metadata = {
                    "tool_function": tool_func.__name__,
                    "tool_module": tool_func.__module__,
                    "args_count": len(args),
                    "kwargs_count": len(kwargs),
                }

                audit_tool_call(
                    tool_name=tool_name,
                    tool_input=tool_input,
                    tool_output=result,
                    execution_time=execution_time,
                    metadata=audit_metadata,
                    workspace_root=workspace_root,
                )

                return result

            except Exception as e:
                # Audit failed tool calls too
                execution_time = time.time() - start_time

                audit_metadata = {
                    "tool_function": tool_func.__name__,
                    "tool_module": tool_func.__module__,
                    "args_count": len(args),
                    "kwargs_count": len(kwargs),
                    "error": str(e),
                    "error_type": type(e).__name__,
                }

                audit_tool_call(
                    tool_name=f"{tool_name}_error",
                    tool_input=tool_input,
                    tool_output=f"ERROR: {e}",
                    execution_time=execution_time,
                    metadata=audit_metadata,
                    workspace_root=workspace_root,
                )

                raise

        return wrapper

    return decorator


class AuditedToolWrapper:
    """
    Wrapper for LangChain tools that automatically audits all tool calls.
    """

    def __init__(self, tool, workspace_root: str):
        """
        Initialize the audited tool wrapper.

        Args:
            tool: The LangChain tool to wrap
            workspace_root: Root workspace directory for audit logs
        """
        self.tool = tool
        self.workspace_root = workspace_root
        self.auditor = get_global_auditor(workspace_root)

        # Get tool name
        self.tool_name = getattr(tool, "name", type(tool).__name__)

        # Copy all attributes from the original tool
        for attr_name in dir(tool):
            if not attr_name.startswith("_") and not hasattr(self, attr_name):
                setattr(self, attr_name, getattr(tool, attr_name))

        logger.info(f"🔍 [AUDITED TOOL WRAPPER] Initialized for tool: {self.tool_name}")

    def __call__(self, *args, **kwargs) -> Any:
        """
        Make the wrapper callable like the original tool.
        """
        return self._run(*args, **kwargs)

    def _run(self, *args, **kwargs) -> Any:
        """
        Run the tool with automatic context auditing.

        Args:
            *args: Positional arguments for the tool
            **kwargs: Keyword arguments for the tool

        Returns:
            Tool result
        """
        start_time = time.time()

        # Capture input
        tool_input = {"args": args, "kwargs": kwargs}

        try:
            # Execute the original tool
            result = self.tool._run(*args, **kwargs)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Audit the tool call
            audit_metadata = {
                "tool_class": type(self.tool).__name__,
                "args_count": len(args),
                "kwargs_count": len(kwargs),
            }

            audit_tool_call(
                tool_name=self.tool_name,
                tool_input=tool_input,
                tool_output=result,
                execution_time=execution_time,
                metadata=audit_metadata,
                workspace_root=self.workspace_root,
            )

            return result

        except Exception as e:
            # Audit failed tool calls too
            execution_time = time.time() - start_time

            audit_metadata = {
                "tool_class": type(self.tool).__name__,
                "args_count": len(args),
                "kwargs_count": len(kwargs),
                "error": str(e),
                "error_type": type(e).__name__,
            }

            audit_tool_call(
                tool_name=f"{self.tool_name}_error",
                tool_input=tool_input,
                tool_output=f"ERROR: {e}",
                execution_time=execution_time,
                metadata=audit_metadata,
                workspace_root=self.workspace_root,
            )

            raise

    async def _arun(self, *args, **kwargs) -> Any:
        """
        Async run the tool with automatic context auditing.

        Args:
            *args: Positional arguments for the tool
            **kwargs: Keyword arguments for the tool

        Returns:
            Tool result
        """
        start_time = time.time()

        # Capture input
        tool_input = {"args": args, "kwargs": kwargs}

        try:
            # Execute the original tool
            result = await self.tool._arun(*args, **kwargs)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Audit the tool call
            audit_metadata = {
                "tool_class": type(self.tool).__name__,
                "args_count": len(args),
                "kwargs_count": len(kwargs),
                "async": True,
            }

            audit_tool_call(
                tool_name=self.tool_name,
                tool_input=tool_input,
                tool_output=result,
                execution_time=execution_time,
                metadata=audit_metadata,
                workspace_root=self.workspace_root,
            )

            return result

        except Exception as e:
            # Audit failed tool calls too
            execution_time = time.time() - start_time

            audit_metadata = {
                "tool_class": type(self.tool).__name__,
                "args_count": len(args),
                "kwargs_count": len(kwargs),
                "async": True,
                "error": str(e),
                "error_type": type(e).__name__,
            }

            audit_tool_call(
                tool_name=f"{self.tool_name}_error",
                tool_input=tool_input,
                tool_output=f"ERROR: {e}",
                execution_time=execution_time,
                metadata=audit_metadata,
                workspace_root=self.workspace_root,
            )

            raise

    def __getattr__(self, name):
        """Delegate attribute access to the wrapped tool."""
        return getattr(self.tool, name)


def wrap_tool_with_auditing(tool, workspace_root: str) -> AuditedToolWrapper:
    """
    Wrap a LangChain tool with automatic context auditing.

    Args:
        tool: The LangChain tool to wrap
        workspace_root: Root workspace directory for audit logs

    Returns:
        Audited tool wrapper
    """
    return AuditedToolWrapper(tool, workspace_root)


def wrap_tools_with_auditing(tools: list, workspace_root: str) -> list:
    """
    Wrap a list of LangChain tools with automatic context auditing.

    Args:
        tools: List of LangChain tools to wrap
        workspace_root: Root workspace directory for audit logs

    Returns:
        List of audited tool wrappers
    """
    return [wrap_tool_with_auditing(tool, workspace_root) for tool in tools]
