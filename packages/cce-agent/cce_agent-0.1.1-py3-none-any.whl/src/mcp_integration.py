"""
MCP (Multi-Agent Communication Protocol) Integration Seam

Provides integration with LangGraph MCP adapters using MultiServerMCPClient
for connecting to MCP servers and accessing their tools.

This module follows the LangGraph MCP documentation pattern for proper
integration with MCP servers and tool access.
"""

import json
import logging
import os
import tempfile
from dataclasses import dataclass
from typing import Any

# Try to import MCP dependencies
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

try:
    from mcp.server.fastmcp import FastMCP

    MCP_CORE_AVAILABLE = True
except ImportError:
    MCP_CORE_AVAILABLE = False


@dataclass
class MCPCapability:
    """Represents an MCP capability or tool."""

    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    provider: str
    enabled: bool = True


@dataclass
class MCPConnection:
    """Represents a connection to an MCP server."""

    server_name: str
    server_url: str
    capabilities: list[MCPCapability]
    status: str  # "connected", "disconnected", "error"
    last_ping: float | None = None
    error_message: str | None = None


def create_math_server_file() -> str:
    """Create a temporary math MCP server file."""
    server_content = '''#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract second number from first"""
    return a - b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide first number by second"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")
'''

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix="_math_server.py", delete=False) as f:
        f.write(server_content)
        return f.name


def create_analysis_server_file() -> str:
    """Create a temporary analysis MCP server file."""
    server_content = '''#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("Analysis")

@mcp.tool()
async def analyze_text(text: str) -> str:
    """Analyze text and return insights"""
    word_count = len(text.split())
    char_count = len(text)
    sentences = len([s for s in text.split('.') if s.strip()])
    
    analysis = {
        "word_count": word_count,
        "character_count": char_count,
        "sentence_count": sentences,
        "avg_words_per_sentence": word_count / max(sentences, 1),
        "complexity": "high" if word_count > 100 else "medium" if word_count > 50 else "low"
    }
    
    return json.dumps(analysis, indent=2)

@mcp.tool()
async def summarize_text(text: str, max_length: int = 100) -> str:
    """Summarize text to specified length"""
    if len(text) <= max_length:
        return text
    
    # Simple summarization - take first sentences up to max_length
    sentences = text.split('. ')
    summary = ""
    for sentence in sentences:
        if len(summary + sentence) <= max_length:
            summary += sentence + ". "
        else:
            break
    
    return summary.strip()

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)
'''

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix="_analysis_server.py", delete=False) as f:
        f.write(server_content)
        return f.name


