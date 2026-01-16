from __future__ import annotations

"""
Stakeholder System Integration for CCE Deep Agent.

This module integrates the existing CCE stakeholder system (5 specialized stakeholder agents)
with the deep agents implementation, creating a unified stakeholder system that combines
both systems for maximum capability and compatibility.
"""

import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

# Import existing CCE stakeholder system
try:
    from ..stakeholder_generator.stakeholder_agents import StakeholderAgent, StakeholderContext, StakeholderType
    from ..stakeholder_generator.subgraphs import (
        create_aider_integration_subgraph,
        create_context_engineering_subgraph,
        create_developer_experience_subgraph,
        create_langgraph_architect_subgraph,
        create_stability_specialist_subgraph,
    )
    from ..stakeholder_generator.supervisor_graph import SupervisorGraph, SupervisorState
except ImportError as e:
    logging.warning(f"Could not import some CCE stakeholder components: {e}")
    SupervisorGraph = None
    StakeholderAgent = None
    StakeholderType = None
    StakeholderContext = None

# Import deep agents components
try:
    from deepagents import SubAgent

    from .stakeholder_agents import ALL_STAKEHOLDER_AGENTS
    from .state import CCEDeepAgentState
    from .subagents import context_engineering_agent, general_purpose_agent, planning_agent
except ImportError as e:
    logging.warning(f"Could not import some deep agents components: {e}")
    SubAgent = None

logger = logging.getLogger(__name__)


@dataclass
class UnifiedStakeholderAgent:
    """Unified stakeholder agent combining CCE and deep agents capabilities."""

    name: str
    description: str
    cce_agent: StakeholderAgent | None = None
    deep_agents_subagent: SubAgent | None = None
    capabilities: list[str] = None
    execution_mode: str = "hybrid"  # "cce", "deep_agents", "hybrid"


