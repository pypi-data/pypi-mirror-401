"""
Error Handling and Timeout Protection for CCE Deep Agent

This module provides comprehensive error handling, timeout protection,
and graceful degradation for the CCE agent system.
"""

import asyncio
import logging
import time
import traceback
from collections.abc import Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .constants import ERROR_HANDLING_CONFIG

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorType(Enum):
    """Types of errors."""

    TIMEOUT = "timeout"
    TOOL_FAILURE = "tool_failure"
    VALIDATION_ERROR = "validation_error"
    NETWORK_ERROR = "network_error"
    PERMISSION_ERROR = "permission_error"
    RESOURCE_ERROR = "resource_error"
    UNKNOWN_ERROR = "unknown_error"


@dataclass
class ErrorContext:
    """Context information for error handling."""

    error_type: ErrorType
    severity: ErrorSeverity
    operation: str
    tool_name: str | None = None
    error_message: str = ""
    stack_trace: str = ""
    timestamp: float = 0.0
    retry_count: int = 0
    max_retries: int = 3
    metadata: dict[str, Any] = None


class DeepAgentErrorHandler:
    """
    Comprehensive error handler for deep agent operations.

    This class provides timeout protection, retry logic, and graceful
    error handling for various types of failures.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or ERROR_HANDLING_CONFIG
        self.error_history: list[ErrorContext] = []
        self.max_error_history = 1000
        self.retry_delays = [1, 2, 4, 8, 16]  # Exponential backoff

    async def handle_timeout(self, operation: str, timeout: int, coro: Callable, *args, **kwargs) -> Any:
        """
        Handle operation timeouts gracefully.

        Args:
            operation: Name of the operation
            timeout: Timeout in seconds
            coro: Coroutine to execute
            *args: Arguments for the coroutine
            **kwargs: Keyword arguments for the coroutine

        Returns:
            Result of the operation or None if timeout

        Raises:
            asyncio.TimeoutError: If operation times out
        """
        try:
            result = await asyncio.wait_for(coro(*args, **kwargs), timeout=timeout)
            logger.debug(f"Operation {operation} completed within {timeout}s")
            return result

        except TimeoutError:
            error_context = ErrorContext(
                error_type=ErrorType.TIMEOUT,
                severity=ErrorSeverity.MEDIUM,
                operation=operation,
                error_message=f"Operation {operation} timed out after {timeout} seconds",
                timestamp=time.time(),
            )

            await self._log_error(error_context)
            logger.warning(f"Operation {operation} timed out after {timeout}s")
            raise

        except Exception as e:
            error_context = ErrorContext(
                error_type=ErrorType.UNKNOWN_ERROR,
                severity=ErrorSeverity.HIGH,
                operation=operation,
                error_message=str(e),
                stack_trace=traceback.format_exc(),
                timestamp=time.time(),
            )

            await self._log_error(error_context)
            logger.error(f"Operation {operation} failed: {e}")
            raise

    async def handle_tool_failure(
        self, tool_name: str, error: Exception, operation: str = "tool_execution"
    ) -> dict[str, Any]:
        """
        Handle tool execution failures.

        Args:
            tool_name: Name of the failed tool
            error: Exception that occurred
            operation: Name of the operation

        Returns:
            Error handling result
        """
        try:
            error_context = ErrorContext(
                error_type=ErrorType.TOOL_FAILURE,
                severity=ErrorSeverity.MEDIUM,
                operation=operation,
                tool_name=tool_name,
                error_message=str(error),
                stack_trace=traceback.format_exc(),
                timestamp=time.time(),
            )

            await self._log_error(error_context)

            # Determine if tool failure is recoverable
            is_recoverable = self._is_recoverable_error(error)

            result = {
                "success": False,
                "tool_name": tool_name,
                "error": str(error),
                "error_type": ErrorType.TOOL_FAILURE.value,
                "is_recoverable": is_recoverable,
                "suggestions": self._get_error_suggestions(error, tool_name),
                "timestamp": time.time(),
            }

            if is_recoverable:
                result["retry_recommended"] = True
                result["retry_delay"] = self._get_retry_delay(error_context.retry_count)

            logger.error(f"Tool {tool_name} failed: {error}")
            return result

        except Exception as e:
            logger.error(f"Error handling tool failure: {e}")
            return {
                "success": False,
                "tool_name": tool_name,
                "error": "Error handler failed",
                "original_error": str(error),
                "handler_error": str(e),
                "timestamp": time.time(),
            }

    async def handle_validation_error(
        self, validation_type: str, error: Exception, context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Handle validation errors.

        Args:
            validation_type: Type of validation that failed
            error: Validation error
            context: Validation context

        Returns:
            Error handling result
        """
        try:
            error_context = ErrorContext(
                error_type=ErrorType.VALIDATION_ERROR,
                severity=ErrorSeverity.MEDIUM,
                operation=f"validation_{validation_type}",
                error_message=str(error),
                stack_trace=traceback.format_exc(),
                timestamp=time.time(),
                metadata=context,
            )

            await self._log_error(error_context)

            result = {
                "success": False,
                "validation_type": validation_type,
                "error": str(error),
                "error_type": ErrorType.VALIDATION_ERROR.value,
                "context": context,
                "suggestions": self._get_validation_suggestions(validation_type, error),
                "timestamp": time.time(),
            }

            logger.warning(f"Validation {validation_type} failed: {error}")
            return result

        except Exception as e:
            logger.error(f"Error handling validation error: {e}")
            return {
                "success": False,
                "validation_type": validation_type,
                "error": "Validation error handler failed",
                "original_error": str(error),
                "handler_error": str(e),
                "timestamp": time.time(),
            }

    async def handle_network_error(self, operation: str, error: Exception, retry_count: int = 0) -> dict[str, Any]:
        """
        Handle network-related errors.

        Args:
            operation: Network operation that failed
            error: Network error
            retry_count: Current retry count

        Returns:
            Error handling result
        """
        try:
            error_context = ErrorContext(
                error_type=ErrorType.NETWORK_ERROR,
                severity=ErrorSeverity.MEDIUM,
                operation=operation,
                error_message=str(error),
                stack_trace=traceback.format_exc(),
                timestamp=time.time(),
                retry_count=retry_count,
            )

            await self._log_error(error_context)

            # Network errors are often recoverable
            is_recoverable = retry_count < self.config.get("max_retries", 3)

            result = {
                "success": False,
                "operation": operation,
                "error": str(error),
                "error_type": ErrorType.NETWORK_ERROR.value,
                "retry_count": retry_count,
                "is_recoverable": is_recoverable,
                "retry_delay": self._get_retry_delay(retry_count),
                "timestamp": time.time(),
            }

            if is_recoverable:
                result["retry_recommended"] = True
                result["suggestions"] = [
                    "Check network connectivity",
                    "Verify server availability",
                    "Retry with exponential backoff",
                ]

            logger.warning(f"Network operation {operation} failed (retry {retry_count}): {error}")
            return result

        except Exception as e:
            logger.error(f"Error handling network error: {e}")
            return {
                "success": False,
                "operation": operation,
                "error": "Network error handler failed",
                "original_error": str(error),
                "handler_error": str(e),
                "timestamp": time.time(),
            }

    async def retry_operation(
        self, operation: Callable, *args, max_retries: int | None = None, timeout: int | None = None, **kwargs
    ) -> Any:
        """
        Retry an operation with exponential backoff.

        Args:
            operation: Operation to retry
            *args: Arguments for the operation
            max_retries: Maximum number of retries
            timeout: Timeout for each attempt
            **kwargs: Keyword arguments for the operation

        Returns:
            Result of the operation

        Raises:
            Exception: If all retries fail
        """
        max_retries = max_retries or self.config.get("max_retries", 3)
        timeout = timeout or self.config.get("timeout_seconds", 30)

        last_error = None

        for attempt in range(max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(operation):
                    result = await self.handle_timeout(f"retry_attempt_{attempt}", timeout, operation, *args, **kwargs)
                else:
                    result = operation(*args, **kwargs)

                if attempt > 0:
                    logger.info(f"Operation succeeded on attempt {attempt + 1}")

                return result

            except Exception as e:
                last_error = e

                if attempt < max_retries:
                    delay = self._get_retry_delay(attempt)
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All {max_retries + 1} attempts failed")
                    break

        # All retries failed
        error_context = ErrorContext(
            error_type=ErrorType.UNKNOWN_ERROR,
            severity=ErrorSeverity.HIGH,
            operation="retry_operation",
            error_message=f"Operation failed after {max_retries + 1} attempts: {last_error}",
            stack_trace=traceback.format_exc(),
            timestamp=time.time(),
            retry_count=max_retries,
        )

        await self._log_error(error_context)
        raise last_error

    def _is_recoverable_error(self, error: Exception) -> bool:
        """Determine if an error is recoverable."""
        recoverable_errors = ["timeout", "connection", "network", "temporary", "rate limit", "service unavailable"]

        error_message = str(error).lower()
        return any(recoverable in error_message for recoverable in recoverable_errors)

    def _get_retry_delay(self, retry_count: int) -> int:
        """Get retry delay with exponential backoff."""
        if retry_count < len(self.retry_delays):
            return self.retry_delays[retry_count]
        return self.retry_delays[-1]  # Use max delay

    def _get_error_suggestions(self, error: Exception, tool_name: str) -> list[str]:
        """Get suggestions for resolving an error."""
        error_message = str(error).lower()
        suggestions = []

        if "permission" in error_message:
            suggestions.append("Check file/directory permissions")
            suggestions.append("Verify user has necessary access rights")
        elif "not found" in error_message:
            suggestions.append("Verify file or command exists")
            suggestions.append("Check file path is correct")
        elif "timeout" in error_message:
            suggestions.append("Increase timeout value")
            suggestions.append("Check system performance")
        elif "network" in error_message:
            suggestions.append("Check network connectivity")
            suggestions.append("Verify server is accessible")

        if not suggestions:
            suggestions.append("Review error message for specific details")
            suggestions.append("Check system logs for additional information")

        return suggestions

    def _get_validation_suggestions(self, validation_type: str, error: Exception) -> list[str]:
        """Get suggestions for validation errors."""
        suggestions = []

        if validation_type == "safety":
            suggestions.append("Review command for safety issues")
            suggestions.append("Check for malicious patterns")
        elif validation_type == "syntax":
            suggestions.append("Check syntax and formatting")
            suggestions.append("Validate input parameters")
        elif validation_type == "permissions":
            suggestions.append("Verify user permissions")
            suggestions.append("Check file access rights")

        return suggestions

    async def _log_error(self, error_context: ErrorContext) -> None:
        """Log error context."""
        try:
            # Add to error history
            self.error_history.append(error_context)

            # Trim history if too long
            if len(self.error_history) > self.max_error_history:
                self.error_history = self.error_history[-self.max_error_history :]

            # Log based on severity
            log_message = f"{error_context.error_type.value}: {error_context.error_message}"

            if error_context.severity == ErrorSeverity.CRITICAL:
                logger.critical(log_message)
            elif error_context.severity == ErrorSeverity.HIGH:
                logger.error(log_message)
            elif error_context.severity == ErrorSeverity.MEDIUM:
                logger.warning(log_message)
            else:
                logger.info(log_message)

        except Exception as e:
            logger.error(f"Error logging error context: {e}")

    def get_error_statistics(self) -> dict[str, Any]:
        """Get error handling statistics."""
        try:
            if not self.error_history:
                return {"total_errors": 0, "error_types": {}, "severity_distribution": {}, "recent_errors": []}

            # Count error types
            error_types = {}
            severity_distribution = {}

            for error in self.error_history:
                error_type = error.error_type.value
                severity = error.severity.value

                error_types[error_type] = error_types.get(error_type, 0) + 1
                severity_distribution[severity] = severity_distribution.get(severity, 0) + 1

            # Get recent errors (last 10)
            recent_errors = [
                {
                    "error_type": error.error_type.value,
                    "severity": error.severity.value,
                    "operation": error.operation,
                    "error_message": error.error_message,
                    "timestamp": error.timestamp,
                }
                for error in self.error_history[-10:]
            ]

            return {
                "total_errors": len(self.error_history),
                "error_types": error_types,
                "severity_distribution": severity_distribution,
                "recent_errors": recent_errors,
                "config": self.config,
            }

        except Exception as e:
            logger.error(f"Error getting error statistics: {e}")
            return {
                "total_errors": 0,
                "error_types": {},
                "severity_distribution": {},
                "recent_errors": [],
                "error": str(e),
            }


# Global error handler instance
_error_handler = None


def get_error_handler(config: dict[str, Any] | None = None) -> DeepAgentErrorHandler:
    """Get the global error handler instance."""
    global _error_handler
    if _error_handler is None:
        _error_handler = DeepAgentErrorHandler(config)
    return _error_handler


@asynccontextmanager
async def timeout_protection(operation: str, timeout: int = 30):
    """
    Context manager for timeout protection.

    Args:
        operation: Name of the operation
        timeout: Timeout in seconds

    Yields:
        Error handler for the operation
    """
    error_handler = get_error_handler()

    try:
        yield error_handler
    except TimeoutError:
        await error_handler.handle_timeout(operation, timeout, lambda: None)
        raise
    except Exception as e:
        await error_handler.handle_tool_failure(operation, e)
        raise