class LangGraphMCPIntegrationManager:
    """
    LangGraph-native MCP integration using MultiServerMCPClient.

    Follows the LangGraph MCP documentation pattern for proper integration.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client: MultiServerMCPClient | None = None
        self.server_configs: dict[str, dict[str, Any]] = {}
        self.tools: list[Any] = []
        self.temp_server_files: list[str] = []

        self.logger.info("🔌 LangGraph MCP Integration Manager initialized")

    async def add_server_config(self, server_name: str, config: dict[str, Any]) -> bool:
        """Add MCP server configuration."""
        try:
            self.server_configs[server_name] = config
            self.logger.info(f"✅ Added MCP server config: {server_name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error adding server config {server_name}: {e}")
            return False

    async def initialize_client(self) -> bool:
        """Initialize MultiServerMCPClient with configured servers."""
        if not MCP_AVAILABLE:
            self.logger.warning("❌ langchain-mcp-adapters not available")
            return False

        if not self.server_configs:
            self.logger.warning("❌ No MCP server configurations available")
            return False

        try:
            self.client = MultiServerMCPClient(self.server_configs)
            self.logger.info(f"✅ Initialized MultiServerMCPClient with {len(self.server_configs)} servers")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize MCP client: {e}")
            return False

    async def get_tools(self) -> list[Any]:
        """Get tools from all MCP servers."""
        if not self.client:
            await self.initialize_client()

        if not self.client:
            return []

        try:
            self.tools = await self.client.get_tools()
            self.logger.info(f"✅ Retrieved {len(self.tools)} tools from MCP servers")
            return self.tools
        except Exception as e:
            self.logger.error(f"❌ Failed to get tools from MCP servers: {e}")
            return []

    async def invoke_tool(self, tool_name: str, params: dict[str, Any]) -> Any:
        """Invoke a specific MCP tool."""
        if not self.tools:
            await self.get_tools()

        # Find the tool
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")

        try:
            result = await tool.ainvoke(params)
            self.logger.debug(f"🔌 Invoked MCP tool: {tool_name}")
            return result
        except Exception as e:
            self.logger.error(f"❌ Failed to invoke tool {tool_name}: {e}")
            raise

    def list_tool_names(self) -> list[str]:
        """List names of available tools."""
        return [tool.name for tool in self.tools]

    def get_tool_info(self, tool_name: str) -> dict[str, Any] | None:
        """Get information about a specific tool."""
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            return None

        return {
            "name": tool.name,
            "description": getattr(tool, "description", ""),
            "args": getattr(tool, "args", {}),
        }

    async def create_default_servers(self) -> bool:
        """Create default MCP servers for testing."""
        if not MCP_CORE_AVAILABLE:
            self.logger.warning("❌ mcp library not available for creating servers")
            return False

        try:
            # Create math server
            math_server_path = create_math_server_file()
            self.temp_server_files.append(math_server_path)

            # Add server configuration (only stdio for reliability)
            import sys

            await self.add_server_config(
                "math",
                {
                    "command": sys.executable,
                    "args": [math_server_path],
                    "transport": "stdio",
                },
            )

            self.logger.info("✅ Created default MCP server (math)")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to create default servers: {e}")
            return False

    async def close(self):
        """Clean up MCP integration resources."""
        if self.client:
            # MultiServerMCPClient doesn't have a close method
            # The connections are just configuration dictionaries
            # We just need to clear our references
            self.client = None
            self.tools = []
            self.logger.info("✅ MCP client references cleared")

        # Clean up temporary server files
        for file_path in self.temp_server_files:
            try:
                os.unlink(file_path)
            except:
                pass

        self.temp_server_files.clear()
        self.logger.info("🔌 MCP Integration Manager cleanup complete")


# Global MCP manager instance
_mcp_manager: LangGraphMCPIntegrationManager | None = None


def get_mcp_manager() -> LangGraphMCPIntegrationManager:
    """Get the global LangGraph MCP integration manager."""
    global _mcp_manager
    if _mcp_manager is None:
        _mcp_manager = LangGraphMCPIntegrationManager()
    return _mcp_manager


async def initialize_mcp_from_config(config_path: str | None = None) -> LangGraphMCPIntegrationManager:
    """
    Initialize MCP integration from configuration.

    Args:
        config_path: Path to MCP configuration file

    Returns:
        Configured LangGraph MCP integration manager
    """
    manager = get_mcp_manager()

    # Try to load configuration
    mcp_config = None
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path) as f:
                mcp_config = json.load(f)
        except Exception as e:
            manager.logger.warning(f"Failed to load MCP config from {config_path}: {e}")

    # Use environment variables if no config file
    if mcp_config is None:
        mcp_servers = os.getenv("MCP_SERVERS", "").strip()
        if mcp_servers:
            try:
                mcp_config = {"servers": json.loads(mcp_servers)}
            except Exception as e:
                manager.logger.warning(f"Failed to parse MCP_SERVERS environment variable: {e}")

    # Create default servers if no configuration
    if mcp_config is None:
        await manager.create_default_servers()
    else:
        # Initialize servers from configuration
        servers = mcp_config.get("servers", [])
        for server_config in servers:
            server_name = server_config.pop("name", f"server_{len(manager.server_configs)}")
            await manager.add_server_config(server_name, server_config)

    # Initialize the client
    await manager.initialize_client()

    return manager


# Convenience functions for integration with other components
async def mcp_invoke(tool_name: str, params: dict[str, Any]) -> Any:
    """Convenience function to invoke MCP tool."""
    manager = get_mcp_manager()
    return await manager.invoke_tool(tool_name, params)


def mcp_list_tools() -> list[str]:
    """Convenience function to list MCP tool names."""
    manager = get_mcp_manager()
    return manager.list_tool_names()


async def mcp_get_tools():
    """Convenience function to get all MCP tools."""
    manager = get_mcp_manager()
    return await manager.get_tools()


def is_mcp_available() -> bool:
    """Check if MCP integration is available."""
    return MCP_AVAILABLE and MCP_CORE_AVAILABLE
