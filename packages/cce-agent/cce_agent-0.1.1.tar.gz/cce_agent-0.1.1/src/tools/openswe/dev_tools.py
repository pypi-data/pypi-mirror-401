"""
Development Tools

Tools for software development tasks including grep search, dependency management,
command safety evaluation, and advanced shell operations.
"""

import asyncio
import logging
import os
from typing import Any

from langchain_core.tools import tool

from .command_safety import validate_command_safety
from src.workspace_context import get_workspace_root

logger = logging.getLogger(__name__)


def _resolve_work_dir(work_dir: str | None) -> str:
    if work_dir and work_dir != ".":
        return work_dir
    resolved = get_workspace_root()
    return resolved or (work_dir or ".")


def _format_grep_command(pattern: str, files: list[str], options: dict[str, Any] = None) -> list[str]:
    """Format grep command with options"""
    if options is None:
        options = {}

    cmd = ["grep"]

    # Add options
    if options.get("case_insensitive", False):
        cmd.append("-i")
    if options.get("recursive", False):
        cmd.append("-r")
    if options.get("line_numbers", True):
        cmd.append("-n")
    if options.get("invert_match", False):
        cmd.append("-v")
    if options.get("whole_words", False):
        cmd.append("-w")

    # Add pattern
    cmd.append(pattern)

    # Add files
    cmd.extend(files)

    return cmd


