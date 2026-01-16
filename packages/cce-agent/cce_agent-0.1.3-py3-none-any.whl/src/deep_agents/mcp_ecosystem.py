"""
Advanced MCP Ecosystem Integration for CCE Deep Agent

This module provides advanced MCP ecosystem management with multiple server
connections, tool discovery, and comprehensive monitoring capabilities.
"""

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

logger = logging.getLogger(__name__)


class ServerStatus(Enum):
    """Status of MCP server connection."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class ToolStatus(Enum):
    """Status of MCP tool."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"
    DEPRECATED = "deprecated"


@dataclass
class ServerConfig:
    """Configuration for MCP server connection."""

    name: str
    command: str
    args: list[str]
    env: dict[str, str] | None = None
    timeout: int = 30
    retry_count: int = 3
    health_check_interval: int = 60
    priority: int = 1  # 1 = highest priority
    tags: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolInfo:
    """Information about an MCP tool."""

    name: str
    server: str
    description: str
    status: ToolStatus = ToolStatus.AVAILABLE
    last_used: float | None = None
    usage_count: int = 0
    error_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EcosystemStats:
    """Statistics for the MCP ecosystem."""

    total_servers: int = 0
    connected_servers: int = 0
    total_tools: int = 0
    available_tools: int = 0
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    uptime: float = 0.0


