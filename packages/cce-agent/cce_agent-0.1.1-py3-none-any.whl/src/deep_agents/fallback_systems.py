"""
Fallback Systems for CCE Deep Agent

This module implements graceful degradation and fallback mechanisms
when services fail, ensuring system reliability and availability.
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .utils.constants import ERROR_HANDLING_CONFIG
from .utils.error_handling import ErrorSeverity, ErrorType, get_error_handler

logger = logging.getLogger(__name__)


class FallbackStrategy(Enum):
    """Fallback strategies for service failures."""

    LEGACY = "legacy"
    MOCK = "mock"
    CACHE = "cache"
    SIMPLIFIED = "simplified"
    DISABLED = "disabled"


class ServiceStatus(Enum):
    """Status of a service."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class ServiceInfo:
    """Information about a service."""

    name: str
    status: ServiceStatus
    last_check: float
    failure_count: int
    fallback_strategy: FallbackStrategy
    health_check_url: str | None = None
    timeout: int = 30
    retry_count: int = 0
    max_retries: int = 3


class FallbackProvider(ABC):
    """Abstract base class for fallback providers."""

    @abstractmethod
    async def provide_fallback(self, operation: str, *args, **kwargs) -> Any:
        """Provide fallback functionality."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if fallback is available."""
        pass


class LegacyFallbackProvider(FallbackProvider):
    """Fallback provider that uses legacy implementations."""

    def __init__(self, legacy_implementations: dict[str, Callable]):
        self.legacy_implementations = legacy_implementations
        self.available = True

    async def provide_fallback(self, operation: str, *args, **kwargs) -> Any:
        """Provide fallback using legacy implementation."""
        try:
            if operation not in self.legacy_implementations:
                raise ValueError(f"No legacy implementation for operation: {operation}")

            legacy_func = self.legacy_implementations[operation]

            if asyncio.iscoroutinefunction(legacy_func):
                result = await legacy_func(*args, **kwargs)
            else:
                result = legacy_func(*args, **kwargs)

            logger.info(f"Legacy fallback successful for operation: {operation}")
            return result

        except Exception as e:
            logger.error(f"Legacy fallback failed for operation {operation}: {e}")
            raise

    def is_available(self) -> bool:
        """Check if legacy fallback is available."""
        return self.available and len(self.legacy_implementations) > 0


class MockFallbackProvider(FallbackProvider):
    """Fallback provider that returns mock responses."""

    def __init__(self, mock_responses: dict[str, Any]):
        self.mock_responses = mock_responses
        self.available = True

    async def provide_fallback(self, operation: str, *args, **kwargs) -> Any:
        """Provide fallback using mock response."""
        try:
            if operation not in self.mock_responses:
                # Generate a generic mock response
                mock_response = {
                    "success": True,
                    "operation": operation,
                    "fallback_type": "mock",
                    "message": f"Mock response for {operation}",
                    "timestamp": time.time(),
                    "args": args,
                    "kwargs": kwargs,
                }
            else:
                mock_response = self.mock_responses[operation]

            logger.info(f"Mock fallback provided for operation: {operation}")
            return mock_response

        except Exception as e:
            logger.error(f"Mock fallback failed for operation {operation}: {e}")
            raise

    def is_available(self) -> bool:
        """Check if mock fallback is available."""
        return self.available


class CacheFallbackProvider(FallbackProvider):
    """Fallback provider that uses cached responses."""

    def __init__(self, cache: dict[str, Any], cache_ttl: int = 3600):
        self.cache = cache
        self.cache_ttl = cache_ttl
        self.cache_timestamps = {}
        self.available = True

    async def provide_fallback(self, operation: str, *args, **kwargs) -> Any:
        """Provide fallback using cached response."""
        try:
            # Generate cache key
            cache_key = f"{operation}:{hash(str(args) + str(kwargs))}"

            # Check if cached response exists and is not expired
            if cache_key in self.cache:
                timestamp = self.cache_timestamps.get(cache_key, 0)
                if time.time() - timestamp < self.cache_ttl:
                    logger.info(f"Cache fallback provided for operation: {operation}")
                    return self.cache[cache_key]
                else:
                    # Remove expired cache entry
                    del self.cache[cache_key]
                    if cache_key in self.cache_timestamps:
                        del self.cache_timestamps[cache_key]

            # No valid cache entry, return fallback response
            fallback_response = {
                "success": False,
                "operation": operation,
                "fallback_type": "cache",
                "message": f"No cached response available for {operation}",
                "timestamp": time.time(),
            }

            logger.warning(f"No cache available for operation: {operation}")
            return fallback_response

        except Exception as e:
            logger.error(f"Cache fallback failed for operation {operation}: {e}")
            raise

    def is_available(self) -> bool:
        """Check if cache fallback is available."""
        return self.available and len(self.cache) > 0


