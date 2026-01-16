"""
Constants and Configuration for CCE Deep Agent

This module defines command constants and configuration values,
directly ported from open-swe-v2 patterns for consistency.
"""

from enum import Enum
from typing import Any, Dict, Set


class CommandCategory(Enum):
    """Categories of commands for safety and approval handling."""

    FILE_OPERATIONS = "file_operations"
    SYSTEM_OPERATIONS = "system_operations"
    GIT_OPERATIONS = "git_operations"
    NETWORK_OPERATIONS = "network_operations"
    READ_ONLY = "read_only"


# File operation commands that require approval
FILE_EDIT_COMMANDS: set[str] = {
    "write_file",
    "hybrid_write_file",
    "str_replace_based_edit_tool",
    "edit_file",
    "hybrid_edit_file",
    "create_file",
    "delete_file",
    "move_file",
    "copy_file",
}

# System operation commands that require approval
SYSTEM_COMMANDS: set[str] = {"execute_bash", "run_command", "shell_command", "system_call"}

# Git operation commands that require approval
GIT_COMMANDS: set[str] = {
    "git_commit",
    "git_push",
    "git_reset",
    "git_rebase",
    "git_merge",
    "git_checkout",
    "git_branch",
    "git_tag",
}

# Network operation commands that require approval
NETWORK_COMMANDS: set[str] = {"curl", "wget", "ssh", "scp", "rsync", "nc", "netcat", "telnet"}

# All commands that require approval (includes file operations plus other system operations)
WRITE_COMMANDS: set[str] = (
    FILE_EDIT_COMMANDS
    | SYSTEM_COMMANDS
    | GIT_COMMANDS
    | NETWORK_COMMANDS
    | {"rm", "mv", "cp", "mkdir", "rmdir", "chmod", "chown", "ln", "unlink"}
)

# Read-only commands that generally don't require approval
READ_ONLY_COMMANDS: set[str] = {
    "ls",
    "hybrid_ls",
    "read_file",
    "hybrid_read_file",
    "cat",
    "grep",
    "find",
    "pwd",
    "whoami",
    "date",
    "echo",
    "head",
    "tail",
    "less",
    "more",
    "file",
    "stat",
    "du",
    "df",
    "ps",
    "top",
    "htop",
    "git_status",
    "git_log",
    "git_diff",
    "git_show",
    "git_branch_list",
    "git_remote_list",
}

# Commands that are always safe and never require approval
SAFE_COMMANDS: set[str] = {
    "pwd",
    "whoami",
    "date",
    "echo",
    "ls",
    "hybrid_ls",
    "read_file",
    "hybrid_read_file",
    "cat",
    "grep",
    "find",
    "git_status",
    "git_log",
    "git_diff",
    "git_show",
    "git_branch_list",
    "git_remote_list",
}

# Commands that are high risk and always require approval
HIGH_RISK_COMMANDS: set[str] = {
    "execute_bash",
    "write_file",
    "hybrid_write_file",
    "edit_file",
    "hybrid_edit_file",
    "rm",
    "mv",
    "git_commit",
    "git_push",
    "git_reset",
    "curl",
    "wget",
    "ssh",
    "scp",
}

# Command categories mapping
COMMAND_CATEGORIES: dict[str, set[str]] = {
    CommandCategory.FILE_OPERATIONS.value: FILE_EDIT_COMMANDS,
    CommandCategory.SYSTEM_OPERATIONS.value: SYSTEM_COMMANDS,
    CommandCategory.GIT_OPERATIONS.value: GIT_COMMANDS,
    CommandCategory.NETWORK_OPERATIONS.value: NETWORK_COMMANDS,
    CommandCategory.READ_ONLY.value: READ_ONLY_COMMANDS,
}

# Approval cache configuration
APPROVAL_CACHE_CONFIG: dict[str, Any] = {
    "default_expiration_hours": 24,
    "max_cache_size": 1000,
    "cleanup_interval_minutes": 60,
    "high_risk_expiration_hours": 1,
    "safe_command_expiration_hours": 168,  # 1 week
}

# Safety validation configuration
SAFETY_CONFIG: dict[str, Any] = {
    "enable_ai_validation": True,
    "enable_pattern_matching": True,
    "enable_whitelist_check": True,
    "max_command_length": 10000,
    "suspicious_pattern_threshold": 0.7,
    "malicious_pattern_threshold": 0.9,
}

# MCP integration configuration
MCP_CONFIG: dict[str, Any] = {
    "default_timeout_seconds": 30,
    "max_retries": 3,
    "retry_delay_seconds": 1,
    "health_check_interval_minutes": 5,
    "max_concurrent_connections": 10,
}

