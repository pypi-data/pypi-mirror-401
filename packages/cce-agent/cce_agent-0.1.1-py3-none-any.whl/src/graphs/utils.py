"""
Graph orchestration helpers shared across CCE systems.

This module wraps existing graphs (AiderGraph, OpenSWEToolsGraph) for reuse.
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from typing import Any, Callable

try:
    from .aider_graph import AiderGraph
    from .open_swe_tools_graph import OpenSWEToolsGraph

    GRAPHS_AVAILABLE = True
except ImportError:
    GRAPHS_AVAILABLE = False
    AiderGraph = None
    OpenSWEToolsGraph = None

logger = logging.getLogger(__name__)


class GraphWrapperBase:
    """Base class for graph wrappers that convert existing graphs to sub-agent patterns."""

    def __init__(self, graph_instance: Any, graph_name: str):
        self.graph = graph_instance
        self.graph_name = graph_name
        self.logger = logging.getLogger(f"{__name__}.{graph_name}")

        self.logger.info("🔗 Wrapped %s as sub-agent", graph_name)

    async def execute(self, instruction: str, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement execute method")

    def get_capabilities(self) -> list[str]:
        raise NotImplementedError("Subclasses must implement get_capabilities method")


class AiderGraphSubAgent(GraphWrapperBase):
    """Wrapper for AiderGraph as deep agents sub-agent."""

    def __init__(self, aider_graph: AiderGraph):
        super().__init__(aider_graph, "AiderGraph")
        self.aider_graph = aider_graph

    async def execute(self, instruction: str, context: dict[str, Any]) -> dict[str, Any]:
        try:
            target_files = context.get("target_files", [])
            auto_approve = context.get("auto_approve", True)
            structured_phases = context.get("structured_phases")

            self.logger.info("🚀 Executing AiderGraph with instruction: %s...", instruction[:100])

            result = await self.aider_graph.run(
                instruction=instruction,
                target_files=target_files,
                auto_approve=auto_approve,
                structured_phases=structured_phases,
            )

            self.logger.info("✅ AiderGraph execution completed successfully")

            return {
                "success": True,
                "result": result,
                "graph_name": "AiderGraph",
                "execution_time": datetime.now(UTC).isoformat(),
                "instruction": instruction,
                "target_files": target_files,
            }

        except Exception as exc:
            self.logger.error("❌ AiderGraph execution failed: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "graph_name": "AiderGraph",
                "execution_time": datetime.now(UTC).isoformat(),
                "instruction": instruction,
            }

    def get_capabilities(self) -> list[str]:
        return [
            "Code analysis and repository mapping",
            "Multi-strategy code editing (UnifiedDiff, EditBlock, WholeFile)",
            "Validation pipelines and automated testing",
            "Git operations and safety mechanisms",
            "Structured workflow execution",
            "Human approval integration",
            "Rollback and error recovery",
        ]


class OpenSWEGraphSubAgent(GraphWrapperBase):
    """Wrapper for OpenSWEToolsGraph as deep agents sub-agent."""

    def __init__(self, openswe_graph: OpenSWEToolsGraph):
        super().__init__(openswe_graph, "OpenSWEToolsGraph")
        self.openswe_graph = openswe_graph

    async def execute(self, instruction: str, context: dict[str, Any]) -> dict[str, Any]:
        try:
            target_files = context.get("target_files", [])
            auto_approve = context.get("auto_approve", True)
            structured_phases = context.get("structured_phases")

            self.logger.info("🚀 Executing OpenSWEToolsGraph with instruction: %s...", instruction[:100])

            result = await self.openswe_graph.run(
                instruction=instruction,
                target_files=target_files,
                auto_approve=auto_approve,
                structured_phases=structured_phases,
            )

            self.logger.info("✅ OpenSWEToolsGraph execution completed successfully")

            return {
                "success": True,
                "result": result,
                "graph_name": "OpenSWEToolsGraph",
                "execution_time": datetime.now(UTC).isoformat(),
                "instruction": instruction,
                "target_files": target_files,
            }

        except Exception as exc:
            self.logger.error("❌ OpenSWEToolsGraph execution failed: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "graph_name": "OpenSWEToolsGraph",
                "execution_time": datetime.now(UTC).isoformat(),
                "instruction": instruction,
            }

    def get_capabilities(self) -> list[str]:
        return [
            "Repository discovery and mapping",
            "Semantic code analysis and ranking",
            "Multi-strategy code editing",
            "Comprehensive validation pipelines",
            "Git workflow management",
            "Structured output generation",
            "Error handling and recovery",
        ]


class DeepAgentsGraphSubAgent(GraphWrapperBase):
    """Wrapper for Deep Agents graph execution."""

    def __init__(self, agent_factory: Callable[[], Any]):
        super().__init__(None, "DeepAgents")
        self._agent_factory = agent_factory
        self._agent: Any | None = None

    def _get_agent(self) -> Any:
        if self._agent is None:
            self._agent = self._agent_factory()
            self.graph = self._agent
        return self._agent

    async def execute(self, instruction: str, context: dict[str, Any]) -> dict[str, Any]:
        try:
            agent = self._get_agent()
            from langchain_core.messages import HumanMessage

            message = HumanMessage(content=instruction)
            if hasattr(agent, "invoke_with_filesystem"):
                result = await agent.invoke_with_filesystem(
                    [message],
                    context_memory=context or {},
                    remaining_steps=1000,
                    execution_phases=[{"cycle_count": 0}],
                )
            else:
                state = {
                    "messages": [message],
                    "remaining_steps": 1000,
                    "context_memory": context or {},
                    "execution_phases": [{"cycle_count": 0}],
                }
                result = await agent.ainvoke(state)

            return {
                "success": True,
                "result": result,
                "graph_name": "deep_agents",
                "execution_time": datetime.now(UTC).isoformat(),
                "instruction": instruction,
            }

        except Exception as exc:
            self.logger.error("❌ Deep agents graph execution failed: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "graph_name": "deep_agents",
                "execution_time": datetime.now(UTC).isoformat(),
                "instruction": instruction,
            }

    def get_capabilities(self) -> list[str]:
        return [
            "LLM-based code editing",
            "Sub-agent coordination",
            "Planning and task management",
            "Virtual filesystem operations",
            "Context-aware code generation",
        ]


class GraphOrchestrationManager:
    """Unified interface for executing graph workflows."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.graph_wrappers: dict[str, GraphWrapperBase] = {}

        self.logger.info("🎭 GraphOrchestrationManager initialized")

    def register_graph(self, name: str, graph_wrapper: GraphWrapperBase) -> None:
        self.graph_wrappers[name] = graph_wrapper
        self.logger.info("📝 Registered graph: %s", name)

    def register_aider_graph(self, aider_graph: AiderGraph) -> None:
        if not GRAPHS_AVAILABLE:
            self.logger.warning("Graphs not available - cannot register AiderGraph")
            return

        wrapper = AiderGraphSubAgent(aider_graph)
        self.register_graph("aider", wrapper)

    def register_openswe_graph(self, openswe_graph: OpenSWEToolsGraph) -> None:
        if not GRAPHS_AVAILABLE:
            self.logger.warning("Graphs not available - cannot register OpenSWEToolsGraph")
            return

        wrapper = OpenSWEGraphSubAgent(openswe_graph)
        self.register_graph("openswe", wrapper)

    def register_deep_agents_graph(self, agent_factory: Callable[[], Any]) -> None:
        wrapper = DeepAgentsGraphSubAgent(agent_factory)
        self.register_graph("deep_agents", wrapper)

    async def execute_graph(
        self, graph_name: str, instruction: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if graph_name not in self.graph_wrappers:
            error_msg = f"Graph not found: {graph_name}. Available: {list(self.graph_wrappers.keys())}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg, "graph_name": graph_name}

        try:
            self.logger.info("🎭 Executing graph: %s", graph_name)
            result = await self.graph_wrappers[graph_name].execute(instruction=instruction, context=context or {})
            self.logger.info("✅ Graph execution completed: %s", graph_name)
            return result

        except Exception as exc:
            error_msg = f"Graph execution failed: {exc}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg, "graph_name": graph_name}

    def get_available_graphs(self) -> list[str]:
        return list(self.graph_wrappers.keys())

    def get_graph_capabilities(self, graph_name: str) -> list[str] | None:
        if graph_name not in self.graph_wrappers:
            return None
        return self.graph_wrappers[graph_name].get_capabilities()

    def get_all_capabilities(self) -> dict[str, list[str]]:
        return {name: wrapper.get_capabilities() for name, wrapper in self.graph_wrappers.items()}

    def get_statistics(self) -> dict[str, Any]:
        return {
            "total_graphs": len(self.graph_wrappers),
            "available_graphs": list(self.graph_wrappers.keys()),
            "graphs_available": GRAPHS_AVAILABLE,
        }

    def get_graph_statistics(self) -> dict[str, Any]:
        return self.get_statistics()


_GRAPH_ORCHESTRATION_MANAGER: GraphOrchestrationManager | None = None


def _semantic_ranking_available() -> bool:
    try:
        from src.semantic.embeddings import OPENAI_AVAILABLE, SENTENCE_TRANSFORMERS_AVAILABLE
    except Exception:
        return False

    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        return True
    if SENTENCE_TRANSFORMERS_AVAILABLE:
        return True
    return False


def _resolve_workspace_root() -> str:
    from src.workspace_context import get_workspace_root

    stored_root = get_workspace_root()
    if stored_root:
        return os.path.abspath(stored_root)
    return os.getcwd()


def _build_editor_llm() -> Any | None:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass

    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model=os.getenv("OPEN_SWE_MODEL", "claude-sonnet-4-20250514"),
                temperature=0,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
            )
        except Exception as exc:
            logger.warning("Failed to initialize Anthropic editor LLM: %s", exc)
            return None

    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=os.getenv("OPEN_SWE_MODEL", "gpt-4o"),
                temperature=0,
            )
        except Exception as exc:
            logger.warning("Failed to initialize OpenAI editor LLM: %s", exc)
            return None

    logger.info("OpenSWE editor LLM not configured; skipping OpenSWE graph registration")
    return None


