"""
Execution Configuration System

Manages execution modes and tool selection for the CCE agent.
Supports switching between native Open SWE tools and Aider integration.
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ExecutionMode(Enum):
    """Available execution modes for the CCE agent."""

    NATIVE = "native"  # Use native Open SWE tools (default)
    AIDER = "aider"  # Use Aider integration
    HYBRID = "hybrid"  # Use both, with native as primary and Aider as fallback


@dataclass
class ExecutionConfig:
    """Configuration for execution mode and tool selection."""

    mode: ExecutionMode
    use_native_file_discovery: bool = True
    use_native_editing: bool = True
    use_native_validation: bool = True
    use_aider_fallback: bool = False
    aider_timeout: int = 300  # 5 minutes
    native_timeout: int = 60  # 1 minute

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary for easy serialization."""
        return {
            "mode": self.mode.value,
            "use_native_file_discovery": self.use_native_file_discovery,
            "use_native_editing": self.use_native_editing,
            "use_native_validation": self.use_native_validation,
            "use_aider_fallback": self.use_aider_fallback,
            "aider_timeout": self.aider_timeout,
            "native_timeout": self.native_timeout,
        }


class ExecutionConfigManager:
    """Manages execution configuration and environment variable parsing."""

    @staticmethod
    def get_config() -> ExecutionConfig:
        """
        Get execution configuration from environment variables and defaults.

        Environment Variables:
        - EXECUTION_MODE: "native", "aider", or "hybrid" (default: "native")
        - USE_NATIVE_FILE_DISCOVERY: "true" or "false" (default: "true")
        - USE_NATIVE_EDITING: "true" or "false" (default: "true")
        - USE_NATIVE_VALIDATION: "true" or "false" (default: "true")
        - USE_AIDER_FALLBACK: "true" or "false" (default: "false")
        - AIDER_TIMEOUT: timeout in seconds (default: 300)
        - NATIVE_TIMEOUT: timeout in seconds (default: 60)
        """
        # Parse execution mode
        mode_str = os.environ.get("EXECUTION_MODE", "native").lower()
        try:
            mode = ExecutionMode(mode_str)
        except ValueError:
            print(f"Warning: Invalid EXECUTION_MODE '{mode_str}', using 'native'")
            mode = ExecutionMode.NATIVE

        # Parse boolean flags
        def parse_bool(value: str, default: bool) -> bool:
            if value.lower() in ("true", "1", "yes", "on"):
                return True
            elif value.lower() in ("false", "0", "no", "off"):
                return False
            else:
                return default

        use_native_file_discovery = parse_bool(os.environ.get("USE_NATIVE_FILE_DISCOVERY", "true"), True)
        use_native_editing = parse_bool(os.environ.get("USE_NATIVE_EDITING", "true"), True)
        use_native_validation = parse_bool(os.environ.get("USE_NATIVE_VALIDATION", "true"), True)
        use_aider_fallback = parse_bool(os.environ.get("USE_AIDER_FALLBACK", "false"), False)

        # Parse timeouts
        try:
            aider_timeout = int(os.environ.get("AIDER_TIMEOUT", "300"))
        except ValueError:
            aider_timeout = 300

        try:
            native_timeout = int(os.environ.get("NATIVE_TIMEOUT", "60"))
        except ValueError:
            native_timeout = 60

        return ExecutionConfig(
            mode=mode,
            use_native_file_discovery=use_native_file_discovery,
            use_native_editing=use_native_editing,
            use_native_validation=use_native_validation,
            use_aider_fallback=use_aider_fallback,
            aider_timeout=aider_timeout,
            native_timeout=native_timeout,
        )

    @staticmethod
    def should_use_native_tools(config: ExecutionConfig) -> bool:
        """Check if native tools should be used based on configuration."""
        return config.mode in [ExecutionMode.NATIVE, ExecutionMode.HYBRID]

    @staticmethod
    def should_use_aider_tools(config: ExecutionConfig) -> bool:
        """Check if Aider tools should be used based on configuration."""
        return config.mode in [ExecutionMode.AIDER, ExecutionMode.HYBRID]

    @staticmethod
    def get_file_discovery_strategy(config: ExecutionConfig) -> str:
        """Get the file discovery strategy based on configuration."""
        if config.use_native_file_discovery and config.mode != ExecutionMode.AIDER:
            return "native"
        elif config.mode == ExecutionMode.AIDER:
            return "aider"
        else:
            return "fallback"

    @staticmethod
    def get_editing_strategy(config: ExecutionConfig) -> str:
        """Get the editing strategy based on configuration."""
        if config.use_native_editing and config.mode != ExecutionMode.AIDER:
            return "native"
        elif config.mode == ExecutionMode.AIDER:
            return "aider"
        else:
            return "fallback"

    @staticmethod
    def get_validation_strategy(config: ExecutionConfig) -> str:
        """Get the validation strategy based on configuration."""
        if config.use_native_validation and config.mode != ExecutionMode.AIDER:
            return "native"
        elif config.mode == ExecutionMode.AIDER:
            return "aider"
        else:
            return "fallback"


# Global configuration instance
_config: ExecutionConfig | None = None


def get_execution_config() -> ExecutionConfig:
    """Get the global execution configuration (singleton pattern)."""
    global _config
    if _config is None:
        _config = ExecutionConfigManager.get_config()
    return _config


def reset_execution_config():
    """Reset the global configuration (useful for testing)."""
    global _config
    _config = None


def set_execution_config(config: ExecutionConfig):
    """Set the global execution configuration (useful for testing)."""
    global _config
    _config = config


# Convenience functions for common checks
def is_native_mode() -> bool:
    """Check if we're in native mode."""
    config = get_execution_config()
    return ExecutionConfigManager.should_use_native_tools(config)


def is_aider_mode() -> bool:
    """Check if we're in Aider mode."""
    config = get_execution_config()
    return ExecutionConfigManager.should_use_aider_tools(config)


def is_hybrid_mode() -> bool:
    """Check if we're in hybrid mode."""
    config = get_execution_config()
    return config.mode == ExecutionMode.HYBRID


def get_file_discovery_strategy() -> str:
    """Get the current file discovery strategy."""
    config = get_execution_config()
    return ExecutionConfigManager.get_file_discovery_strategy(config)


def get_editing_strategy() -> str:
    """Get the current editing strategy."""
    config = get_execution_config()
    return ExecutionConfigManager.get_editing_strategy(config)


def get_validation_strategy() -> str:
    """Get the current validation strategy."""
    config = get_execution_config()
    return ExecutionConfigManager.get_validation_strategy(config)