# Error handling configuration
ERROR_HANDLING_CONFIG: dict[str, Any] = {
    "max_retries": 3,
    "retry_delay_seconds": 1,
    "timeout_seconds": 30,
    "enable_fallback": True,
    "log_level": "INFO",
    "enable_metrics": True,
}

# Post-model hook configuration
POST_MODEL_HOOK_CONFIG: dict[str, Any] = {
    "enable_approval_caching": True,
    "enable_safety_validation": True,
    "enable_interrupts": True,
    "approval_timeout_seconds": 300,  # 5 minutes
    "max_interrupts_per_session": 100,
    # Automatic validation options
    "enable_automatic_validation": True,
    "validation_tools": ["run_linting", "check_syntax"],
    "validation_timeout_seconds": 30,
    "log_validation_results": True,
    "store_validation_results": True,
}

# File system configuration
FILESYSTEM_CONFIG: dict[str, Any] = {
    "max_file_size_mb": 100,
    "allowed_extensions": {
        ".py",
        ".js",
        ".ts",
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".xml",
        ".html",
        ".css",
        ".scss",
        ".sql",
        ".sh",
        ".bash",
    },
    "blocked_extensions": {
        ".exe",
        ".bat",
        ".cmd",
        ".com",
        ".pif",
        ".scr",
        ".vbs",
        ".js",
        ".jar",
        ".app",
        ".dmg",
        ".pkg",
        ".deb",
        ".rpm",
    },
    "max_directory_depth": 20,
    "temp_directory": "/tmp/cce-agent",
}

# Planning tool configuration
PLANNING_CONFIG: dict[str, Any] = {
    "max_plan_steps": 1000,
    "max_plan_description_length": 1000,
    "default_plan_expiration_hours": 72,
    "enable_plan_persistence": True,
    "max_concurrent_plans": 10,
}

# Sub-agent configuration
SUBAGENT_CONFIG: dict[str, Any] = {
    "max_subagent_calls": 1000,
    "subagent_timeout_seconds": 300,
    "enable_subagent_fallback": True,
    "max_subagent_depth": 5,
    "enable_subagent_metrics": True,
}

# Logging configuration
LOGGING_CONFIG: dict[str, Any] = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "enable_file_logging": True,
    "log_file_path": "logs/cce-agent.log",
    "max_log_file_size_mb": 100,
    "backup_count": 5,
    "enable_console_logging": True,
}

# Performance configuration
PERFORMANCE_CONFIG: dict[str, Any] = {
    "enable_caching": True,
    "cache_ttl_seconds": 3600,
    "max_cache_size": 10000,
    "enable_compression": True,
    "compression_level": 6,
    "enable_metrics": True,
    "metrics_interval_seconds": 60,
}

# Security configuration
SECURITY_CONFIG: dict[str, Any] = {
    "enable_sandboxing": True,
    "sandbox_timeout_seconds": 30,
    "max_memory_mb": 512,
    "max_cpu_percent": 50,
    "enable_network_isolation": True,
    "allowed_network_hosts": [],
    "blocked_network_hosts": [],
}

# Prompt cache configuration
PROMPT_CACHE_CONFIG: dict[str, Any] = {"enabled": True, "max_entries": 10000, "ttl_hours": 24}

# All configuration dictionaries
ALL_CONFIGS: dict[str, dict[str, Any]] = {
    "approval_cache": APPROVAL_CACHE_CONFIG,
    "safety": SAFETY_CONFIG,
    "mcp": MCP_CONFIG,
    "error_handling": ERROR_HANDLING_CONFIG,
    "post_model_hook": POST_MODEL_HOOK_CONFIG,
    "filesystem": FILESYSTEM_CONFIG,
    "planning": PLANNING_CONFIG,
    "subagent": SUBAGENT_CONFIG,
    "logging": LOGGING_CONFIG,
    "performance": PERFORMANCE_CONFIG,
    "security": SECURITY_CONFIG,
    "prompt_cache": PROMPT_CACHE_CONFIG,
}


def get_config(config_name: str, key: str = None, default: Any = None) -> Any:
    """
    Get configuration value.

    Args:
        config_name: Name of the configuration section
        key: Optional specific key within the section
        default: Default value if not found

    Returns:
        Configuration value
    """
    if config_name not in ALL_CONFIGS:
        return default

    config = ALL_CONFIGS[config_name]

    if key is None:
        return config

    return config.get(key, default)