def _build_aider_graph() -> AiderGraph | None:
    if not GRAPHS_AVAILABLE or AiderGraph is None:
        return None

    try:
        from ..tools.aider.wrapper import AiderctlWrapper
        from ..tools.git_ops import GitOps
        from ..tools.shell_runner import ShellRunner
        from ..tools.validation.runner import ValidationRunner

        workspace_root = _resolve_workspace_root()
        shell_runner = ShellRunner(workspace_root)
        git_ops = GitOps(shell_runner)
        aider_wrapper = AiderctlWrapper(cwd=workspace_root, force_mode=True, strict_mode=False)
        validation_runner = ValidationRunner(aider_wrapper)

        return AiderGraph(
            aider_wrapper=aider_wrapper,
            git_ops=git_ops,
            validation_runner=validation_runner,
            enable_semantic_ranking=_semantic_ranking_available(),
        )
    except Exception as exc:
        logger.warning("Failed to initialize AiderGraph: %s", exc)
        return None


def _build_open_swe_graph() -> OpenSWEToolsGraph | None:
    if not GRAPHS_AVAILABLE or OpenSWEToolsGraph is None:
        return None

    try:
        from ..tools.git_ops import GitOps
        from ..tools.openswe.code_tools import CodeTools
        from ..tools.shell_runner import ShellRunner
        from ..tools.validation.linting import LintingManager
        from ..tools.validation.runner import ValidationRunner
        from ..tools.validation.testing import FrameworkTestManager

        editor_llm = _build_editor_llm()
        if editor_llm is None:
            return None

        workspace_root = _resolve_workspace_root()
        shell_runner = ShellRunner(workspace_root)
        git_ops = GitOps(shell_runner)
        linting = LintingManager(workspace_root)
        testing = FrameworkTestManager(workspace_root)
        code_tools = CodeTools(
            workspace_root=workspace_root,
            shell_runner=shell_runner,
            git_ops=git_ops,
            linting=linting,
            testing=testing,
            editor_llm=editor_llm,
        )
        validation_runner = ValidationRunner(code_tools)

        return OpenSWEToolsGraph(
            code_tools=code_tools,
            git_ops=git_ops,
            validation_runner=validation_runner,
        )
    except Exception as exc:
        logger.warning("Failed to initialize OpenSWEToolsGraph: %s", exc)
        return None