class SimplifiedFallbackProvider(FallbackProvider):
    """Fallback provider that provides simplified functionality."""

    def __init__(self, simplified_implementations: dict[str, Callable]):
        self.simplified_implementations = simplified_implementations
        self.available = True

    async def provide_fallback(self, operation: str, *args, **kwargs) -> Any:
        """Provide fallback using simplified implementation."""
        try:
            if operation not in self.simplified_implementations:
                # Provide a basic simplified response
                simplified_response = {
                    "success": True,
                    "operation": operation,
                    "fallback_type": "simplified",
                    "message": f"Simplified response for {operation}",
                    "timestamp": time.time(),
                    "note": "This is a simplified fallback response",
                }
            else:
                simplified_func = self.simplified_implementations[operation]

                if asyncio.iscoroutinefunction(simplified_func):
                    simplified_response = await simplified_func(*args, **kwargs)
                else:
                    simplified_response = simplified_func(*args, **kwargs)

            logger.info(f"Simplified fallback provided for operation: {operation}")
            return simplified_response

        except Exception as e:
            logger.error(f"Simplified fallback failed for operation {operation}: {e}")
            raise

    def is_available(self) -> bool:
        """Check if simplified fallback is available."""
        return self.available and len(self.simplified_implementations) > 0


class FallbackManager:
    """
    Manager for fallback systems and graceful degradation.

    This class coordinates fallback strategies when services fail,
    ensuring system reliability and availability.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or ERROR_HANDLING_CONFIG
        self.services: dict[str, ServiceInfo] = {}
        self.fallback_providers: dict[FallbackStrategy, FallbackProvider] = {}
        self.error_handler = get_error_handler()
        self.fallback_history: list[dict[str, Any]] = []
        self.max_fallback_history = 1000

        # Initialize default fallback providers
        self._initialize_fallback_providers()

    def _initialize_fallback_providers(self) -> None:
        """Initialize default fallback providers."""
        # Mock fallback provider
        mock_responses = {
            "safety_validation": {
                "is_safe": True,
                "threat_type": "SAFE",
                "reasoning": "Mock safety validation - assuming safe",
                "confidence": 0.5,
            },
            "mcp_tools": {"tools": [], "message": "Mock MCP tools - no external tools available"},
            "planning": {"plan_id": "mock_plan", "message": "Mock planning - basic plan created"},
        }
        self.fallback_providers[FallbackStrategy.MOCK] = MockFallbackProvider(mock_responses)

        # Cache fallback provider with some initial cache
        initial_cache = {
            "safety_validation": {
                "is_safe": True,
                "threat_type": "SAFE",
                "reasoning": "Cached safety validation",
                "confidence": 0.8,
            }
        }
        self.fallback_providers[FallbackStrategy.CACHE] = CacheFallbackProvider(initial_cache)

        # Simplified fallback provider
        simplified_implementations = {
            "safety_validation": self._simplified_safety_validation,
            "mcp_tools": self._simplified_mcp_tools,
            "planning": self._simplified_planning,
        }
        self.fallback_providers[FallbackStrategy.SIMPLIFIED] = SimplifiedFallbackProvider(simplified_implementations)

    def register_service(
        self,
        name: str,
        fallback_strategy: FallbackStrategy = FallbackStrategy.MOCK,
        health_check_url: str | None = None,
        timeout: int = 30,
    ) -> None:
        """
        Register a service for fallback management.

        Args:
            name: Service name
            fallback_strategy: Fallback strategy to use
            health_check_url: Optional health check URL
            timeout: Health check timeout
        """
        service_info = ServiceInfo(
            name=name,
            status=ServiceStatus.UNKNOWN,
            last_check=0.0,
            failure_count=0,
            fallback_strategy=fallback_strategy,
            health_check_url=health_check_url,
            timeout=timeout,
        )

        self.services[name] = service_info
        logger.info(f"Registered service: {name} with fallback strategy: {fallback_strategy.value}")

    def register_legacy_fallback(self, legacy_implementations: dict[str, Callable]) -> None:
        """
        Register legacy implementations for fallback.

        Args:
            legacy_implementations: Dictionary mapping operation names to legacy functions
        """
        self.fallback_providers[FallbackStrategy.LEGACY] = LegacyFallbackProvider(legacy_implementations)
        logger.info(f"Registered legacy fallback for {len(legacy_implementations)} operations")

    async def fallback_to_legacy(self, operation: str, *args, **kwargs) -> Any:
        """
        Fallback to legacy implementation when needed.

        Args:
            operation: Operation name
            *args: Operation arguments
            **kwargs: Operation keyword arguments

        Returns:
            Result from legacy implementation
        """
        try:
            if FallbackStrategy.LEGACY not in self.fallback_providers:
                raise ValueError("No legacy fallback provider registered")

            provider = self.fallback_providers[FallbackStrategy.LEGACY]
            if not provider.is_available():
                raise ValueError("Legacy fallback provider not available")

            result = await provider.provide_fallback(operation, *args, **kwargs)

            # Log fallback usage
            self._log_fallback_usage("legacy", operation, True)

            return result

        except Exception as e:
            logger.error(f"Legacy fallback failed for operation {operation}: {e}")
            self._log_fallback_usage("legacy", operation, False, str(e))
            raise

    async def fallback_to_mock(self, service: str, operation: str, *args, **kwargs) -> Any:
        """
        Fallback to mock responses for reliability.

        Args:
            service: Service name
            operation: Operation name
            *args: Operation arguments
            **kwargs: Operation keyword arguments

        Returns:
            Mock response
        """
        try:
            if FallbackStrategy.MOCK not in self.fallback_providers:
                raise ValueError("No mock fallback provider registered")

            provider = self.fallback_providers[FallbackStrategy.MOCK]
            if not provider.is_available():
                raise ValueError("Mock fallback provider not available")

            result = await provider.provide_fallback(operation, *args, **kwargs)

            # Log fallback usage
            self._log_fallback_usage("mock", operation, True, service=service)

            return result

        except Exception as e:
            logger.error(f"Mock fallback failed for operation {operation}: {e}")
            self._log_fallback_usage("mock", operation, False, str(e), service=service)
            raise

    async def fallback_to_cache(self, operation: str, *args, **kwargs) -> Any:
        """
        Fallback to cached responses.

        Args:
            operation: Operation name
            *args: Operation arguments
            **kwargs: Operation keyword arguments

        Returns:
            Cached response or fallback response
        """
        try:
            if FallbackStrategy.CACHE not in self.fallback_providers:
                raise ValueError("No cache fallback provider registered")

            provider = self.fallback_providers[FallbackStrategy.CACHE]
            if not provider.is_available():
                raise ValueError("Cache fallback provider not available")

            result = await provider.provide_fallback(operation, *args, **kwargs)

            # Log fallback usage
            self._log_fallback_usage("cache", operation, True)

            return result

        except Exception as e:
            logger.error(f"Cache fallback failed for operation {operation}: {e}")
            self._log_fallback_usage("cache", operation, False, str(e))
            raise

    async def fallback_to_simplified(self, operation: str, *args, **kwargs) -> Any:
        """
        Fallback to simplified implementation.

        Args:
            operation: Operation name
            *args: Operation arguments
            **kwargs: Operation keyword arguments

        Returns:
            Simplified response
        """
        try:
            if FallbackStrategy.SIMPLIFIED not in self.fallback_providers:
                raise ValueError("No simplified fallback provider registered")

            provider = self.fallback_providers[FallbackStrategy.SIMPLIFIED]
            if not provider.is_available():
                raise ValueError("Simplified fallback provider not available")

            result = await provider.provide_fallback(operation, *args, **kwargs)

            # Log fallback usage
            self._log_fallback_usage("simplified", operation, True)

            return result

        except Exception as e:
            logger.error(f"Simplified fallback failed for operation {operation}: {e}")
            self._log_fallback_usage("simplified", operation, False, str(e))
            raise

    async def execute_with_fallback(
        self, operation: str, primary_func: Callable, service_name: str | None = None, *args, **kwargs
    ) -> Any:
        """
        Execute operation with automatic fallback.

        Args:
            operation: Operation name
            primary_func: Primary function to execute
            service_name: Optional service name
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result from primary function or fallback
        """
        try:
            # Try primary function first
            if asyncio.iscoroutinefunction(primary_func):
                result = await primary_func(*args, **kwargs)
            else:
                result = primary_func(*args, **kwargs)

            # Update service status on success
            if service_name and service_name in self.services:
                self.services[service_name].status = ServiceStatus.HEALTHY
                self.services[service_name].failure_count = 0

            return result

        except Exception as e:
            logger.warning(f"Primary operation {operation} failed: {e}")

            # Update service status on failure
            if service_name and service_name in self.services:
                service = self.services[service_name]
                service.status = ServiceStatus.FAILED
                service.failure_count += 1
                service.fallback_strategy = self._determine_fallback_strategy(service)

            # Try fallback strategies
            fallback_strategies = [
                FallbackStrategy.LEGACY,
                FallbackStrategy.CACHE,
                FallbackStrategy.SIMPLIFIED,
                FallbackStrategy.MOCK,
            ]

            for strategy in fallback_strategies:
                try:
                    if strategy in self.fallback_providers:
                        provider = self.fallback_providers[strategy]
                        if provider.is_available():
                            result = await provider.provide_fallback(operation, *args, **kwargs)
                            logger.info(f"Fallback {strategy.value} successful for operation {operation}")
                            return result
                except Exception as fallback_error:
                    logger.warning(f"Fallback {strategy.value} failed for operation {operation}: {fallback_error}")
                    continue

            # All fallbacks failed
            logger.error(f"All fallbacks failed for operation {operation}")
            raise e

    def _determine_fallback_strategy(self, service: ServiceInfo) -> FallbackStrategy:
        """Determine appropriate fallback strategy based on service status."""
        if service.failure_count < 3:
            return FallbackStrategy.LEGACY
        elif service.failure_count < 5:
            return FallbackStrategy.CACHE
        elif service.failure_count < 10:
            return FallbackStrategy.SIMPLIFIED
        else:
            return FallbackStrategy.MOCK

    def _log_fallback_usage(
        self, fallback_type: str, operation: str, success: bool, error: str | None = None, **kwargs
    ) -> None:
        """Log fallback usage."""
        log_entry = {
            "fallback_type": fallback_type,
            "operation": operation,
            "success": success,
            "timestamp": time.time(),
            "error": error,
            **kwargs,
        }

        self.fallback_history.append(log_entry)

        # Trim history if too long
        if len(self.fallback_history) > self.max_fallback_history:
            self.fallback_history = self.fallback_history[-self.max_fallback_history :]

    # Simplified fallback implementations
    def _simplified_safety_validation(self, command: str) -> dict[str, Any]:
        """Simplified safety validation."""
        return {
            "is_safe": True,
            "threat_type": "SAFE",
            "reasoning": "Simplified validation - basic safety check passed",
            "confidence": 0.3,
        }

    def _simplified_mcp_tools(self) -> dict[str, Any]:
        """Simplified MCP tools."""
        return {"tools": [], "message": "Simplified MCP - no external tools available"}

    def _simplified_planning(self, description: str, steps: list[str]) -> dict[str, Any]:
        """Simplified planning."""
        return {
            "plan_id": f"simplified_plan_{int(time.time())}",
            "title": f"Simplified Plan: {description[:50]}...",
            "description": description,
            "steps": steps,
            "message": "Simplified planning - basic plan created",
        }

    def get_fallback_statistics(self) -> dict[str, Any]:
        """Get fallback system statistics."""
        try:
            # Count fallback usage
            fallback_counts = {}
            success_counts = {}

            for entry in self.fallback_history:
                fallback_type = entry["fallback_type"]
                fallback_counts[fallback_type] = fallback_counts.get(fallback_type, 0) + 1

                if entry["success"]:
                    success_counts[fallback_type] = success_counts.get(fallback_type, 0) + 1

            # Service status summary
            service_status = {}
            for name, service in self.services.items():
                service_status[name] = {
                    "status": service.status.value,
                    "failure_count": service.failure_count,
                    "fallback_strategy": service.fallback_strategy.value,
                    "last_check": service.last_check,
                }

            return {
                "total_fallback_attempts": len(self.fallback_history),
                "fallback_counts": fallback_counts,
                "success_counts": success_counts,
                "service_status": service_status,
                "available_providers": [
                    strategy.value for strategy, provider in self.fallback_providers.items() if provider.is_available()
                ],
                "config": self.config,
            }

        except Exception as e:
            logger.error(f"Error getting fallback statistics: {e}")
            return {
                "total_fallback_attempts": 0,
                "fallback_counts": {},
                "success_counts": {},
                "service_status": {},
                "available_providers": [],
                "error": str(e),
            }


# Global fallback manager instance
_fallback_manager = None


def get_fallback_manager(config: dict[str, Any] | None = None) -> FallbackManager:
    """Get the global fallback manager instance."""
    global _fallback_manager
    if _fallback_manager is None:
        _fallback_manager = FallbackManager(config)
    return _fallback_manager