def is_write_command(command: str) -> bool:
    """
    Check if a command is a write command that requires approval.

    Args:
        command: Command name to check

    Returns:
        True if command requires approval
    """
    return command in WRITE_COMMANDS


def is_safe_command(command: str) -> bool:
    """
    Check if a command is safe and doesn't require approval.

    Args:
        command: Command name to check

    Returns:
        True if command is safe
    """
    return command in SAFE_COMMANDS


def is_high_risk_command(command: str) -> bool:
    """
    Check if a command is high risk and always requires approval.

    Args:
        command: Command name to check

    Returns:
        True if command is high risk
    """
    return command in HIGH_RISK_COMMANDS


def get_command_category(command: str) -> str:
    """
    Get the category of a command.

    Args:
        command: Command name to categorize

    Returns:
        Command category
    """
    for category, commands in COMMAND_CATEGORIES.items():
        if command in commands:
            return category

    return "unknown"


def get_approval_requirements(command: str) -> dict[str, Any]:
    """
    Get approval requirements for a command.

    Args:
        command: Command name to check

    Returns:
        Dictionary with approval requirements
    """
    return {
        "requires_approval": is_write_command(command),
        "is_safe": is_safe_command(command),
        "is_high_risk": is_high_risk_command(command),
        "category": get_command_category(command),
        "expiration_hours": (
            APPROVAL_CACHE_CONFIG["high_risk_expiration_hours"]
            if is_high_risk_command(command)
            else APPROVAL_CACHE_CONFIG["safe_command_expiration_hours"]
            if is_safe_command(command)
            else APPROVAL_CACHE_CONFIG["default_expiration_hours"]
        ),
    }


# Tool Call Validation Configuration
TOOL_CALL_VALIDATION_CONFIG: dict[str, Any] = {
    "enabled": True,
    "strict_mode": True,
    "validation_rules": {
        "write_file": {
            "required_parameters": ["file_path", "content"],
            "parameter_validation": {
                "content": {"type": "string", "min_length": 1, "not_empty": True},
                "file_path": {"type": "string", "min_length": 1, "not_empty": True},
            },
        },
        "hybrid_write_file": {
            "required_parameters": ["file_path", "content"],
            "parameter_validation": {
                "content": {"type": "string", "min_length": 1, "not_empty": True},
                "file_path": {"type": "string", "min_length": 1, "not_empty": True},
            },
        },
        "edit_file": {
            "required_parameters": ["file_path", "old_string", "new_string"],
            "parameter_validation": {
                "file_path": {"type": "string", "min_length": 1, "not_empty": True},
                "old_string": {
                    "type": "string",
                    "min_length": 0,  # Can be empty string for insertion
                },
                "new_string": {
                    "type": "string",
                    "min_length": 0,  # Can be empty string for deletion
                },
            },
        },
        "hybrid_edit_file": {
            "required_parameters": ["file_path", "old_string", "new_string"],
            "parameter_validation": {
                "file_path": {"type": "string", "min_length": 1, "not_empty": True},
                "old_string": {
                    "type": "string",
                    "min_length": 0,  # Can be empty string for insertion
                },
                "new_string": {
                    "type": "string",
                    "min_length": 0,  # Can be empty string for deletion
                },
            },
        },
        "execute_bash_command": {
            "required_parameters": ["command"],
            "parameter_validation": {"command": {"type": "string", "min_length": 1, "not_empty": True}},
        },
    },
    "error_handling": {"fail_fast": True, "max_validation_errors": 10, "include_suggestions": True},
    "scoring": {"parameter_completeness_weight": 0.6, "parameter_validation_weight": 0.4, "passing_threshold": 0.8},
}


def get_tool_validation_config(tool_name: str = None) -> dict[str, Any]:
    """
    Get tool call validation configuration.

    Args:
        tool_name: Specific tool name to get config for, or None for global config

    Returns:
        Validation configuration dictionary
    """
    if tool_name and tool_name in TOOL_CALL_VALIDATION_CONFIG["validation_rules"]:
        return TOOL_CALL_VALIDATION_CONFIG["validation_rules"][tool_name]

    return TOOL_CALL_VALIDATION_CONFIG


def is_tool_validation_enabled() -> bool:
    """
    Check if tool call validation is enabled.

    Returns:
        True if validation is enabled
    """
    return TOOL_CALL_VALIDATION_CONFIG.get("enabled", True)


def get_validation_threshold() -> float:
    """
    Get the validation passing threshold.

    Returns:
        Validation threshold score
    """
    return TOOL_CALL_VALIDATION_CONFIG["scoring"].get("passing_threshold", 0.8)