def _build_deep_agents_factory() -> Callable[[], Any] | None:
    try:
        from src.deep_agents.cce_deep_agent import createCCEDeepAgent
    except Exception as exc:
        logger.warning("Deep agents not available: %s", exc)
        return None

    if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")):
        logger.warning("Deep agents API key not configured; skipping deep_agents graph registration")
        return None

    def _factory() -> Any:
        return createCCEDeepAgent(workspace_root=_resolve_workspace_root())

    return _factory


def register_default_graphs(manager: GraphOrchestrationManager, *, deep_agents_only: bool = False) -> dict[str, Any]:
    """Register available graph wrappers with the orchestration manager."""
    if not manager:
        return {"available_graphs": []}

    existing = set(manager.get_available_graphs())
    if not deep_agents_only:
        if "aider" not in existing:
            aider_graph = _build_aider_graph()
            if aider_graph is not None:
                manager.register_aider_graph(aider_graph)

        if "openswe" not in existing:
            open_swe_graph = _build_open_swe_graph()
            if open_swe_graph is not None:
                manager.register_openswe_graph(open_swe_graph)

    if "deep_agents" not in existing:
        deep_agents_factory = _build_deep_agents_factory()
        if deep_agents_factory is not None:
            manager.register_deep_agents_graph(deep_agents_factory)

    return {"available_graphs": manager.get_available_graphs()}


def get_graph_orchestration_manager(
    *, register_defaults: bool = True, deep_agents_only: bool = False
) -> GraphOrchestrationManager:
    global _GRAPH_ORCHESTRATION_MANAGER
    if _GRAPH_ORCHESTRATION_MANAGER is None:
        _GRAPH_ORCHESTRATION_MANAGER = GraphOrchestrationManager()

    if register_defaults:
        register_default_graphs(_GRAPH_ORCHESTRATION_MANAGER, deep_agents_only=deep_agents_only)

    return _GRAPH_ORCHESTRATION_MANAGER


__all__ = [
    "GraphWrapperBase",
    "AiderGraphSubAgent",
    "DeepAgentsGraphSubAgent",
    "OpenSWEGraphSubAgent",
    "GraphOrchestrationManager",
    "GRAPHS_AVAILABLE",
    "get_graph_orchestration_manager",
    "register_default_graphs",
]
