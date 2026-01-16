"""
MCP Workflow Integration for LangGraph

Provides LangGraph workflow integration with MCP tools using ToolNode
and proper agent patterns as shown in the LangGraph documentation.
"""

import asyncio
import logging
from typing import Any

# LangGraph imports
try:
    from langchain.chat_models import init_chat_model
    from langgraph.graph import END, START, MessagesState, StateGraph
    from langgraph.prebuilt import ToolNode

    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

# MCP imports
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

from mcp_integration import LangGraphMCPIntegrationManager, create_math_server_file


class MCPWorkflowBuilder:
    """
    Builder for LangGraph workflows that integrate MCP tools.

    Follows the LangGraph MCP documentation pattern for creating
    agents with MCP tool access.
    """

    def __init__(self, model_name: str = "anthropic:claude-sonnet-4-20250514"):
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.model = None
        self.model_with_tools = None
        self.tools = []
        self.tool_node = None
        self.graph = None
        self.mcp_manager = None

        if not LANGGRAPH_AVAILABLE:
            raise ImportError("LangGraph not available")
        if not MCP_AVAILABLE:
            raise ImportError("langchain-mcp-adapters not available")

    async def initialize_model(self):
        """Initialize the chat model."""
        try:
            self.model = init_chat_model(self.model_name)
            self.logger.info(f"✅ Initialized model: {self.model_name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize model: {e}")
            return False

    async def setup_mcp_tools(self, server_configs: dict[str, dict[str, Any]] | None = None):
        """Set up MCP tools for the workflow."""
        try:
            if server_configs:
                # Use provided server configurations
                client = MultiServerMCPClient(server_configs)
            else:
                # Use default MCP manager
                self.mcp_manager = LangGraphMCPIntegrationManager()
                await self.mcp_manager.create_default_servers()
                await self.mcp_manager.initialize_client()
                client = self.mcp_manager.client

            # Get tools from MCP servers
            self.tools = await client.get_tools()
            self.logger.info(f"✅ Retrieved {len(self.tools)} MCP tools")

            # Create ToolNode
            self.tool_node = ToolNode(self.tools)

            # Bind tools to model
            self.model_with_tools = self.model.bind_tools(self.tools)

            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to setup MCP tools: {e}")
            return False

    def should_continue(self, state: MessagesState) -> str:
        """Determine whether to continue to tools or end."""
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    async def call_model(self, state: MessagesState) -> dict[str, list]:
        """Call the model with the current state."""
        messages = state["messages"]
        response = await self.model_with_tools.ainvoke(messages)
        return {"messages": [response]}

    def build_graph(self) -> bool:
        """Build the LangGraph workflow."""
        try:
            # Create StateGraph
            builder = StateGraph(MessagesState)

            # Add nodes
            builder.add_node("call_model", self.call_model)
            builder.add_node("tools", self.tool_node)

            # Add edges
            builder.add_edge(START, "call_model")
            builder.add_conditional_edges(
                "call_model",
                self.should_continue,
            )
            builder.add_edge("tools", "call_model")

            # Compile the graph
            self.graph = builder.compile()
            self.logger.info("✅ Built MCP workflow graph")

            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to build graph: {e}")
            return False

    async def create_workflow(self, server_configs: dict[str, dict[str, Any]] | None = None) -> bool:
        """Create a complete MCP-enabled workflow."""
        try:
            # Initialize model
            if not await self.initialize_model():
                return False

            # Setup MCP tools
            if not await self.setup_mcp_tools(server_configs):
                return False

            # Build graph
            if not self.build_graph():
                return False

            self.logger.info("✅ MCP workflow created successfully")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to create workflow: {e}")
            return False

    async def invoke(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        """Invoke the workflow with messages."""
        if not self.graph:
            raise RuntimeError("Workflow not created. Call create_workflow() first.")

        try:
            result = await self.graph.ainvoke({"messages": messages})
            return result
        except Exception as e:
            self.logger.error(f"❌ Workflow invocation failed: {e}")
            raise

    async def cleanup(self):
        """Clean up resources."""
        if self.mcp_manager:
            await self.mcp_manager.close()
        self.logger.info("✅ MCP workflow cleanup completed")


# Convenience functions for easy workflow creation
async def create_mcp_workflow(
    model_name: str = "anthropic:claude-sonnet-4-20250514",
    server_configs: dict[str, dict[str, Any]] | None = None,
) -> MCPWorkflowBuilder:
    """Create an MCP-enabled workflow."""
    builder = MCPWorkflowBuilder(model_name)
    success = await builder.create_workflow(server_configs)
    if not success:
        raise RuntimeError("Failed to create MCP workflow")
    return builder


async def create_default_mcp_workflow() -> MCPWorkflowBuilder:
    """Create a workflow with default MCP servers."""
    return await create_mcp_workflow()


# Example usage patterns
async def example_math_workflow():
    """Example of using MCP workflow for math operations."""
    try:
        # Create workflow with default servers
        workflow = await create_default_mcp_workflow()

        # Test math operations
        math_queries = [
            {"role": "user", "content": "What's 15 + 27?"},
            {"role": "user", "content": "Calculate 6 * 8"},
            {"role": "user", "content": "What's 100 divided by 4?"},
        ]

        for query in math_queries:
            result = await workflow.invoke([query])
            print(f"Query: {query['content']}")
            print(f"Response: {result['messages'][-1].content}")
            print("-" * 50)

        # Cleanup
        await workflow.cleanup()

    except Exception as e:
        print(f"❌ Math workflow example failed: {e}")


async def example_custom_servers_workflow():
    """Example of using MCP workflow with custom server configurations."""
    try:
        import sys

        # Create custom math server
        math_server_path = create_math_server_file()

        # Custom server configuration
        server_configs = {
            "math": {
                "command": sys.executable,
                "args": [math_server_path],
                "transport": "stdio",
            }
        }

        # Create workflow with custom servers
        workflow = await create_mcp_workflow(server_configs=server_configs)

        # Test with custom server
        result = await workflow.invoke([{"role": "user", "content": "What's 25 + 17?"}])

        print(f"Custom server result: {result['messages'][-1].content}")

        # Cleanup
        await workflow.cleanup()

        # Clean up temp file
        import os

        os.unlink(math_server_path)

    except Exception as e:
        print(f"❌ Custom servers workflow example failed: {e}")


if __name__ == "__main__":
    # Run examples
    asyncio.run(example_math_workflow())
    asyncio.run(example_custom_servers_workflow())