class MCPEcosystem:
    """
    Advanced MCP ecosystem manager with multiple server connections.

    This class provides comprehensive MCP ecosystem management including
    server connection management, tool discovery, health monitoring,
    and performance optimization.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.servers: dict[str, ServerConfig] = {}
        self.server_status: dict[str, ServerStatus] = {}
        self.server_connections: dict[str, Any] = {}
        self.tool_registry: dict[str, ToolInfo] = {}
        self.tool_usage_stats: dict[str, dict[str, Any]] = {}
        self.health_check_tasks: dict[str, asyncio.Task] = {}
        self.ecosystem_stats = EcosystemStats()
        self.start_time = time.time()
        self.request_history: list[dict[str, Any]] = []
        self.max_history_size = 1000

    async def register_server(self, config: ServerConfig) -> bool:
        """
        Register an MCP server configuration.

        Args:
            config: MCP server configuration

        Returns:
            True if server was registered successfully
        """
        try:
            self.servers[config.name] = config
            self.server_status[config.name] = ServerStatus.DISCONNECTED
            self.ecosystem_stats.total_servers += 1

            logger.info(f"Registered MCP server: {config.name} (priority: {config.priority})")
            return True

        except Exception as e:
            logger.error(f"Failed to register MCP server {config.name}: {e}")
            return False

    async def connect_server(self, server_name: str) -> bool:
        """
        Connect to an MCP server.

        Args:
            server_name: Name of the server to connect to

        Returns:
            True if connection was successful
        """
        if server_name not in self.servers:
            logger.error(f"Server {server_name} not registered")
            return False

        try:
            self.server_status[server_name] = ServerStatus.CONNECTING
            config = self.servers[server_name]

            # Simulate MCP server connection with retry logic
            for attempt in range(config.retry_count):
                try:
                    # Simulate connection time based on priority
                    connection_delay = 0.1 / config.priority
                    await asyncio.sleep(connection_delay)

                    # Simulate connection success/failure based on priority
                    if config.priority >= 1:
                        self.server_status[server_name] = ServerStatus.CONNECTED
                        self.server_connections[server_name] = {
                            "config": config,
                            "connected_at": time.time(),
                            "last_health_check": time.time(),
                            "connection_attempts": attempt + 1,
                        }

                        # Start health check task
                        self.health_check_tasks[server_name] = asyncio.create_task(self._health_check_loop(server_name))

                        self.ecosystem_stats.connected_servers += 1
                        logger.info(f"Connected to MCP server: {server_name} (attempt {attempt + 1})")
                        return True
                    else:
                        raise Exception("Low priority server connection failed")

                except Exception as e:
                    if attempt < config.retry_count - 1:
                        logger.warning(f"Connection attempt {attempt + 1} failed for {server_name}: {e}")
                        await asyncio.sleep(2**attempt)  # Exponential backoff
                    else:
                        raise e

            return False

        except Exception as e:
            self.server_status[server_name] = ServerStatus.ERROR
            logger.error(f"Failed to connect to MCP server {server_name}: {e}")
            return False

    async def disconnect_server(self, server_name: str) -> bool:
        """
        Disconnect from an MCP server.

        Args:
            server_name: Name of the server to disconnect from

        Returns:
            True if disconnection was successful
        """
        try:
            # Cancel health check task
            if server_name in self.health_check_tasks:
                self.health_check_tasks[server_name].cancel()
                del self.health_check_tasks[server_name]

            # Remove server connection
            if server_name in self.server_connections:
                del self.server_connections[server_name]

            # Update server status
            self.server_status[server_name] = ServerStatus.DISCONNECTED
            self.ecosystem_stats.connected_servers -= 1

            # Remove tools from this server
            tools_to_remove = [
                tool_name for tool_name, tool_info in self.tool_registry.items() if tool_info.server == server_name
            ]
            for tool_name in tools_to_remove:
                del self.tool_registry[tool_name]
                self.ecosystem_stats.total_tools -= 1

            logger.info(f"Disconnected from MCP server: {server_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to disconnect from MCP server {server_name}: {e}")
            return False

    async def discover_tools(self, server_name: str | None = None) -> dict[str, list[ToolInfo]]:
        """
        Discover and register tools from MCP servers.

        Args:
            server_name: Optional specific server name, if None discovers from all connected servers

        Returns:
            Dictionary mapping server names to their discovered tools
        """
        try:
            discovered_tools = {}

            servers_to_check = [server_name] if server_name else list(self.server_connections.keys())

            for server in servers_to_check:
                if server not in self.server_connections:
                    continue

                # Simulate tool discovery
                server_tools = []
                tool_count = 3 + (self.servers[server].priority * 2)  # More tools for higher priority servers

                for i in range(tool_count):
                    tool_name = f"{server}_tool_{i + 1}"
                    tool_info = ToolInfo(
                        name=tool_name,
                        server=server,
                        description=f"Tool {i + 1} from {server} server",
                        metadata={
                            "category": f"category_{i % 3}",
                            "version": "1.0.0",
                            "priority": self.servers[server].priority,
                        },
                    )

                    # Register tool
                    self.tool_registry[tool_name] = tool_info
                    server_tools.append(tool_info)
                    self.ecosystem_stats.total_tools += 1

                discovered_tools[server] = server_tools
                logger.info(f"Discovered {len(server_tools)} tools from server {server}")

            # Update available tools count
            self.ecosystem_stats.available_tools = len(
                [tool for tool in self.tool_registry.values() if tool.status == ToolStatus.AVAILABLE]
            )

            return discovered_tools

        except Exception as e:
            logger.error(f"Failed to discover tools: {e}")
            return {}

    def get_available_tools(self, server_name: str | None = None, category: str | None = None) -> list[ToolInfo]:
        """
        Get list of available external tools.

        Args:
            server_name: Optional specific server name
            category: Optional tool category filter

        Returns:
            List of available tools
        """
        try:
            tools = []

            for tool_name, tool_info in self.tool_registry.items():
                # Filter by server if specified
                if server_name and tool_info.server != server_name:
                    continue

                # Filter by category if specified
                if category and tool_info.metadata.get("category") != category:
                    continue

                # Only include available tools
                if tool_info.status == ToolStatus.AVAILABLE:
                    tools.append(tool_info)

            # Sort by priority and usage count
            tools.sort(key=lambda t: (-self.servers[t.server].priority, -t.usage_count, t.name))

            return tools

        except Exception as e:
            logger.error(f"Failed to get available tools: {e}")
            return []

    async def execute_tool(self, tool_name: str, args: dict[str, Any]) -> Any:
        """
        Execute a tool from an MCP server.

        Args:
            tool_name: Name of the tool to execute
            args: Arguments for the tool

        Returns:
            Tool execution result
        """
        start_time = time.time()

        try:
            if tool_name not in self.tool_registry:
                raise ValueError(f"Tool {tool_name} not found in registry")

            tool_info = self.tool_registry[tool_name]
            server_name = tool_info.server

            if server_name not in self.server_connections:
                raise ValueError(f"Server {server_name} is not connected")

            # Update tool usage stats
            tool_info.last_used = time.time()
            tool_info.usage_count += 1

            # Update ecosystem stats
            self.ecosystem_stats.total_requests += 1

            # Simulate tool execution with performance based on server priority
            server_priority = self.servers[server_name].priority
            execution_delay = 0.1 / server_priority
            await asyncio.sleep(execution_delay)

            # Simulate success/failure based on server priority
            if server_priority >= 1:
                result = {
                    "tool_name": tool_name,
                    "server": server_name,
                    "args": args,
                    "result": f"Executed {tool_name} with args {args}",
                    "executed_at": time.time(),
                    "execution_time": time.time() - start_time,
                    "server_priority": server_priority,
                }

                # Update success stats
                self.ecosystem_stats.successful_requests += 1

                # Update average response time
                response_time = time.time() - start_time
                self._update_average_response_time(response_time)

                # Add to request history
                self._add_to_request_history(
                    {
                        "tool_name": tool_name,
                        "server": server_name,
                        "success": True,
                        "response_time": response_time,
                        "timestamp": time.time(),
                    }
                )

                logger.info(f"Executed MCP tool {tool_name} on server {server_name} in {response_time:.3f}s")
                return result
            else:
                raise Exception("Low priority server execution failed")

        except Exception as e:
            # Update failure stats
            self.ecosystem_stats.failed_requests += 1

            # Update tool error count
            if tool_name in self.tool_registry:
                self.tool_registry[tool_name].error_count += 1

            # Add to request history
            self._add_to_request_history(
                {
                    "tool_name": tool_name,
                    "server": tool_info.server if tool_name in self.tool_registry else "unknown",
                    "success": False,
                    "error": str(e),
                    "response_time": time.time() - start_time,
                    "timestamp": time.time(),
                }
            )

            logger.error(f"Failed to execute MCP tool {tool_name}: {e}")
            raise

    async def _health_check_loop(self, server_name: str) -> None:
        """Health check loop for a server."""
        try:
            while True:
                await asyncio.sleep(self.servers[server_name].health_check_interval)

                if server_name not in self.server_connections:
                    break

                # Simulate health check
                health_status = await self._perform_health_check(server_name)

                if not health_status["healthy"]:
                    logger.warning(f"Health check failed for server {server_name}: {health_status['error']}")
                    self.server_status[server_name] = ServerStatus.ERROR
                else:
                    self.server_status[server_name] = ServerStatus.CONNECTED
                    self.server_connections[server_name]["last_health_check"] = time.time()

        except asyncio.CancelledError:
            logger.info(f"Health check loop cancelled for server {server_name}")
        except Exception as e:
            logger.error(f"Health check loop error for server {server_name}: {e}")

    async def _perform_health_check(self, server_name: str) -> dict[str, Any]:
        """Perform health check on a server."""
        try:
            # Simulate health check
            await asyncio.sleep(0.01)

            # Simulate health check result based on server priority
            server_priority = self.servers[server_name].priority
            is_healthy = server_priority >= 1

            return {
                "healthy": is_healthy,
                "response_time": 0.01,
                "timestamp": time.time(),
                "error": None if is_healthy else "Low priority server health check failed",
            }

        except Exception as e:
            return {"healthy": False, "response_time": 0.0, "timestamp": time.time(), "error": str(e)}

    def _update_average_response_time(self, response_time: float) -> None:
        """Update average response time."""
        if self.ecosystem_stats.total_requests == 1:
            self.ecosystem_stats.average_response_time = response_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.ecosystem_stats.average_response_time = (
                alpha * response_time + (1 - alpha) * self.ecosystem_stats.average_response_time
            )

    def _add_to_request_history(self, request_info: dict[str, Any]) -> None:
        """Add request to history."""
        self.request_history.append(request_info)

        # Trim history if too long
        if len(self.request_history) > self.max_history_size:
            self.request_history = self.request_history[-self.max_history_size :]

    def get_ecosystem_stats(self) -> EcosystemStats:
        """Get ecosystem statistics."""
        self.ecosystem_stats.uptime = time.time() - self.start_time
        return self.ecosystem_stats

    def get_server_status(self, server_name: str | None = None) -> ServerStatus | dict[str, ServerStatus]:
        """Get status of MCP servers."""
        if server_name:
            return self.server_status.get(server_name, ServerStatus.DISCONNECTED)
        return self.server_status.copy()

    def get_tool_usage_stats(self) -> dict[str, dict[str, Any]]:
        """Get tool usage statistics."""
        return {
            tool_name: {
                "usage_count": tool_info.usage_count,
                "error_count": tool_info.error_count,
                "last_used": tool_info.last_used,
                "server": tool_info.server,
                "status": tool_info.status.value,
            }
            for tool_name, tool_info in self.tool_registry.items()
        }

    def get_request_history(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get recent request history."""
        return self.request_history[-limit:]

    async def optimize_ecosystem(self) -> dict[str, Any]:
        """Optimize ecosystem performance."""
        try:
            optimizations = {"servers_optimized": 0, "tools_optimized": 0, "performance_improvements": []}

            # Optimize server connections
            for server_name, connection in self.server_connections.items():
                if connection["connection_attempts"] > 1:
                    # Server had connection issues, consider reconnection
                    optimizations["servers_optimized"] += 1
                    optimizations["performance_improvements"].append(
                        f"Server {server_name} had connection issues, consider reconnection"
                    )

            # Optimize tool usage
            for tool_name, tool_info in self.tool_registry.items():
                if tool_info.error_count > tool_info.usage_count * 0.1:  # >10% error rate
                    optimizations["tools_optimized"] += 1
                    optimizations["performance_improvements"].append(
                        f"Tool {tool_name} has high error rate ({tool_info.error_count}/{tool_info.usage_count})"
                    )

            return optimizations

        except Exception as e:
            logger.error(f"Failed to optimize ecosystem: {e}")
            return {"error": str(e)}

    async def shutdown(self) -> None:
        """Shutdown the ecosystem."""
        try:
            # Cancel all health check tasks
            for task in self.health_check_tasks.values():
                task.cancel()

            # Wait for tasks to complete
            if self.health_check_tasks:
                await asyncio.gather(*self.health_check_tasks.values(), return_exceptions=True)

            # Disconnect all servers
            for server_name in list(self.server_connections.keys()):
                await self.disconnect_server(server_name)

            logger.info("MCP ecosystem shutdown complete")

        except Exception as e:
            logger.error(f"Error during ecosystem shutdown: {e}")


