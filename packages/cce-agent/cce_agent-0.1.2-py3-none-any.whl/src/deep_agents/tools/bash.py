"""
Bash Tools for Deep Agents

This module provides bash execution capabilities for the deep agent,
allowing direct command execution when other tools are insufficient.
"""

import logging
from typing import Any, Dict, Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ExecuteBashCommandInput(BaseModel):
    """Input schema for execute_bash_command tool."""

    command: str = Field(..., description="The bash command to execute")
    timeout: int = Field(default=180, description="Timeout in seconds")


class AdvancedShellCommandInput(BaseModel):
    """Input schema for advanced_shell_command tool."""

    command: str = Field(..., description="The bash command to execute")
    work_dir: str = Field(default=".", description="Working directory for the command")
    timeout: int = Field(default=180, description="Timeout in seconds")


class CheckSystemStatusInput(BaseModel):
    """Input schema for check_system_status tool."""

    pass  # No parameters needed


# Import bash execution tools
try:
    from ...tools.openswe.core_tools import execute_bash
    from ...tools.openswe.dev_tools import advanced_shell

    BASH_TOOLS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Bash tools not available: {e}")
    BASH_TOOLS_AVAILABLE = False
    # Set fallback values to avoid NameError
    execute_bash = None
    advanced_shell = None


@tool(
    args_schema=ExecuteBashCommandInput,
    description="Execute a bash command directly with safety validation. CRITICAL: Always provide the command parameter. Use this when other tools are insufficient or you need direct system access.",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def execute_bash_command(command: str, timeout: int = 180) -> str:
    """
    Execute a bash command directly when other tools are insufficient.

    Use this tool when:
    - You need to run system commands that aren't available through other tools
    - You're stuck and need to debug or explore the system directly
    - You need to install packages, check system status, or run custom scripts
    - Other tools are failing and you need a direct approach

    Args:
        command: The bash command to execute
        timeout: Timeout in seconds (default: 30)

    Returns:
        Command execution results with success/error status
    """
    # Check if command is provided and not just whitespace
    if not command or not command.strip():
        error_msg = f"""⚠️ Command parameter is empty or missing.

To execute a bash command, provide the command like:
execute_bash_command(command="your bash command here")

Examples:
execute_bash_command(command="ls -la")
execute_bash_command(command="git status")
execute_bash_command(command="python --version")
execute_bash_command(command="cd /path && npm install")

CRITICAL: The command parameter cannot be empty or whitespace-only."""

        logger.error(f"❌ [BASH TOOLS] {error_msg}")
        return error_msg

    if not BASH_TOOLS_AVAILABLE:
        return "❌ Bash tools not available - missing dependencies"

    try:
        import asyncio
        import subprocess

        # Execute command directly without OpenAI safety validation to avoid quota issues
        # Basic safety checks for obviously dangerous commands
        dangerous_patterns = [
            "rm -rf /",
            "format",
            "mkfs",
            "dd if=",
            "shutdown",
            "reboot",
            "halt",
            "poweroff",
            "init 0",
            "init 6",
            "> /dev/sd",
            "mkfs.ext",
        ]

        if any(pattern in command.lower() for pattern in dangerous_patterns):
            return f"❌ **Command Blocked**\n\n```bash\n{command}\n```\n\n**Reason:** Command contains potentially dangerous patterns"

        # Execute the command directly using subprocess
        process = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)

        if process.returncode == 0:
            output = process.stdout.strip()
            return f"✅ **Command Executed Successfully**\n\n```bash\n{command}\n```\n\n**Output:**\n```\n{output}\n```"
        else:
            error_msg = process.stderr.strip() or process.stdout.strip()
            return f"❌ **Command Failed**\n\n```bash\n{command}\n```\n\n**Error (exit code: {process.returncode}):**\n```\n{error_msg}\n```"

    except subprocess.TimeoutExpired:
        return f"❌ **Command Timed Out**\n\n```bash\n{command}\n```\n\n**Error:** Command timed out after {timeout} seconds"
    except Exception as e:
        logger.error(f"Bash command execution failed: {e}")
        return f"❌ **Command Execution Error**\n\n```bash\n{command}\n```\n\n**Error:** {str(e)}"


