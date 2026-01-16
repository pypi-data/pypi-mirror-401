"""
Audited Post-Hook Wrapper for Deep Agents

This module provides a post-hook wrapper that automatically audits all post-hook
executions with comprehensive context tracking for debugging context explosion issues.
"""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, Dict

from .context_auditor import audit_post_hook, get_global_auditor

logger = logging.getLogger(__name__)


def audited_post_hook(hook_name: str, workspace_root: str):
    """
    Decorator to wrap a post-hook function with automatic context auditing.

    Args:
        hook_name: Name of the post-hook for audit logs
        workspace_root: Root workspace directory for audit logs

    Returns:
        Decorated post-hook function
    """

    def decorator(hook_func: Callable) -> Callable:
        @wraps(hook_func)
        def wrapper(state: dict[str, Any]) -> dict[str, Any]:
            start_time = time.time()

            # Capture input state
            input_state = state.copy()

            try:
                # Execute the original hook
                output_state = hook_func(state)

                # Calculate execution time
                execution_time = time.time() - start_time

                # Audit the hook execution
                audit_metadata = {"hook_function": hook_func.__name__, "hook_module": hook_func.__module__}

                audit_post_hook(
                    hook_name=hook_name,
                    input_state=input_state,
                    output_state=output_state,
                    execution_time=execution_time,
                    metadata=audit_metadata,
                    workspace_root=workspace_root,
                )

                return output_state

            except Exception as e:
                # Audit failed hook executions too
                execution_time = time.time() - start_time

                audit_metadata = {
                    "hook_function": hook_func.__name__,
                    "hook_module": hook_func.__module__,
                    "error": str(e),
                    "error_type": type(e).__name__,
                }

                # Create error state
                error_state = input_state.copy()
                error_state["_hook_error"] = {"error": str(e), "error_type": type(e).__name__, "hook_name": hook_name}

                audit_post_hook(
                    hook_name=f"{hook_name}_error",
                    input_state=input_state,
                    output_state=error_state,
                    execution_time=execution_time,
                    metadata=audit_metadata,
                    workspace_root=workspace_root,
                )

                raise

        return wrapper

    return decorator


class AuditedPostHookManager:
    """
    Manager for creating audited post-hooks with comprehensive context tracking.
    """

    def __init__(self, workspace_root: str):
        """
        Initialize the audited post-hook manager.

        Args:
            workspace_root: Root workspace directory for audit logs
        """
        self.workspace_root = workspace_root
        self.auditor = get_global_auditor(workspace_root)

        logger.info(f"🔍 [AUDITED POST HOOK MANAGER] Initialized for workspace: {workspace_root}")

    def create_audited_hook(self, hook_name: str, hook_func: Callable) -> Callable:
        """
        Create an audited post-hook from a function.

        Args:
            hook_name: Name of the post-hook for audit logs
            hook_func: The post-hook function to wrap

        Returns:
            Audited post-hook function
        """
        return audited_post_hook(hook_name, self.workspace_root)(hook_func)

    def create_combined_audited_hook(self, hook_name: str, *hook_functions: Callable) -> Callable:
        """
        Create a combined audited post-hook from multiple functions.

        Args:
            hook_name: Name of the combined post-hook for audit logs
            *hook_functions: Post-hook functions to combine

        Returns:
            Combined audited post-hook function
        """

        def combined_hook(state: dict[str, Any]) -> dict[str, Any]:
            start_time = time.time()
            input_state = state.copy()
            current_state = state

            hook_results = []

            try:
                # Execute each hook in sequence
                for i, hook_func in enumerate(hook_functions):
                    hook_start_time = time.time()

                    # Execute the hook
                    current_state = hook_func(current_state)

                    # Calculate execution time for this hook
                    hook_execution_time = time.time() - hook_start_time

                    # Record hook result
                    hook_results.append(
                        {
                            "hook_index": i,
                            "hook_name": getattr(hook_func, "__name__", f"hook_{i}"),
                            "execution_time_ms": hook_execution_time * 1000,
                            "success": True,
                        }
                    )

                # Calculate total execution time
                total_execution_time = time.time() - start_time

                # Audit the combined hook execution
                audit_metadata = {
                    "hook_count": len(hook_functions),
                    "hook_results": hook_results,
                    "combined_hook": True,
                }

                audit_post_hook(
                    hook_name=hook_name,
                    input_state=input_state,
                    output_state=current_state,
                    execution_time=total_execution_time,
                    metadata=audit_metadata,
                    workspace_root=self.workspace_root,
                )

                return current_state

            except Exception as e:
                # Audit failed combined hook execution
                total_execution_time = time.time() - start_time

                # Find which hook failed
                failed_hook_index = len(hook_results)

                audit_metadata = {
                    "hook_count": len(hook_functions),
                    "hook_results": hook_results,
                    "failed_hook_index": failed_hook_index,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "combined_hook": True,
                }

                # Create error state
                error_state = input_state.copy()
                error_state["_combined_hook_error"] = {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "hook_name": hook_name,
                    "failed_hook_index": failed_hook_index,
                }

                audit_post_hook(
                    hook_name=f"{hook_name}_error",
                    input_state=input_state,
                    output_state=error_state,
                    execution_time=total_execution_time,
                    metadata=audit_metadata,
                    workspace_root=self.workspace_root,
                )

                raise

        return combined_hook


def create_audited_post_hook_manager(workspace_root: str) -> AuditedPostHookManager:
    """
    Create an audited post-hook manager.

    Args:
        workspace_root: Root workspace directory for audit logs

    Returns:
        Audited post-hook manager
    """
    return AuditedPostHookManager(workspace_root)