# Global MCP ecosystem instance
_mcp_ecosystem = None


def get_mcp_ecosystem(config: dict[str, Any] | None = None) -> MCPEcosystem:
    """Get the global MCP ecosystem instance."""
    global _mcp_ecosystem
    if _mcp_ecosystem is None:
        _mcp_ecosystem = MCPEcosystem(config)
    return _mcp_ecosystem


async def initialize_mcp_ecosystem() -> bool:
    """
    Initialize the MCP ecosystem with default servers.

    Returns:
        True if initialization was successful
    """
    try:
        ecosystem = get_mcp_ecosystem()

        # Example server configurations with different priorities
        default_servers = [
            ServerConfig(
                name="filesystem",
                command="mcp-server-filesystem",
                args=["--root", "/tmp"],
                env={"MCP_SERVER_FILESYSTEM_ROOT": "/tmp"},
                priority=3,
                tags={"filesystem", "storage"},
            ),
            ServerConfig(
                name="git",
                command="mcp-server-git",
                args=["--repo", "."],
                env={"MCP_SERVER_GIT_REPO": "."},
                priority=2,
                tags={"git", "version-control"},
            ),
            ServerConfig(
                name="database",
                command="mcp-server-database",
                args=["--host", "localhost"],
                priority=1,
                tags={"database", "storage"},
            ),
        ]

        # Register and connect servers
        for config in default_servers:
            await ecosystem.register_server(config)
            await ecosystem.connect_server(config.name)

        # Discover tools from all servers
        await ecosystem.discover_tools()

        logger.info("MCP ecosystem initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize MCP ecosystem: {e}")
        return False