@tool(
    args_schema=AdvancedShellCommandInput,
    description="Execute a bash command with advanced options, working directory control, and retry mechanism",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def advanced_shell_command(command: str, work_dir: str = ".", timeout: int = 180) -> str:
    """
    Execute a bash command with advanced options and working directory control.

    Use this tool when:
    - You need to run commands in a specific directory
    - You need more control over the execution environment
    - You're working with complex shell operations

    Args:
        command: The bash command to execute
        work_dir: Working directory for the command (default: current directory)
        timeout: Timeout in seconds (default: 30)

    Returns:
        Command execution results with success/error status
    """
    if not BASH_TOOLS_AVAILABLE:
        return "❌ Advanced shell tools not available - missing dependencies"

    try:
        import os
        import subprocess

        # Basic safety checks for obviously dangerous commands
        dangerous_patterns = [
            "rm -rf /",
            "format",
            "mkfs",
            "dd if=",
            "shutdown",
            "reboot",
            "halt",
            "poweroff",
            "init 0",
            "init 6",
            "> /dev/sd",
            "mkfs.ext",
        ]

        if any(pattern in command.lower() for pattern in dangerous_patterns):
            return f"❌ **Command Blocked**\n\n**Directory:** `{work_dir}`\n**Command:**\n```bash\n{command}\n```\n\n**Reason:** Command contains potentially dangerous patterns"

        # Execute the command directly using subprocess with working directory
        process = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout, cwd=work_dir)

        if process.returncode == 0:
            output = process.stdout.strip()
            return f"✅ **Advanced Shell Command Executed**\n\n**Directory:** `{work_dir}`\n**Command:**\n```bash\n{command}\n```\n\n**Output:**\n```\n{output}\n```"
        else:
            error_msg = process.stderr.strip() or process.stdout.strip()
            return f"❌ **Advanced Shell Command Failed**\n\n**Directory:** `{work_dir}`\n**Command:**\n```bash\n{command}\n```\n\n**Error (exit code: {process.returncode}):**\n```\n{error_msg}\n```"

    except subprocess.TimeoutExpired:
        return f"❌ **Advanced Shell Command Timed Out**\n\n**Directory:** `{work_dir}`\n**Command:**\n```bash\n{command}\n```\n\n**Error:** Command timed out after {timeout} seconds"
    except Exception as e:
        logger.error(f"Advanced shell command execution failed: {e}")
        return f"❌ **Advanced Shell Execution Error**\n\n**Directory:** `{work_dir}`\n**Command:**\n```bash\n{command}\n```\n\n**Error:** {str(e)}"


@tool(
    args_schema=CheckSystemStatusInput,
    description="Check basic system status and environment information including OS, Python version, and available tools",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def check_system_status() -> str:
    """
    Check basic system status and environment information.

    Use this tool when:
    - You need to understand the current system environment
    - You're debugging issues and need system information
    - You want to verify what tools and commands are available

    Returns:
        System status information including OS, Python version, available tools, etc.
    """
    if not BASH_TOOLS_AVAILABLE:
        return "❌ System status check not available - missing dependencies"

    try:
        import asyncio
        import os
        import subprocess
        import sys

        # Collect system information
        system_info = []

        # Python version
        system_info.append(f"🐍 **Python Version:** {sys.version}")

        # Current working directory
        system_info.append(f"📁 **Working Directory:** {os.getcwd()}")

        # Check common tools
        common_tools = ["git", "python", "pip", "node", "npm", "docker", "kubectl"]
        available_tools = []

        for tool in common_tools:
            try:
                result = subprocess.run(f"which {tool}", shell=True, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    available_tools.append(f"✅ {tool}")
                else:
                    available_tools.append(f"❌ {tool}")
            except:
                available_tools.append(f"❓ {tool}")

        system_info.append(f"🔧 **Available Tools:**\n" + "\n".join(available_tools))

        # Git status if available
        try:
            git_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True, timeout=5)
            if git_result.returncode == 0:
                git_output = git_result.stdout.strip()
                if git_output:
                    system_info.append(f"📝 **Git Status:**\n```\n{git_output}\n```")
                else:
                    system_info.append("📝 **Git Status:** Clean working directory")
        except:
            system_info.append("📝 **Git Status:** Not available")

        return "🖥️ **System Status**\n\n" + "\n\n".join(system_info)

    except Exception as e:
        logger.error(f"System status check failed: {e}")
        return f"❌ **System Status Check Failed**\n\n**Error:** {str(e)}"


# Export bash tools
BASH_TOOLS = [execute_bash_command, advanced_shell_command, check_system_status]
