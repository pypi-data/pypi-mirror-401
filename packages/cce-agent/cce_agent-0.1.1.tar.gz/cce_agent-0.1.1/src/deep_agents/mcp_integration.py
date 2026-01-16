"""
MCP Integration for CCE Deep Agent

This module implements Model Context Protocol integration for external tool access,
enabling the CCE agent to connect to external tool ecosystems.
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class MCPServerStatus(Enum):
    """Status of MCP server connection."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class MCPServerConfig:
    """Configuration for MCP server connection."""

    name: str
    command: str
    args: list[str]
    env: dict[str, str] | None = None
    timeout: int = 30


class MCPIntegration:
    """
    Model Context Protocol integration for external tool access.

    This class manages connections to MCP servers and provides access
    to external tools and capabilities.
    """

    def __init__(self):
        self.servers: dict[str, MCPServerConfig] = {}
        self.server_status: dict[str, MCPServerStatus] = {}
        self.tool_registry: dict[str, Any] = {}
        self.connected_servers: dict[str, Any] = {}

    async def register_server(self, config: MCPServerConfig) -> bool:
        """
        Register an MCP server configuration.

        Args:
            config: MCP server configuration

        Returns:
            True if server was registered successfully
        """
        try:
            self.servers[config.name] = config
            self.server_status[config.name] = MCPServerStatus.DISCONNECTED
            logger.info(f"Registered MCP server: {config.name}")
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
            self.server_status[server_name] = MCPServerStatus.CONNECTING
            config = self.servers[server_name]

            # Simulate MCP server connection
            # In a real implementation, this would use the MCP client
            await asyncio.sleep(0.1)  # Simulate connection time

            self.server_status[server_name] = MCPServerStatus.CONNECTED
            self.connected_servers[server_name] = {
                "config": config,
                "tools": [],
                "connected_at": asyncio.get_event_loop().time(),
            }

            logger.info(f"Connected to MCP server: {server_name}")
            return True

        except Exception as e:
            self.server_status[server_name] = MCPServerStatus.ERROR
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
            if server_name in self.connected_servers:
                del self.connected_servers[server_name]

            self.server_status[server_name] = MCPServerStatus.DISCONNECTED
            logger.info(f"Disconnected from MCP server: {server_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to disconnect from MCP server {server_name}: {e}")
            return False

    async def get_mcp_tools(self, server_name: str | None = None) -> list[dict[str, Any]]:
        """
        Get tools from MCP servers.

        Args:
            server_name: Optional specific server name, if None returns tools from all servers

        Returns:
            List of available tools
        """
        try:
            tools = []

            if server_name:
                if server_name in self.connected_servers:
                    # Simulate getting tools from specific server
                    server_tools = [
                        {
                            "name": f"{server_name}_tool_1",
                            "description": f"Tool 1 from {server_name}",
                            "server": server_name,
                        },
                        {
                            "name": f"{server_name}_tool_2",
                            "description": f"Tool 2 from {server_name}",
                            "server": server_name,
                        },
                    ]
                    tools.extend(server_tools)
            else:
                # Get tools from all connected servers
                for name in self.connected_servers:
                    server_tools = await self.get_mcp_tools(name)
                    tools.extend(server_tools)

            return tools

        except Exception as e:
            logger.error(f"Failed to get MCP tools: {e}")
            return []

    async def discover_tools(self) -> dict[str, list[dict[str, Any]]]:
        """
        Discover and register tools from all connected MCP servers.

        Returns:
            Dictionary mapping server names to their tools
        """
        try:
            discovered_tools = {}

            for server_name in self.connected_servers:
                tools = await self.get_mcp_tools(server_name)
                discovered_tools[server_name] = tools

                # Register tools in the tool registry
                for tool in tools:
                    self.tool_registry[tool["name"]] = {
                        "tool": tool,
                        "server": server_name,
                        "registered_at": asyncio.get_event_loop().time(),
                    }

            logger.info(
                f"Discovered {sum(len(tools) for tools in discovered_tools.values())} tools from {len(discovered_tools)} servers"
            )
            return discovered_tools

        except Exception as e:
            logger.error(f"Failed to discover tools: {e}")
            return {}

    def get_available_tools(self) -> list[str]:
        """
        Get list of available external tool names.

        Returns:
            List of available tool names
        """
        return list(self.tool_registry.keys())

    def get_tool_info(self, tool_name: str) -> dict[str, Any] | None:
        """
        Get information about a specific tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool information or None if not found
        """
        return self.tool_registry.get(tool_name)

    def get_server_status(self, server_name: str | None = None) -> MCPServerStatus | dict[str, MCPServerStatus]:
        """
        Get status of MCP servers.

        Args:
            server_name: Optional specific server name

        Returns:
            Server status or dictionary of all server statuses
        """
        if server_name:
            return self.server_status.get(server_name, MCPServerStatus.DISCONNECTED)
        return self.server_status.copy()

    async def execute_tool(self, tool_name: str, args: dict[str, Any]) -> Any:
        """
        Execute a tool from an MCP server.

        Args:
            tool_name: Name of the tool to execute
            args: Arguments for the tool

        Returns:
            Tool execution result
        """
        try:
            if tool_name not in self.tool_registry:
                raise ValueError(f"Tool {tool_name} not found in registry")

            tool_info = self.tool_registry[tool_name]
            server_name = tool_info["server"]

            if server_name not in self.connected_servers:
                raise ValueError(f"Server {server_name} is not connected")

            # Simulate tool execution
            # In a real implementation, this would call the actual MCP tool
            result = {
                "tool_name": tool_name,
                "server": server_name,
                "args": args,
                "result": f"Executed {tool_name} with args {args}",
                "executed_at": asyncio.get_event_loop().time(),
            }

            logger.info(f"Executed MCP tool {tool_name} on server {server_name}")
            return result

        except Exception as e:
            logger.error(f"Failed to execute MCP tool {tool_name}: {e}")
            raise

    async def health_check(self) -> dict[str, Any]:
        """
        Perform health check on all MCP servers.

        Returns:
            Health check results
        """
        try:
            health_results = {
                "overall_status": "healthy",
                "servers": {},
                "total_servers": len(self.servers),
                "connected_servers": len(self.connected_servers),
                "total_tools": len(self.tool_registry),
            }

            for server_name, status in self.server_status.items():
                server_health = {
                    "status": status.value,
                    "connected": status == MCPServerStatus.CONNECTED,
                    "tools_count": len([t for t in self.tool_registry.values() if t["server"] == server_name]),
                }
                health_results["servers"][server_name] = server_health

                if status != MCPServerStatus.CONNECTED:
                    health_results["overall_status"] = "degraded"

            return health_results

        except Exception as e:
            logger.error(f"Failed to perform health check: {e}")
            return {
                "overall_status": "error",
                "error": str(e),
                "servers": {},
                "total_servers": 0,
                "connected_servers": 0,
                "total_tools": 0,
            }


# Global MCP integration instance (lazy initialization to avoid import side effects)
_mcp_integration: MCPIntegration | None = None


def get_mcp_integration() -> MCPIntegration:
    """Get the global MCP integration instance (lazy initialized)."""
    global _mcp_integration
    if _mcp_integration is None:
        _mcp_integration = MCPIntegration()
    return _mcp_integration


async def initialize_mcp_servers() -> bool:
    """
    Initialize default MCP servers.

    Returns:
        True if initialization was successful
    """
    try:
        # Example server configurations
        default_servers = [
            MCPServerConfig(
                name="filesystem",
                command="mcp-server-filesystem",
                args=["--root", "/tmp"],
                env={"MCP_SERVER_FILESYSTEM_ROOT": "/tmp"},
            ),
            MCPServerConfig(
                name="git", command="mcp-server-git", args=["--repo", "."], env={"MCP_SERVER_GIT_REPO": "."}
            ),
        ]

        integration = get_mcp_integration()

        for config in default_servers:
            await integration.register_server(config)

        # Connect to servers
        for config in default_servers:
            await integration.connect_server(config.name)

        # Discover tools
        await integration.discover_tools()

        logger.info("MCP servers initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize MCP servers: {e}")
        return False