@tool
async def grep_search(
    pattern: str,
    files: list[str],
    case_insensitive: bool = False,
    recursive: bool = False,
    line_numbers: bool = True,
    invert_match: bool = False,
    whole_words: bool = False,
    work_dir: str = ".",
) -> dict[str, Any]:
    """
    Search for patterns in files using grep with advanced options.

    Args:
        pattern: The search pattern (regex supported)
        files: List of files or directories to search
        case_insensitive: Case-insensitive search (default: False)
        recursive: Recursive search in directories (default: False)
        line_numbers: Show line numbers (default: True)
        invert_match: Invert match (show non-matching lines) (default: False)
        whole_words: Match whole words only (default: False)
        work_dir: Working directory for search (default: current directory)

    Returns:
        Dictionary containing search results
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        # Format grep command
        options = {
            "case_insensitive": case_insensitive,
            "recursive": recursive,
            "line_numbers": line_numbers,
            "invert_match": invert_match,
            "whole_words": whole_words,
        }

        cmd = _format_grep_command(pattern, files, options)

        # Execute grep command
        process = await asyncio.create_subprocess_exec(
            *cmd, cwd=work_dir, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 1:
            # No matches found
            return {"success": True, "result": "No matches found", "status": "success", "exit_code": 1}
        elif process.returncode > 1:
            # Error occurred
            error_msg = stderr.decode("utf-8") if stderr else "Unknown error"
            return {
                "success": False,
                "result": f"Grep command failed with exit code {process.returncode}: {error_msg}",
                "status": "error",
                "exit_code": process.returncode,
            }
        else:
            # Success
            result = stdout.decode("utf-8") if stdout else ""
            return {"success": True, "result": result, "status": "success", "exit_code": 0}

    except Exception as e:
        return {"success": False, "result": f"Error running grep search: {str(e)}", "status": "error", "exit_code": -1}


@tool
async def install_dependencies(command: list[str], work_dir: str = ".", timeout: int = 150) -> dict[str, Any]:
    """
    Install dependencies using package managers.

    Args:
        command: List of command parts (e.g., ["npm", "install"])
        work_dir: Working directory for installation (default: current directory)
        timeout: Timeout in seconds (default: 150)

    Returns:
        Dictionary containing installation results
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        # Validate command safety
        full_command = " ".join(command)
        safety_validation = await validate_command_safety(full_command)

        if not safety_validation.get("is_safe", False):
            return {
                "success": False,
                "result": f"Command blocked - safety validation failed: {safety_validation.get('reasoning', 'Unknown reason')}",
                "status": "error",
            }

        # Set environment variables
        env = os.environ.copy()
        env["COREPACK_ENABLE_DOWNLOAD_PROMPT"] = "0"  # Prevent corepack prompts

        # Execute command
        process = await asyncio.create_subprocess_exec(
            *command, cwd=work_dir, env=env, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except TimeoutError:
            process.kill()
            await process.wait()
            return {"success": False, "result": f"Command timed out after {timeout} seconds", "status": "error"}

        if process.returncode != 0:
            error_msg = stderr.decode("utf-8") if stderr else "Unknown error"
            return {
                "success": False,
                "result": f"Installation failed with exit code {process.returncode}: {error_msg}",
                "status": "error",
            }

        result = stdout.decode("utf-8") if stdout else "Installation completed successfully"
        return {"success": True, "result": result, "status": "success"}

    except Exception as e:
        return {"success": False, "result": f"Error installing dependencies: {str(e)}", "status": "error"}


@tool
async def advanced_shell(
    command: str, work_dir: str = ".", timeout: int = 180, env_vars: dict[str, str] | None = None
) -> dict[str, Any]:
    """
    Execute shell commands with advanced options and environment management.

    Args:
        command: The shell command to execute
        work_dir: Working directory for execution (default: current directory)
        timeout: Timeout in seconds (default: 30)
        env_vars: Additional environment variables (default: None)

    Returns:
        Dictionary containing command execution results
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        # Validate command safety
        safety_validation = await validate_command_safety(command)

        if not safety_validation.get("is_safe", False):
            return {
                "success": False,
                "result": f"Command blocked - safety validation failed: {safety_validation.get('reasoning', 'Unknown reason')}",
                "status": "error",
            }

        # Set up environment
        env = os.environ.copy()
        env["COREPACK_ENABLE_DOWNLOAD_PROMPT"] = "0"  # Prevent corepack prompts

        if env_vars:
            env.update(env_vars)

        # Execute command
        process = await asyncio.create_subprocess_shell(
            command, cwd=work_dir, env=env, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except TimeoutError:
            process.kill()
            await process.wait()
            return {"success": False, "result": f"Command timed out after {timeout} seconds", "status": "error"}

        if process.returncode != 0:
            error_msg = stderr.decode("utf-8") if stderr else "Unknown error"
            return {
                "success": False,
                "result": f"Command failed with exit code {process.returncode}: {error_msg}",
                "status": "error",
            }

        result = stdout.decode("utf-8") if stdout else "Command completed successfully"
        return {"success": True, "result": result, "status": "success"}

    except Exception as e:
        return {"success": False, "result": f"Error executing command: {str(e)}", "status": "error"}


@tool
async def command_safety_evaluator(command: str, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
    """
    AI-powered command safety evaluation for development commands.

    Args:
        command: The command to evaluate
        tool_name: The name of the tool (shell, grep, view, etc.)
        args: The arguments passed to the tool

    Returns:
        Dictionary containing safety evaluation results
    """
    try:
        # Use our existing command safety validation
        safety_validation = await validate_command_safety(command)

        # Map the validation result to our expected format
        is_safe = safety_validation.get("is_safe", False)
        reasoning = safety_validation.get("reasoning", "No reasoning provided")
        threat_type = safety_validation.get("threat_type", "UNKNOWN")

        # Determine risk level based on threat type
        if threat_type == "SAFE":
            risk_level = "low"
        elif threat_type == "PROMPT_INJECTION" or threat_type == "MALICIOUS_COMMAND":
            risk_level = "high"
        else:
            risk_level = "medium"

        logger.info(
            "Command safety evaluation completed",
            {
                "command": command,
                "tool_name": tool_name,
                "is_safe": is_safe,
                "risk_level": risk_level,
            },
        )

        return {
            "success": True,
            "result": {"is_safe": is_safe, "reasoning": reasoning, "risk_level": risk_level},
            "status": "success",
        }

    except Exception as e:
        logger.error(
            "Failed to evaluate command safety",
            {
                "error": str(e),
            },
        )
        return {
            "success": False,
            "result": {
                "is_safe": False,
                "reasoning": "Failed to evaluate safety - defaulting to unsafe",
                "risk_level": "high",
            },
            "status": "error",
        }


__all__ = ["grep_search", "install_dependencies", "advanced_shell", "command_safety_evaluator"]
