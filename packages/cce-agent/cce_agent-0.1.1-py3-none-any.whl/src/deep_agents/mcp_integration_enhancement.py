"""
MCP Integration Enhancement for CCE Deep Agent.

This module integrates the existing CCE MCP workflow with the deep agents MCP ecosystem,
creating a unified MCP system that combines both systems for maximum capability and compatibility.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

# Import existing CCE MCP integration
try:
    from ..mcp_integration import MCPIntegration
    from ..mcp_workflow import MCPWorkflow
except ImportError as e:
    logging.warning(f"Could not import some CCE MCP components: {e}")
    MCPIntegration = None
    MCPWorkflow = None

# Import deep agents MCP components
try:
    from .mcp_ecosystem import MCPEcosystem
    from .mcp_integration import MCPIntegration as DeepAgentsMCPIntegration
except ImportError as e:
    logging.warning(f"Could not import some deep agents MCP components: {e}")
    DeepAgentsMCPIntegration = None
    MCPEcosystem = None

logger = logging.getLogger(__name__)


@dataclass
class UnifiedMCPTool:
    """Unified MCP tool combining CCE and deep agents capabilities."""

    name: str
    description: str
    cce_tool: Any | None = None
    deep_agents_tool: Any | None = None
    source: str = "unified"  # "cce", "deep_agents", "unified"
    capabilities: list[str] = None


class CCE_MCPIntegration:
    """
    Integrates existing CCE MCP workflow with deep agents MCP ecosystem.

    This class bridges the gap between the existing CCE MCP integration
    and the new deep agents MCP ecosystem, providing seamless access to all
    MCP capabilities through a unified interface.
    """

    def __init__(self):
        """Initialize the MCP integration system."""
        self.logger = logging.getLogger(f"{__name__}.CCE_MCPIntegration")
        self.existing_mcp: MCPIntegration | None = None
        self.existing_mcp_workflow: MCPWorkflow | None = None
        self.deep_agents_mcp: DeepAgentsMCPIntegration | None = None
        self.deep_agents_mcp_ecosystem: MCPEcosystem | None = None
        self.unified_mcp_system: dict[str, Any] = {}
        self.mcp_tool_registry: dict[str, UnifiedMCPTool] = {}

        self.logger.info("CCE_MCPIntegration initialized")

    def _load_existing_mcp(self) -> MCPIntegration | None:
        """
        Load the existing CCE MCP integration.

        Returns:
            MCPIntegration instance or None if not available
        """
        if not MCPIntegration:
            self.logger.warning("Existing MCPIntegration not available")
            return None

        try:
            existing_mcp = MCPIntegration()
            self.logger.info("Existing MCPIntegration loaded successfully")
            return existing_mcp
        except Exception as e:
            self.logger.error(f"Failed to load existing MCPIntegration: {e}")
            return None

    def _load_existing_mcp_workflow(self) -> MCPWorkflow | None:
        """
        Load the existing CCE MCP workflow.

        Returns:
            MCPWorkflow instance or None if not available
        """
        if not MCPWorkflow:
            self.logger.warning("Existing MCPWorkflow not available")
            return None

        try:
            existing_mcp_workflow = MCPWorkflow()
            self.logger.info("Existing MCPWorkflow loaded successfully")
            return existing_mcp_workflow
        except Exception as e:
            self.logger.error(f"Failed to load existing MCPWorkflow: {e}")
            return None

    def _load_deep_agents_mcp(self) -> DeepAgentsMCPIntegration | None:
        """
        Load the deep agents MCP integration.

        Returns:
            DeepAgentsMCPIntegration instance or None if not available
        """
        if not DeepAgentsMCPIntegration:
            self.logger.warning("Deep agents MCPIntegration not available")
            return None

        try:
            deep_agents_mcp = DeepAgentsMCPIntegration(
                server_urls=["http://localhost:3000"],  # Default server URLs
                client_id="cce-deep-agent",
            )
            self.logger.info("Deep agents MCPIntegration loaded successfully")
            return deep_agents_mcp
        except Exception as e:
            self.logger.error(f"Failed to load deep agents MCPIntegration: {e}")
            return None

    def _load_deep_agents_mcp_ecosystem(self) -> MCPEcosystem | None:
        """
        Load the deep agents MCP ecosystem.

        Returns:
            MCPEcosystem instance or None if not available
        """
        if not MCPEcosystem:
            self.logger.warning("Deep agents MCPEcosystem not available")
            return None

        try:
            # Default server configurations
            server_configs = [
                {"url": "http://localhost:3000", "client_id": "cce-deep-agent"},
                {"url": "http://localhost:3001", "client_id": "cce-deep-agent"},
            ]

            deep_agents_mcp_ecosystem = MCPEcosystem(server_configs)
            self.logger.info("Deep agents MCPEcosystem loaded successfully")
            return deep_agents_mcp_ecosystem
        except Exception as e:
            self.logger.error(f"Failed to load deep agents MCPEcosystem: {e}")
            return None

    def create_unified_mcp_system(self) -> dict[str, Any]:
        """
        Create unified MCP system combining CCE and deep agents.

        Returns:
            Unified MCP system configuration
        """
        self.logger.info("Creating unified MCP system...")

        # Load MCP components from both systems
        self.existing_mcp = self._load_existing_mcp()
        self.existing_mcp_workflow = self._load_existing_mcp_workflow()
        self.deep_agents_mcp = self._load_deep_agents_mcp()
        self.deep_agents_mcp_ecosystem = self._load_deep_agents_mcp_ecosystem()

        # Create unified MCP system
        self.unified_mcp_system = {
            "existing_mcp": self.existing_mcp,
            "existing_mcp_workflow": self.existing_mcp_workflow,
            "deep_agents_mcp": self.deep_agents_mcp,
            "deep_agents_mcp_ecosystem": self.deep_agents_mcp_ecosystem,
            "mcp_tool_registry": self.mcp_tool_registry,
            "server_configurations": self._get_server_configurations(),
            "tool_discovery": self._get_tool_discovery_config(),
            "execution_strategies": self._get_execution_strategies(),
        }

        # Initialize MCP tool registry
        self._initialize_mcp_tool_registry()

        self.logger.info("Unified MCP system created successfully")
        return self.unified_mcp_system

    def _get_server_configurations(self) -> dict[str, Any]:
        """Get MCP server configurations."""
        return {
            "default_servers": [
                {"url": "http://localhost:3000", "client_id": "cce-deep-agent"},
                {"url": "http://localhost:3001", "client_id": "cce-deep-agent"},
            ],
            "server_health_check": {
                "enabled": True,
                "interval": 30,  # seconds
                "timeout": 5,  # seconds
                "retry_count": 3,
            },
            "connection_pooling": {"enabled": True, "max_connections": 10, "max_connections_per_server": 5},
        }

    def _get_tool_discovery_config(self) -> dict[str, Any]:
        """Get tool discovery configuration."""
        return {
            "discovery_strategies": {
                "automatic": {
                    "enabled": True,
                    "interval": 60,  # seconds
                    "force_refresh": False,
                },
                "manual": {"enabled": True, "on_demand": True},
                "hybrid": {"enabled": True, "automatic_interval": 60, "manual_override": True},
            },
            "tool_caching": {
                "enabled": True,
                "cache_duration": 300,  # seconds
                "max_cache_size": 1000,
            },
            "tool_validation": {"enabled": True, "validate_schemas": True, "test_execution": True},
        }

    def _get_execution_strategies(self) -> dict[str, Any]:
        """Get execution strategies for different MCP systems."""
        return {
            "cce_mcp": {
                "description": "Use existing CCE MCP integration",
                "advantages": ["proven", "stable", "integrated"],
                "use_cases": ["existing workflows", "legacy tools", "stable operations"],
            },
            "deep_agents_mcp": {
                "description": "Use deep agents MCP integration",
                "advantages": ["modern", "flexible", "ecosystem"],
                "use_cases": ["new tools", "experimental features", "ecosystem integration"],
            },
            "unified": {
                "description": "Use unified MCP system with intelligent routing",
                "advantages": ["comprehensive", "optimal", "fallback"],
                "use_cases": ["production", "complex scenarios", "maximum capability"],
            },
        }

    def _initialize_mcp_tool_registry(self) -> None:
        """Initialize the MCP tool registry with available tools."""
        # Load tools from existing CCE MCP
        if self.existing_mcp:
            try:
                # This would load tools from existing MCP integration
                # For now, we'll create placeholder tools
                cce_tools = [
                    {"name": "cce_tool_1", "description": "CCE MCP Tool 1"},
                    {"name": "cce_tool_2", "description": "CCE MCP Tool 2"},
                ]

                for tool_info in cce_tools:
                    unified_tool = UnifiedMCPTool(
                        name=tool_info["name"],
                        description=tool_info["description"],
                        cce_tool=tool_info,
                        source="cce",
                        capabilities=["cce_operation"],
                    )
                    self.mcp_tool_registry[tool_info["name"]] = unified_tool

            except Exception as e:
                self.logger.error(f"Failed to load CCE MCP tools: {e}")

        # Load tools from deep agents MCP
        if self.deep_agents_mcp_ecosystem:
            try:
                # This would load tools from deep agents MCP ecosystem
                # For now, we'll create placeholder tools
                deep_agents_tools = [
                    {"name": "deep_agents_tool_1", "description": "Deep Agents MCP Tool 1"},
                    {"name": "deep_agents_tool_2", "description": "Deep Agents MCP Tool 2"},
                ]

                for tool_info in deep_agents_tools:
                    if tool_info["name"] not in self.mcp_tool_registry:
                        unified_tool = UnifiedMCPTool(
                            name=tool_info["name"],
                            description=tool_info["description"],
                            deep_agents_tool=tool_info,
                            source="deep_agents",
                            capabilities=["deep_agents_operation"],
                        )
                        self.mcp_tool_registry[tool_info["name"]] = unified_tool

            except Exception as e:
                self.logger.error(f"Failed to load deep agents MCP tools: {e}")

        self.logger.info(f"MCP tool registry initialized with {len(self.mcp_tool_registry)} tools")

    def integrate_mcp_workflows(self) -> dict[str, Any]:
        """
        Integrate existing MCP workflows with deep agents.

        Returns:
            Integrated MCP workflows configuration
        """
        self.logger.info("Integrating MCP workflows...")

        workflow_integration = {
            "workflow_types": {
                "cce_workflows": {
                    "description": "Existing CCE MCP workflows",
                    "components": ["MCPWorkflow", "MCPIntegration"],
                    "capabilities": ["legacy_tools", "existing_integrations", "proven_workflows"],
                },
                "deep_agents_workflows": {
                    "description": "Deep agents MCP workflows",
                    "components": ["MCPEcosystem", "MCPIntegration"],
                    "capabilities": ["ecosystem_tools", "dynamic_discovery", "modern_integration"],
                },
                "unified_workflows": {
                    "description": "Unified MCP workflows combining both systems",
                    "components": ["UnifiedMCPSystem", "IntelligentRouting"],
                    "capabilities": ["comprehensive_tools", "optimal_routing", "fallback_support"],
                },
            },
            "routing_strategies": {
                "tool_based": {
                    "description": "Route based on tool availability and capabilities",
                    "criteria": ["tool_name", "tool_capabilities", "tool_performance"],
                },
                "workflow_based": {
                    "description": "Route based on workflow requirements",
                    "criteria": ["workflow_type", "complexity", "performance_requirements"],
                },
                "hybrid": {
                    "description": "Combine tool and workflow-based routing",
                    "criteria": ["tool_availability", "workflow_requirements", "performance_optimization"],
                },
            },
            "execution_modes": {
                "sequential": {
                    "description": "Execute workflows sequentially",
                    "use_cases": ["simple_workflows", "dependency_management"],
                },
                "parallel": {
                    "description": "Execute workflows in parallel",
                    "use_cases": ["independent_operations", "performance_optimization"],
                },
                "adaptive": {
                    "description": "Adapt execution based on context and requirements",
                    "use_cases": ["complex_scenarios", "dynamic_requirements"],
                },
            },
        }

        return workflow_integration

    async def discover_mcp_tools(self, force_refresh: bool = False) -> list[UnifiedMCPTool]:
        """
        Discover MCP tools from all available systems.

        Args:
            force_refresh: Force refresh of tool discovery

        Returns:
            List of discovered MCP tools
        """
        self.logger.info("Discovering MCP tools...")

        discovered_tools = []

        # Discover tools from existing CCE MCP
        if self.existing_mcp and not force_refresh:
            try:
                # This would discover tools from existing MCP
                # For now, we'll use the registry
                for tool in self.mcp_tool_registry.values():
                    if tool.source == "cce":
                        discovered_tools.append(tool)
            except Exception as e:
                self.logger.error(f"Failed to discover CCE MCP tools: {e}")

        # Discover tools from deep agents MCP
        if self.deep_agents_mcp_ecosystem:
            try:
                # This would discover tools from deep agents MCP ecosystem
                # For now, we'll use the registry
                for tool in self.mcp_tool_registry.values():
                    if tool.source == "deep_agents":
                        discovered_tools.append(tool)
            except Exception as e:
                self.logger.error(f"Failed to discover deep agents MCP tools: {e}")

        self.logger.info(f"Discovered {len(discovered_tools)} MCP tools")
        return discovered_tools

    async def execute_mcp_tool(self, tool_name: str, **kwargs) -> dict[str, Any]:
        """
        Execute an MCP tool using the unified system.

        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool arguments

        Returns:
            Tool execution result
        """
        self.logger.info(f"Executing MCP tool: {tool_name}")

        if tool_name not in self.mcp_tool_registry:
            return {
                "success": False,
                "error": f"MCP tool '{tool_name}' not found",
                "available_tools": list(self.mcp_tool_registry.keys()),
            }

        tool = self.mcp_tool_registry[tool_name]

        try:
            # Execute based on tool source
            if tool.source == "cce" and self.existing_mcp:
                result = await self._execute_cce_mcp_tool(tool, **kwargs)
            elif tool.source == "deep_agents" and self.deep_agents_mcp_ecosystem:
                result = await self._execute_deep_agents_mcp_tool(tool, **kwargs)
            elif tool.source == "unified":
                result = await self._execute_unified_mcp_tool(tool, **kwargs)
            else:
                return {"success": False, "error": f"Tool source '{tool.source}' not available for execution"}

            return {"success": True, "result": result, "tool_name": tool_name, "source": tool.source}

        except Exception as e:
            self.logger.error(f"MCP tool execution failed: {e}")
            return {"success": False, "error": str(e), "tool_name": tool_name, "source": tool.source}

    async def _execute_cce_mcp_tool(self, tool: UnifiedMCPTool, **kwargs) -> Any:
        """Execute tool using CCE MCP system."""
        # This would execute using existing CCE MCP integration
        # For now, return a mock result
        return f"CCE MCP tool '{tool.name}' executed with args: {kwargs}"

    async def _execute_deep_agents_mcp_tool(self, tool: UnifiedMCPTool, **kwargs) -> Any:
        """Execute tool using deep agents MCP system."""
        # This would execute using deep agents MCP ecosystem
        # For now, return a mock result
        return f"Deep agents MCP tool '{tool.name}' executed with args: {kwargs}"

    async def _execute_unified_mcp_tool(self, tool: UnifiedMCPTool, **kwargs) -> Any:
        """Execute tool using unified MCP system."""
        # Try CCE first, fallback to deep agents
        if tool.cce_tool and self.existing_mcp:
            try:
                result = await self._execute_cce_mcp_tool(tool, **kwargs)
                return result
            except Exception as e:
                self.logger.warning(f"CCE MCP tool execution failed, trying deep agents: {e}")

        if tool.deep_agents_tool and self.deep_agents_mcp_ecosystem:
            try:
                result = await self._execute_deep_agents_mcp_tool(tool, **kwargs)
                return result
            except Exception as e:
                self.logger.error(f"Deep agents MCP tool execution also failed: {e}")

        raise RuntimeError("Both CCE and deep agents MCP tool execution failed")

    def get_available_mcp_tools(self) -> list[str]:
        """
        Get list of available MCP tool names.

        Returns:
            List of available MCP tool names
        """
        return list(self.mcp_tool_registry.keys())

    def get_mcp_tool_info(self, tool_name: str) -> dict[str, Any] | None:
        """
        Get information about a specific MCP tool.

        Args:
            tool_name: Name of the MCP tool

        Returns:
            MCP tool information dictionary or None if not found
        """
        if tool_name not in self.mcp_tool_registry:
            return None

        tool = self.mcp_tool_registry[tool_name]
        return {
            "name": tool.name,
            "description": tool.description,
            "source": tool.source,
            "capabilities": tool.capabilities,
            "has_cce_tool": tool.cce_tool is not None,
            "has_deep_agents_tool": tool.deep_agents_tool is not None,
        }

    def get_mcp_system_health(self) -> dict[str, Any]:
        """
        Get health status of all MCP systems.

        Returns:
            MCP system health information
        """
        health_status = {
            "overall_health": "healthy",
            "systems": {},
            "tool_counts": {
                "total": len(self.mcp_tool_registry),
                "cce": len([t for t in self.mcp_tool_registry.values() if t.source == "cce"]),
                "deep_agents": len([t for t in self.mcp_tool_registry.values() if t.source == "deep_agents"]),
                "unified": len([t for t in self.mcp_tool_registry.values() if t.source == "unified"]),
            },
        }

        # Check CCE MCP system health
        if self.existing_mcp:
            health_status["systems"]["cce_mcp"] = {
                "status": "healthy",
                "available": True,
                "tools_available": len([t for t in self.mcp_tool_registry.values() if t.source == "cce"]),
            }
        else:
            health_status["systems"]["cce_mcp"] = {"status": "unavailable", "available": False, "tools_available": 0}
            health_status["overall_health"] = "degraded"

        # Check deep agents MCP system health
        if self.deep_agents_mcp_ecosystem:
            health_status["systems"]["deep_agents_mcp"] = {
                "status": "healthy",
                "available": True,
                "tools_available": len([t for t in self.mcp_tool_registry.values() if t.source == "deep_agents"]),
            }
        else:
            health_status["systems"]["deep_agents_mcp"] = {
                "status": "unavailable",
                "available": False,
                "tools_available": 0,
            }
            health_status["overall_health"] = "degraded"

        return health_status

    def validate_mcp_integration(self) -> dict[str, Any]:
        """
        Validate that MCP integration is working correctly.

        Returns:
            Validation results
        """
        validation_results = {"success": True, "errors": [], "warnings": [], "mcp_health": self.get_mcp_system_health()}

        # Check for MCP systems
        if not self.existing_mcp and not self.deep_agents_mcp_ecosystem:
            validation_results["errors"].append("No MCP systems available")
            validation_results["success"] = False

        # Check for MCP tools
        if not self.mcp_tool_registry:
            validation_results["warnings"].append("No MCP tools available")

        # Check tool registry integrity
        for tool_name, tool in self.mcp_tool_registry.items():
            if not tool.name:
                validation_results["errors"].append(f"MCP tool '{tool_name}' missing name")
                validation_results["success"] = False
            if not tool.description:
                validation_results["warnings"].append(f"MCP tool '{tool_name}' missing description")
            if not tool.capabilities:
                validation_results["warnings"].append(f"MCP tool '{tool_name}' missing capabilities")

        self.logger.info(f"MCP integration validation: {'PASSED' if validation_results['success'] else 'FAILED'}")
        return validation_results


# Global instance for easy access
_mcp_integration_instance: CCE_MCPIntegration | None = None


def get_mcp_integration() -> CCE_MCPIntegration:
    """
    Get the global MCP integration instance.

    Returns:
        CCE_MCPIntegration instance
    """
    global _mcp_integration_instance
    if _mcp_integration_instance is None:
        _mcp_integration_instance = CCE_MCPIntegration()
        _mcp_integration_instance.create_unified_mcp_system()
    return _mcp_integration_instance


async def execute_mcp_tool(tool_name: str, **kwargs) -> dict[str, Any]:
    """
    Execute an MCP tool using the unified system.

    Args:
        tool_name: Name of the tool to execute
        **kwargs: Tool arguments

    Returns:
        Tool execution result
    """
    integration = get_mcp_integration()
    return await integration.execute_mcp_tool(tool_name, **kwargs)


def get_available_mcp_tools() -> list[str]:
    """
    Get list of available MCP tool names.

    Returns:
        List of available MCP tool names
    """
    integration = get_mcp_integration()
    return integration.get_available_mcp_tools()