class CCE_StakeholderIntegration:
    """
    Integrates existing CCE stakeholder system with deep agents sub-agents.

    This class bridges the gap between the existing CCE stakeholder system
    (5 specialized stakeholder agents with supervisor orchestration) and the
    new deep agents implementation, providing seamless access to all stakeholder
    capabilities through a unified interface.
    """

    def __init__(self):
        """Initialize the stakeholder integration system."""
        self.logger = logging.getLogger(f"{__name__}.CCE_StakeholderIntegration")
        self.supervisor_graph: SupervisorGraph | None = None
        self.cce_stakeholder_agents: dict[str, StakeholderAgent] = {}
        self.deep_agents_subagents: dict[str, SubAgent] = {}
        self.unified_stakeholder_system: dict[str, UnifiedStakeholderAgent] = {}
        self.stakeholder_registry: dict[str, Any] = {}
        self.deep_agents_executor = None

        self.logger.info("CCE_StakeholderIntegration initialized")

    @staticmethod
    def _get_subagent_name(subagent: Any) -> str | None:
        if isinstance(subagent, dict):
            return subagent.get("name")
        return getattr(subagent, "name", None)

    @staticmethod
    def _get_subagent_description(subagent: Any, fallback: str) -> str:
        if isinstance(subagent, dict):
            return subagent.get("description", fallback)
        return getattr(subagent, "description", fallback)

    @staticmethod
    def _get_subagent_tools(subagent: Any) -> list[str]:
        if isinstance(subagent, dict):
            return subagent.get("tools", []) or []
        return getattr(subagent, "tools", []) or []

    def _load_stakeholder_agents(self) -> dict[str, StakeholderAgent]:
        """
        Load existing CCE stakeholder agents.

        Returns:
            Dictionary mapping stakeholder names to agent instances
        """
        stakeholder_agents = {}

        if not StakeholderAgent or StakeholderType is None:
            self.logger.warning("StakeholderAgent not available")
            return stakeholder_agents

        try:
            stakeholder_definitions = {
                "aider_specialist": StakeholderType.AIDER_INTEGRATION,
                "context_engineer": StakeholderType.CONTEXT_ENGINEERING,
                "langgraph_architect": StakeholderType.LANGGRAPH_ARCHITECTURE,
                "stability_specialist": StakeholderType.PRODUCTION_STABILITY,
                "developer_experience_specialist": StakeholderType.DEVELOPER_EXPERIENCE,
            }

            for agent_id, stakeholder_type in stakeholder_definitions.items():
                try:
                    stakeholder_agent = StakeholderAgent(stakeholder_type)
                    config = getattr(stakeholder_agent, "config", {})
                    stakeholder_agent.name = config.get("name", agent_id)
                    stakeholder_agent.description = config.get("domain", "")
                    stakeholder_agent.capabilities = config.get("focus_areas", [])
                    stakeholder_agents[agent_id] = stakeholder_agent
                except Exception as e:
                    self.logger.warning(f"Could not create stakeholder agent '{agent_id}': {e}")

            self.logger.info(f"Loaded {len(stakeholder_agents)} CCE stakeholder agents")

        except Exception as e:
            self.logger.error(f"Failed to load CCE stakeholder agents: {e}")

        return stakeholder_agents

    def _load_deep_agents_subagents(self) -> dict[str, SubAgent]:
        """
        Load deep agents sub-agents.

        Returns:
            Dictionary mapping sub-agent names to SubAgent instances
        """
        subagents = {}

        if not SubAgent:
            self.logger.warning("SubAgent not available")
            return subagents

        try:
            if ALL_STAKEHOLDER_AGENTS:
                for subagent in ALL_STAKEHOLDER_AGENTS:
                    name = self._get_subagent_name(subagent)
                    if name:
                        subagents[name] = subagent

            core_candidates = {
                "context-engineer": globals().get("context_engineering_agent"),
                "general-purpose": globals().get("general_purpose_agent"),
                "planning-specialist": globals().get("planning_agent"),
            }

            for fallback_name, subagent in core_candidates.items():
                if not subagent:
                    continue
                name = self._get_subagent_name(subagent) or fallback_name
                subagents[name] = subagent

            self.logger.info(f"Loaded {len(subagents)} deep agents sub-agents")

        except Exception as e:
            self.logger.error(f"Failed to load deep agents sub-agents: {e}")

        return subagents

    def _load_supervisor_graph(self) -> SupervisorGraph | None:
        """
        Load the existing CCE supervisor graph.

        Returns:
            SupervisorGraph instance or None if not available
        """
        if not SupervisorGraph:
            self.logger.warning("SupervisorGraph not available")
            return None

        try:
            # Create supervisor graph (simplified for integration)
            supervisor_graph = SupervisorGraph()
            self.logger.info("SupervisorGraph loaded successfully")
            return supervisor_graph
        except Exception as e:
            self.logger.error(f"Failed to load SupervisorGraph: {e}")
            return None

    def create_unified_stakeholder_system(self) -> dict[str, UnifiedStakeholderAgent]:
        """
        Create unified stakeholder system combining CCE and deep agents.

        Returns:
            Unified stakeholder system with all available agents
        """
        self.logger.info("Creating unified stakeholder system...")

        # Load stakeholder agents from both systems
        self.cce_stakeholder_agents = self._load_stakeholder_agents()
        self.deep_agents_subagents = self._load_deep_agents_subagents()
        self.supervisor_graph = self._load_supervisor_graph()

        # Create unified stakeholder agents
        self.unified_stakeholder_system = {}

        # Map CCE stakeholders to deep agents sub-agents
        stakeholder_mapping = {
            "aider_specialist": "aider-specialist",
            "context_engineer": "context-engineer",
            "langgraph_architect": "langgraph-architect",
            "stability_specialist": "stability-specialist",
            "developer_experience_specialist": "developer-experience-specialist",
        }

        # Create unified agents
        for cce_name, cce_agent in self.cce_stakeholder_agents.items():
            deep_agents_name = stakeholder_mapping.get(cce_name)
            deep_agents_subagent = self.deep_agents_subagents.get(deep_agents_name) if deep_agents_name else None

            unified_agent = UnifiedStakeholderAgent(
                name=cce_agent.name,
                description=cce_agent.description,
                cce_agent=cce_agent,
                deep_agents_subagent=deep_agents_subagent,
                capabilities=cce_agent.capabilities if hasattr(cce_agent, "capabilities") else [],
                execution_mode="hybrid" if deep_agents_subagent else "cce",
            )

            self.unified_stakeholder_system[cce_name] = unified_agent

        # Add deep agents sub-agents that don't have CCE equivalents
        for subagent_name, subagent in self.deep_agents_subagents.items():
            if subagent_name not in stakeholder_mapping.values():
                unified_agent = UnifiedStakeholderAgent(
                    name=self._get_subagent_name(subagent) or subagent_name,
                    description=self._get_subagent_description(subagent, f"Deep agents sub-agent: {subagent_name}"),
                    cce_agent=None,
                    deep_agents_subagent=subagent,
                    capabilities=self._get_subagent_tools(subagent),
                    execution_mode="deep_agents",
                )

                self.unified_stakeholder_system[subagent_name] = unified_agent

        # Register in stakeholder registry
        self._register_stakeholders()

        self.logger.info(f"Unified stakeholder system created with {len(self.unified_stakeholder_system)} agents")
        return self.unified_stakeholder_system

    def _register_stakeholders(self) -> None:
        """Register stakeholders in the stakeholder registry."""
        self.stakeholder_registry = {
            "unified_agents": self.unified_stakeholder_system,
            "cce_agents": self.cce_stakeholder_agents,
            "deep_agents_subagents": self.deep_agents_subagents,
            "supervisor_graph": self.supervisor_graph,
            "capabilities": self._get_capability_mapping(),
            "execution_strategies": self._get_execution_strategies(),
        }

    def _get_capability_mapping(self) -> dict[str, list[str]]:
        """Get mapping of capabilities to stakeholder agents."""
        capability_mapping = {}

        for agent_name, agent in self.unified_stakeholder_system.items():
            for capability in agent.capabilities:
                if capability not in capability_mapping:
                    capability_mapping[capability] = []
                capability_mapping[capability].append(agent_name)

        return capability_mapping

    def _get_execution_strategies(self) -> dict[str, Any]:
        """Get execution strategies for different stakeholder types."""
        return {
            "cce": {
                "description": "Use existing CCE stakeholder system",
                "advantages": ["proven", "stable", "comprehensive"],
                "use_cases": ["complex analysis", "supervisor orchestration", "established workflows"],
            },
            "deep_agents": {
                "description": "Use deep agents sub-agent delegation",
                "advantages": ["flexible", "contextual", "adaptive"],
                "use_cases": ["general tasks", "context management", "planning"],
            },
            "hybrid": {
                "description": "Intelligently route to best stakeholder system",
                "advantages": ["optimal", "fallback", "comprehensive"],
                "use_cases": ["production", "complex scenarios", "maximum capability"],
            },
        }

    def integrate_stakeholder_expertise(self) -> dict[str, Any]:
        """
        Integrate existing stakeholder expertise with deep agents.

        Returns:
            Integrated stakeholder expertise configuration
        """
        self.logger.info("Integrating stakeholder expertise...")

        expertise_integration = {
            "stakeholder_roles": {
                "aider_specialist": {
                    "cce_expertise": "Code analysis, repository mapping, AIDER integration",
                    "deep_agents_expertise": "LLM-based code editing, file system operations",
                    "unified_capabilities": ["code_analysis", "repository_mapping", "code_editing", "file_operations"],
                },
                "context_engineer": {
                    "cce_expertise": "Context management, memory systems, semantic optimization",
                    "deep_agents_expertise": "Virtual filesystem, context sharing, memory optimization",
                    "unified_capabilities": [
                        "context_management",
                        "memory_systems",
                        "semantic_optimization",
                        "virtual_filesystem",
                    ],
                },
                "langgraph_architect": {
                    "cce_expertise": "LangGraph orchestration, state management, workflow design",
                    "deep_agents_expertise": "Graph orchestration, sub-agent coordination, state management",
                    "unified_capabilities": [
                        "graph_orchestration",
                        "state_management",
                        "workflow_design",
                        "sub_agent_coordination",
                    ],
                },
                "stability_specialist": {
                    "cce_expertise": "Operational reliability, performance optimization, error handling",
                    "deep_agents_expertise": "Error handling, fallback systems, performance optimization",
                    "unified_capabilities": [
                        "reliability",
                        "performance_optimization",
                        "error_handling",
                        "fallback_systems",
                    ],
                },
                "developer_experience_specialist": {
                    "cce_expertise": "API design, debugging, maintainability, user experience",
                    "deep_agents_expertise": "General-purpose operations, user interaction, system usability",
                    "unified_capabilities": [
                        "api_design",
                        "debugging",
                        "maintainability",
                        "user_experience",
                        "general_operations",
                    ],
                },
            },
            "expertise_areas": {
                "code_analysis": ["aider_specialist"],
                "context_management": ["context_engineer"],
                "graph_orchestration": ["langgraph_architect"],
                "reliability": ["stability_specialist"],
                "user_experience": ["developer_experience_specialist"],
                "planning": ["planning-specialist"],
                "general_operations": ["general-purpose"],
            },
            "collaboration_patterns": {
                "sequential": "Stakeholders work in sequence, passing results between them",
                "parallel": "Multiple stakeholders work simultaneously on different aspects",
                "supervisor": "Supervisor graph orchestrates stakeholder interactions",
                "delegation": "Deep agents sub-agents delegate to appropriate stakeholders",
            },
        }

        return expertise_integration

    def get_stakeholder_by_capability(self, capability: str) -> list[UnifiedStakeholderAgent]:
        """
        Get stakeholders that have a specific capability.

        Args:
            capability: Capability to search for

        Returns:
            List of stakeholders with the specified capability
        """
        stakeholders = []

        for agent in self.unified_stakeholder_system.values():
            if capability in agent.capabilities:
                stakeholders.append(agent)

        return stakeholders

    def get_best_stakeholder_for_task(
        self, task_description: str, task_type: str = None
    ) -> UnifiedStakeholderAgent | None:
        """
        Get the best stakeholder for a specific task.

        Args:
            task_description: Description of the task
            task_type: Type of task (optional)

        Returns:
            Best stakeholder agent for the task or None if not found
        """
        # Simple keyword-based matching (could be enhanced with ML)
        task_lower = task_description.lower()

        # Define task patterns and their preferred stakeholders
        task_patterns = {
            "code": ["aider_specialist"],
            "context": ["context_engineer"],
            "graph": ["langgraph_architect"],
            "reliability": ["stability_specialist"],
            "api": ["developer_experience_specialist"],
            "plan": ["planning-specialist"],
            "general": ["general-purpose"],
        }

        # Find matching patterns
        for pattern, stakeholders in task_patterns.items():
            if pattern in task_lower:
                for stakeholder_name in stakeholders:
                    if stakeholder_name in self.unified_stakeholder_system:
                        return self.unified_stakeholder_system[stakeholder_name]

        # Fallback to general-purpose agent
        if "general-purpose" in self.unified_stakeholder_system:
            return self.unified_stakeholder_system["general-purpose"]

        return None

    def execute_stakeholder_task(
        self, stakeholder_name: str, task_data: dict[str, Any], execution_mode: str = "auto"
    ) -> dict[str, Any]:
        """
        Execute a task using a specific stakeholder.

        Args:
            stakeholder_name: Name of the stakeholder to use
            task_data: Task data and parameters
            execution_mode: Execution mode ("cce", "deep_agents", "hybrid", "auto")

        Returns:
            Task execution result
        """
        if stakeholder_name not in self.unified_stakeholder_system:
            return {
                "success": False,
                "error": f"Stakeholder '{stakeholder_name}' not found",
                "available_stakeholders": list(self.unified_stakeholder_system.keys()),
            }

        stakeholder = self.unified_stakeholder_system[stakeholder_name]

        # Determine execution mode
        if execution_mode == "auto":
            execution_mode = stakeholder.execution_mode

        # Execute based on mode
        if execution_mode == "cce" and stakeholder.cce_agent:
            return self._execute_cce_stakeholder(stakeholder, task_data)
        elif execution_mode == "deep_agents" and stakeholder.deep_agents_subagent:
            return self._execute_deep_agents_stakeholder(stakeholder, task_data)
        elif execution_mode == "hybrid":
            return self._execute_hybrid_stakeholder(stakeholder, task_data)
        else:
            return {
                "success": False,
                "error": f"Execution mode '{execution_mode}' not available for stakeholder '{stakeholder_name}'",
            }

    def _execute_cce_stakeholder(
        self, stakeholder: UnifiedStakeholderAgent, task_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute task using CCE stakeholder system."""
        try:
            integration_challenge = (
                task_data.get("integration_challenge")
                or task_data.get("instruction")
                or task_data.get("task")
                or task_data.get("description")
                or ""
            )
            stakeholder_charter = task_data.get("stakeholder_charter", "")
            thread_id = task_data.get("thread_id") or f"stakeholder-{stakeholder.name}-{int(time.time())}"
            output_directory = task_data.get("output_directory")

            if self.supervisor_graph and hasattr(self.supervisor_graph, "run"):
                result = self.supervisor_graph.run(
                    integration_challenge=integration_challenge,
                    stakeholder_charter=stakeholder_charter,
                    thread_id=thread_id,
                    output_directory=output_directory,
                )
                return {
                    "success": result is not None,
                    "result": result,
                    "execution_mode": "cce",
                    "stakeholder": stakeholder.name,
                }

            if (
                stakeholder.cce_agent
                and hasattr(stakeholder.cce_agent, "analyze")
                and StakeholderContext is not None
            ):
                previous_contributions = task_data.get("previous_contributions", {})
                messages = task_data.get("messages", [])
                context = StakeholderContext(
                    integration_challenge=integration_challenge,
                    charter=stakeholder_charter,
                    previous_contributions=previous_contributions,
                    messages=messages,
                )
                result = stakeholder.cce_agent.analyze(context)
                return {
                    "success": True,
                    "result": result,
                    "execution_mode": "cce",
                    "stakeholder": stakeholder.name,
                }

            return {
                "success": False,
                "error": "CCE stakeholder execution unavailable (no supervisor graph or stakeholder agent).",
                "execution_mode": "cce",
                "stakeholder": stakeholder.name,
            }
        except Exception as e:
            return {"success": False, "error": str(e), "execution_mode": "cce", "stakeholder": stakeholder.name}

    def _execute_deep_agents_stakeholder(
        self, stakeholder: UnifiedStakeholderAgent, task_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute task using deep agents sub-agent."""
        try:
            return self._run_async(self._execute_deep_agents_stakeholder_async(stakeholder, task_data))
        except Exception as e:
            return {"success": False, "error": str(e), "execution_mode": "deep_agents", "stakeholder": stakeholder.name}

    async def _execute_deep_agents_stakeholder_async(
        self, stakeholder: UnifiedStakeholderAgent, task_data: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            instruction = (
                task_data.get("instruction")
                or task_data.get("task")
                or task_data.get("description")
                or f"Assist as {stakeholder.name}."
            )
            context = dict(task_data.get("context") or {})
            context.update({"stakeholder": stakeholder.name, "execution_mode": "deep_agents"})

            executor = self.deep_agents_executor
            if executor is None:
                from src.graphs.utils import get_graph_orchestration_manager

                manager = get_graph_orchestration_manager()
                result = await manager.execute_graph("deep_agents", instruction, context)
            else:
                result = executor(instruction, context)
                if hasattr(result, "__await__"):
                    result = await result

            payload = result if isinstance(result, dict) else {"result": result}
            payload.setdefault("success", True)
            payload["execution_mode"] = "deep_agents"
            payload["stakeholder"] = stakeholder.name
            return payload
        except Exception as e:
            return {"success": False, "error": str(e), "execution_mode": "deep_agents", "stakeholder": stakeholder.name}

    def _run_async(self, coro: Any) -> Any:
        import asyncio

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        if loop.is_running():
            raise RuntimeError("Async execution required when running in an event loop.")
        return loop.run_until_complete(coro)

    def _execute_hybrid_stakeholder(
        self, stakeholder: UnifiedStakeholderAgent, task_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute task using hybrid approach."""
        # Try CCE first, fallback to deep agents
        if stakeholder.cce_agent:
            result = self._execute_cce_stakeholder(stakeholder, task_data)
            if result["success"]:
                result["fallback_used"] = False
                return result

        if stakeholder.deep_agents_subagent:
            result = self._execute_deep_agents_stakeholder(stakeholder, task_data)
            result["fallback_used"] = True
            return result

        return {
            "success": False,
            "error": "Both CCE and deep agents execution failed",
            "execution_mode": "hybrid",
            "stakeholder": stakeholder.name,
        }

    def get_available_stakeholders(self) -> list[str]:
        """
        Get list of available stakeholder names.

        Returns:
            List of available stakeholder names
        """
        return list(self.unified_stakeholder_system.keys())

    def get_stakeholder_info(self, stakeholder_name: str) -> dict[str, Any] | None:
        """
        Get information about a specific stakeholder.

        Args:
            stakeholder_name: Name of the stakeholder

        Returns:
            Stakeholder information dictionary or None if not found
        """
        if stakeholder_name not in self.unified_stakeholder_system:
            return None

        stakeholder = self.unified_stakeholder_system[stakeholder_name]
        return {
            "name": stakeholder.name,
            "description": stakeholder.description,
            "capabilities": stakeholder.capabilities,
            "execution_mode": stakeholder.execution_mode,
            "has_cce_agent": stakeholder.cce_agent is not None,
            "has_deep_agents_subagent": stakeholder.deep_agents_subagent is not None,
        }

    def validate_stakeholder_integration(self) -> dict[str, Any]:
        """
        Validate that stakeholder integration is working correctly.

        Returns:
            Validation results
        """
        validation_results = {
            "success": True,
            "errors": [],
            "warnings": [],
            "stakeholder_counts": len(self.unified_stakeholder_system),
            "available_stakeholders": list(self.unified_stakeholder_system.keys()),
        }

        # Check for critical stakeholders
        critical_stakeholders = ["aider_specialist", "context_engineer", "langgraph_architect"]
        for stakeholder_name in critical_stakeholders:
            if stakeholder_name not in self.unified_stakeholder_system:
                validation_results["errors"].append(f"Critical stakeholder '{stakeholder_name}' not found")
                validation_results["success"] = False

        # Check stakeholder capabilities
        for name, stakeholder in self.unified_stakeholder_system.items():
            if not stakeholder.capabilities:
                validation_results["warnings"].append(f"Stakeholder '{name}' has no capabilities defined")

        # Check execution modes
        for name, stakeholder in self.unified_stakeholder_system.items():
            if stakeholder.execution_mode == "cce" and not stakeholder.cce_agent:
                validation_results["warnings"].append(
                    f"Stakeholder '{name}' set to CCE mode but no CCE agent available"
                )
            elif stakeholder.execution_mode == "deep_agents" and not stakeholder.deep_agents_subagent:
                validation_results["warnings"].append(
                    f"Stakeholder '{name}' set to deep agents mode but no sub-agent available"
                )

        self.logger.info(
            f"Stakeholder integration validation: {'PASSED' if validation_results['success'] else 'FAILED'}"
        )
        return validation_results


# Global instance for easy access
_stakeholder_integration_instance: CCE_StakeholderIntegration | None = None


def get_stakeholder_integration() -> CCE_StakeholderIntegration:
    """
    Get the global stakeholder integration instance.

    Returns:
        CCE_StakeholderIntegration instance
    """
    global _stakeholder_integration_instance
    if _stakeholder_integration_instance is None:
        _stakeholder_integration_instance = CCE_StakeholderIntegration()
        _stakeholder_integration_instance.create_unified_stakeholder_system()
    return _stakeholder_integration_instance


def get_best_stakeholder_for_task(task_description: str) -> UnifiedStakeholderAgent | None:
    """
    Get the best stakeholder for a specific task.

    Args:
        task_description: Description of the task

    Returns:
        Best stakeholder agent for the task or None if not found
    """
    integration = get_stakeholder_integration()
    return integration.get_best_stakeholder_for_task(task_description)
