"""
State Helpers for CCE Deep Agent

This module implements approval caching with directory-based keys,
directly ported from open-swe-v2 patterns for reducing user friction.
"""

import logging
import pathlib
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class ApprovalCache:
    """Approval cache entry."""

    approval_key: str
    command: str
    args: dict[str, Any]
    approved_at: datetime
    expires_at: datetime | None = None
    approval_count: int = 1
    last_used: datetime | None = None


class AgentStateHelpers:
    """
    Helper functions for agent state management and approval caching.

    This class provides utilities for managing approval caching with
    directory-based keys, directly inspired by open-swe-v2 patterns.
    """

    @staticmethod
    def get_approval_key(command: str, args: dict[str, Any]) -> str:
        """
        Generate approval key based on command and directory.

        This method creates a unique key for approval caching based on
        the command type and the target directory, following open-swe-v2 patterns.

        Args:
            command: The command being executed
            args: Command arguments

        Returns:
            Unique approval key string
        """
        try:
            target_dir = None

            # File operation commands
            if command in [
                "write_file",
                "write_file",
                "edit_file",
                "edit_file",
                "str_replace_based_edit_tool",
            ]:
                file_path = args.get("file_path") or args.get("path")
                if file_path:
                    target_dir = pathlib.Path(file_path).parent.resolve()

            # Bash execution commands
            elif command == "execute_bash":
                target_dir = pathlib.Path(args.get("cwd", ".")).resolve()

            # File system exploration commands
            elif command in ["ls", "ls", "read_file", "read_file", "glob", "grep"]:
                target_dir = pathlib.Path(args.get("path", args.get("directory", "."))).resolve()

            # Git commands
            elif command in ["git_add", "git_commit", "git_push", "git_pull"]:
                target_dir = pathlib.Path(args.get("cwd", ".")).resolve()

            # Default to current working directory
            if not target_dir:
                target_dir = pathlib.Path.cwd()

            # Create approval key
            approval_key = f"{command}:{target_dir}"

            logger.debug(f"Generated approval key: {approval_key}")
            return approval_key

        except Exception as e:
            logger.error(f"Error generating approval key: {e}")
            # Fallback to command only
            return f"{command}:fallback"

    @staticmethod
    def is_operation_approved(state: dict[str, Any], command: str, args: dict[str, Any]) -> bool:
        """
        Check if operation is already approved.

        Args:
            state: Agent state containing approval cache
            command: Command being executed
            args: Command arguments

        Returns:
            True if operation is already approved
        """
        try:
            if not state.get("approved_operations"):
                return False

            approved_operations = state["approved_operations"]
            if not approved_operations.get("cached_approvals"):
                return False

            approval_key = AgentStateHelpers.get_approval_key(command, args)
            cached_approvals = approved_operations["cached_approvals"]

            # Check if approval exists and is not expired
            if approval_key in cached_approvals:
                approval_entry = cached_approvals[approval_key]

                # Check expiration
                if approval_entry.get("expires_at"):
                    expires_at = datetime.fromisoformat(approval_entry["expires_at"])
                    if datetime.now() > expires_at:
                        # Remove expired approval
                        del cached_approvals[approval_key]
                        return False

                # Update last used timestamp
                approval_entry["last_used"] = datetime.now().isoformat()
                approval_entry["approval_count"] = approval_entry.get("approval_count", 0) + 1

                logger.debug(f"Operation approved from cache: {approval_key}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error checking operation approval: {e}")
            return False

    @staticmethod
    def add_operation_approval(
        state: dict[str, Any], command: str, args: dict[str, Any], expires_in_hours: int | None = None
    ) -> None:
        """
        Add operation to approval cache.

        Args:
            state: Agent state to update
            command: Command that was approved
            args: Command arguments
            expires_in_hours: Optional expiration time in hours
        """
        try:
            if "approved_operations" not in state:
                state["approved_operations"] = {"cached_approvals": {}}

            approved_operations = state["approved_operations"]
            if "cached_approvals" not in approved_operations:
                approved_operations["cached_approvals"] = {}

            approval_key = AgentStateHelpers.get_approval_key(command, args)
            now = datetime.now()

            # Calculate expiration time
            expires_at = None
            if expires_in_hours:
                expires_at = now + timedelta(hours=expires_in_hours)

            # Create approval entry
            approval_entry = {
                "command": command,
                "args": args,
                "approved_at": now.isoformat(),
                "expires_at": expires_at.isoformat() if expires_at else None,
                "approval_count": 1,
                "last_used": now.isoformat(),
            }

            approved_operations["cached_approvals"][approval_key] = approval_entry

            logger.info(f"Added operation to approval cache: {approval_key}")

        except Exception as e:
            logger.error(f"Error adding operation approval: {e}")

    @staticmethod
    def remove_operation_approval(state: dict[str, Any], command: str, args: dict[str, Any]) -> bool:
        """
        Remove operation from approval cache.

        Args:
            state: Agent state to update
            command: Command to remove
            args: Command arguments

        Returns:
            True if approval was removed
        """
        try:
            if not state.get("approved_operations", {}).get("cached_approvals"):
                return False

            approval_key = AgentStateHelpers.get_approval_key(command, args)
            cached_approvals = state["approved_operations"]["cached_approvals"]

            if approval_key in cached_approvals:
                del cached_approvals[approval_key]
                logger.info(f"Removed operation from approval cache: {approval_key}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error removing operation approval: {e}")
            return False

    @staticmethod
    def clear_expired_approvals(state: dict[str, Any]) -> int:
        """
        Clear expired approvals from cache.

        Args:
            state: Agent state to clean up

        Returns:
            Number of expired approvals removed
        """
        try:
            if not state.get("approved_operations", {}).get("cached_approvals"):
                return 0

            cached_approvals = state["approved_operations"]["cached_approvals"]
            now = datetime.now()
            expired_keys = []

            for approval_key, approval_entry in cached_approvals.items():
                if approval_entry.get("expires_at"):
                    expires_at = datetime.fromisoformat(approval_entry["expires_at"])
                    if now > expires_at:
                        expired_keys.append(approval_key)

            # Remove expired approvals
            for key in expired_keys:
                del cached_approvals[key]

            if expired_keys:
                logger.info(f"Cleared {len(expired_keys)} expired approvals")

            return len(expired_keys)

        except Exception as e:
            logger.error(f"Error clearing expired approvals: {e}")
            return 0

    @staticmethod
    def get_approval_cache_stats(state: dict[str, Any]) -> dict[str, Any]:
        """
        Get approval cache statistics.

        Args:
            state: Agent state to analyze

        Returns:
            Dictionary with cache statistics
        """
        try:
            if not state.get("approved_operations", {}).get("cached_approvals"):
                return {
                    "total_approvals": 0,
                    "expired_approvals": 0,
                    "active_approvals": 0,
                    "most_used_command": None,
                    "cache_size_bytes": 0,
                }

            cached_approvals = state["approved_operations"]["cached_approvals"]
            now = datetime.now()

            total_approvals = len(cached_approvals)
            expired_approvals = 0
            active_approvals = 0
            command_usage = {}
            total_size = 0

            for approval_key, approval_entry in cached_approvals.items():
                # Calculate size (rough estimate)
                total_size += len(str(approval_entry))

                # Check expiration
                if approval_entry.get("expires_at"):
                    expires_at = datetime.fromisoformat(approval_entry["expires_at"])
                    if now > expires_at:
                        expired_approvals += 1
                    else:
                        active_approvals += 1
                else:
                    active_approvals += 1

                # Track command usage
                command = approval_entry.get("command", "unknown")
                usage_count = approval_entry.get("approval_count", 0)
                if command in command_usage:
                    command_usage[command] += usage_count
                else:
                    command_usage[command] = usage_count

            most_used_command = max(command_usage.items(), key=lambda x: x[1])[0] if command_usage else None

            return {
                "total_approvals": total_approvals,
                "expired_approvals": expired_approvals,
                "active_approvals": active_approvals,
                "most_used_command": most_used_command,
                "cache_size_bytes": total_size,
                "command_usage": command_usage,
            }

        except Exception as e:
            logger.error(f"Error getting approval cache stats: {e}")
            return {
                "total_approvals": 0,
                "expired_approvals": 0,
                "active_approvals": 0,
                "most_used_command": None,
                "cache_size_bytes": 0,
                "error": str(e),
            }

    @staticmethod
    def should_require_approval(command: str, args: dict[str, Any]) -> bool:
        """
        Determine if a command should require approval.

        Args:
            command: Command being executed
            args: Command arguments

        Returns:
            True if command should require approval
        """
        # Commands that always require approval
        high_risk_commands = {
            "execute_bash",
            "write_file",
            "edit_file",
            "str_replace_based_edit_tool",
            "git_commit",
            "git_push",
            "git_reset",
            "rm",
            "mv",
            "cp",
        }

        # Commands that are generally safe
        safe_commands = {
            "ls",
            "read_file",
            "cat",
            "grep",
            "find",
            "pwd",
            "whoami",
            "date",
            "echo",
            "git_status",
            "git_log",
            "git_diff",
        }

        if command in high_risk_commands:
            return True
        elif command in safe_commands:
            return False
        else:
            # Unknown commands require approval by default
            return True

    @staticmethod
    def get_approval_context(command: str, args: dict[str, Any]) -> dict[str, Any]:
        """
        Get context information for approval decision.

        Args:
            command: Command being executed
            args: Command arguments

        Returns:
            Context information for approval
        """
        try:
            approval_key = AgentStateHelpers.get_approval_key(command, args)
            target_dir = None

            # Extract target directory
            if command in [
                "write_file",
                "write_file",
                "edit_file",
                "edit_file",
                "str_replace_based_edit_tool",
            ]:
                file_path = args.get("file_path") or args.get("path")
                if file_path:
                    target_dir = str(pathlib.Path(file_path).parent.resolve())
            elif command == "execute_bash":
                target_dir = str(pathlib.Path(args.get("cwd", ".")).resolve())
            elif command in ["ls", "ls", "read_file", "read_file", "glob", "grep"]:
                target_dir = str(pathlib.Path(args.get("path", args.get("directory", "."))).resolve())

            return {
                "approval_key": approval_key,
                "command": command,
                "target_directory": target_dir,
                "requires_approval": AgentStateHelpers.should_require_approval(command, args),
                "risk_level": "high"
                if command in ["execute_bash", "write_file", "write_file", "edit_file", "edit_file"]
                else "medium",
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error getting approval context: {e}")
            return {
                "approval_key": f"{command}:error",
                "command": command,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
