"""
Advanced Sub-Agent Patterns for CCE Deep Agent

This module implements advanced sub-agent patterns including tool-limited agents,
custom model configurations, and specialized agent types for enhanced security
and flexibility.
"""

import asyncio
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Types of advanced sub-agents."""

    TOOL_LIMITED = "tool_limited"
    CUSTOM_MODEL = "custom_model"
    SPECIALIZED = "specialized"
    SECURITY_FOCUSED = "security_focused"
    PERFORMANCE_OPTIMIZED = "performance_optimized"


class SecurityLevel(Enum):
    """Security levels for sub-agents."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"


class PerformanceProfile(Enum):
    """Performance profiles for sub-agents."""

    FAST = "fast"
    BALANCED = "balanced"
    ACCURATE = "accurate"
    COMPREHENSIVE = "comprehensive"


@dataclass
class ModelConfig:
    """Configuration for custom model agents."""

    model_name: str
    temperature: float = 0.7
    max_tokens: int = 4000
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: int = 30
    retry_count: int = 3
    custom_parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolConfig:
    """Configuration for tool access."""

    allowed_tools: set[str] = field(default_factory=set)
    blocked_tools: set[str] = field(default_factory=set)
    tool_restrictions: dict[str, dict[str, Any]] = field(default_factory=dict)
    require_approval: bool = False
    approval_timeout: int = 300


@dataclass
class SecurityConfig:
    """Security configuration for sub-agents."""

    security_level: SecurityLevel = SecurityLevel.MEDIUM
    sandbox_enabled: bool = True
    network_access: bool = False
    file_access_restricted: bool = True
    allowed_directories: set[str] = field(default_factory=set)
    blocked_directories: set[str] = field(default_factory=set)
    audit_logging: bool = True


@dataclass
class PerformanceConfig:
    """Performance configuration for sub-agents."""

    performance_profile: PerformanceProfile = PerformanceProfile.BALANCED
    max_execution_time: int = 60
    memory_limit_mb: int = 512
    cpu_limit_percent: int = 50
    cache_enabled: bool = True
    parallel_execution: bool = False
    optimization_level: str = "basic"


@dataclass
class AdvancedSubAgentConfig:
    """Configuration for advanced sub-agents."""

    agent_type: AgentType
    name: str
    description: str
    model_config: ModelConfig | None = None
    tool_config: ToolConfig | None = None
    security_config: SecurityConfig | None = None
    performance_config: PerformanceConfig | None = None
    custom_instructions: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class AdvancedSubAgent:
    """
    Advanced sub-agent with specialized configurations.

    This class provides advanced sub-agent patterns including tool-limited agents,
    custom model configurations, and specialized agent types for enhanced security
    and flexibility.
    """

    def __init__(self, config: AdvancedSubAgentConfig):
        self.config = config
        self.agent_type = config.agent_type
        self.name = config.name
        self.description = config.description
        self.model_config = config.model_config
        self.tool_config = config.tool_config
        self.security_config = config.security_config
        self.performance_config = config.performance_config
        self.custom_instructions = config.custom_instructions
        self.metadata = config.metadata

        # Runtime state
        self.created_at = time.time()
        self.execution_count = 0
        self.total_execution_time = 0.0
        self.error_count = 0
        self.last_execution = None

        # Initialize based on agent type
        self._initialize_agent()

    def _initialize_agent(self) -> None:
        """Initialize agent based on type and configuration."""
        try:
            if self.agent_type == AgentType.TOOL_LIMITED:
                self._initialize_tool_limited_agent()
            elif self.agent_type == AgentType.CUSTOM_MODEL:
                self._initialize_custom_model_agent()
            elif self.agent_type == AgentType.SPECIALIZED:
                self._initialize_specialized_agent()
            elif self.agent_type == AgentType.SECURITY_FOCUSED:
                self._initialize_security_focused_agent()
            elif self.agent_type == AgentType.PERFORMANCE_OPTIMIZED:
                self._initialize_performance_optimized_agent()

            logger.info(f"Initialized {self.agent_type.value} agent: {self.name}")

        except Exception as e:
            logger.error(f"Failed to initialize agent {self.name}: {e}")
            raise

    def _initialize_tool_limited_agent(self) -> None:
        """Initialize tool-limited agent."""
        if not self.tool_config:
            self.tool_config = ToolConfig()

        # Set default tool restrictions for security
        if not self.tool_config.allowed_tools:
            self.tool_config.allowed_tools = {"read_file", "ls", "grep", "find", "cat"}

        # Add security-focused instructions
        self.custom_instructions += """
        You are a tool-limited agent with restricted access to system tools.
        You can only use the following tools: {allowed_tools}
        You must not attempt to use any tools not in your allowed list.
        If you need to perform operations outside your tool set, delegate to another agent.
        """.format(allowed_tools=", ".join(self.tool_config.allowed_tools))

    def _initialize_custom_model_agent(self) -> None:
        """Initialize custom model agent."""
        if not self.model_config:
            self.model_config = ModelConfig(
                model_name="claude-sonnet-4-20250514",  # Use Anthropic model to match system
                temperature=0.7,
                max_tokens=4000,
            )

        # Add model-specific instructions
        self.custom_instructions += f"""
        You are using a custom model configuration:
        - Model: {self.model_config.model_name}
        - Temperature: {self.model_config.temperature}
        - Max Tokens: {self.model_config.max_tokens}
        - Timeout: {self.model_config.timeout}s
        """

    def _initialize_specialized_agent(self) -> None:
        """Initialize specialized agent."""
        # Add specialization instructions based on metadata
        specialization = self.metadata.get("specialization", "general")
        self.custom_instructions += f"""
        You are a specialized agent focused on: {specialization}
        You have deep expertise in this domain and should provide detailed, accurate responses.
        When working outside your specialization, clearly indicate your limitations.
        """

    def _initialize_security_focused_agent(self) -> None:
        """Initialize security-focused agent."""
        if not self.security_config:
            self.security_config = SecurityConfig(
                security_level=SecurityLevel.HIGH,
                sandbox_enabled=True,
                network_access=False,
                file_access_restricted=True,
                audit_logging=True,
            )

        # Add security-focused instructions
        self.custom_instructions += """
        You are a security-focused agent with enhanced security measures.
        You must:
        - Validate all inputs for security issues
        - Never execute potentially dangerous operations
        - Log all security-relevant activities
        - Report any suspicious patterns or behaviors
        - Follow security best practices at all times
        """

    def _initialize_performance_optimized_agent(self) -> None:
        """Initialize performance-optimized agent."""
        if not self.performance_config:
            self.performance_config = PerformanceConfig(
                performance_profile=PerformanceProfile.FAST,
                max_execution_time=30,
                memory_limit_mb=256,
                cache_enabled=True,
                optimization_level="aggressive",
            )

        # Add performance-focused instructions
        self.custom_instructions += """
        You are a performance-optimized agent focused on speed and efficiency.
        You should:
        - Prioritize fast responses over comprehensive analysis
        - Use caching when possible
        - Optimize your operations for speed
        - Report performance metrics
        - Minimize resource usage
        """

    async def execute(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Execute a task with the advanced sub-agent.

        Args:
            task: Task to execute
            context: Optional context information

        Returns:
            Execution result
        """
        try:
            start_time = time.time()
            self.execution_count += 1

            # Apply security checks
            if self.security_config:
                security_result = await self._apply_security_checks(task, context)
                if not security_result["allowed"]:
                    return {
                        "success": False,
                        "error": f"Security check failed: {security_result['reason']}",
                        "agent": self.name,
                        "execution_time": time.time() - start_time,
                    }

            # Apply performance limits
            if self.performance_config:
                await self._apply_performance_limits()

            # Execute task based on agent type
            result = await self._execute_task(task, context)

            # Update execution statistics
            execution_time = time.time() - start_time
            self.total_execution_time += execution_time
            self.last_execution = time.time()

            # Add execution metadata
            result.update(
                {
                    "agent": self.name,
                    "agent_type": self.agent_type.value,
                    "execution_time": execution_time,
                    "execution_count": self.execution_count,
                }
            )

            return result

        except Exception as e:
            self.error_count += 1
            logger.error(f"Agent {self.name} execution failed: {e}")
            return {"success": False, "error": str(e), "agent": self.name, "execution_time": time.time() - start_time}

    async def _apply_security_checks(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Apply security checks based on configuration."""
        try:
            # Check security level
            if self.security_config.security_level == SecurityLevel.MAXIMUM:
                # Maximum security - very restrictive
                if any(keyword in task.lower() for keyword in ["delete", "remove", "modify", "change"]):
                    return {"allowed": False, "reason": "Operation not allowed at maximum security level"}

            # Check network access
            if not self.security_config.network_access:
                if any(keyword in task.lower() for keyword in ["download", "upload", "fetch", "curl", "wget"]):
                    return {"allowed": False, "reason": "Network access not allowed"}

            # Check file access restrictions
            if self.security_config.file_access_restricted:
                if any(keyword in task.lower() for keyword in ["/etc/", "/root/", "/sys/", "/proc/"]):
                    return {"allowed": False, "reason": "Restricted file access"}

            # Check blocked directories
            if self.security_config.blocked_directories:
                for blocked_dir in self.security_config.blocked_directories:
                    if blocked_dir in task:
                        return {"allowed": False, "reason": f"Access to {blocked_dir} blocked"}

            return {"allowed": True, "reason": "Security checks passed"}

        except Exception as e:
            logger.error(f"Security check failed: {e}")
            return {"allowed": False, "reason": f"Security check error: {e}"}

    async def _apply_performance_limits(self) -> None:
        """Apply performance limits based on configuration."""
        try:
            # Check execution time limit
            if self.performance_config.max_execution_time:
                # This would be implemented with actual timeout mechanisms
                pass

            # Check memory limit
            if self.performance_config.memory_limit_mb:
                # This would be implemented with actual memory monitoring
                pass

            # Check CPU limit
            if self.performance_config.cpu_limit_percent:
                # This would be implemented with actual CPU monitoring
                pass

        except Exception as e:
            logger.error(f"Performance limit application failed: {e}")

    async def _execute_task(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Execute task based on agent type and configuration."""
        try:
            # Simulate task execution based on agent type
            if self.agent_type == AgentType.TOOL_LIMITED:
                return await self._execute_tool_limited_task(task, context)
            elif self.agent_type == AgentType.CUSTOM_MODEL:
                return await self._execute_custom_model_task(task, context)
            elif self.agent_type == AgentType.SPECIALIZED:
                return await self._execute_specialized_task(task, context)
            elif self.agent_type == AgentType.SECURITY_FOCUSED:
                return await self._execute_security_focused_task(task, context)
            elif self.agent_type == AgentType.PERFORMANCE_OPTIMIZED:
                return await self._execute_performance_optimized_task(task, context)
            else:
                return await self._execute_generic_task(task, context)

        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return {"success": False, "error": str(e)}

    async def _execute_tool_limited_task(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Execute task with tool limitations."""
        # Simulate tool-limited execution
        await asyncio.sleep(0.1)
        return {
            "success": True,
            "result": f"Tool-limited execution of: {task}",
            "tools_used": list(self.tool_config.allowed_tools) if self.tool_config else [],
            "execution_type": "tool_limited",
        }

    async def _execute_custom_model_task(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Execute task with custom model configuration."""
        # Simulate custom model execution
        await asyncio.sleep(0.2)
        return {
            "success": True,
            "result": f"Custom model execution of: {task}",
            "model": self.model_config.model_name if self.model_config else "default",
            "execution_type": "custom_model",
        }

    async def _execute_specialized_task(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Execute task with specialization."""
        # Simulate specialized execution
        await asyncio.sleep(0.15)
        specialization = self.metadata.get("specialization", "general")
        return {
            "success": True,
            "result": f"Specialized execution of: {task}",
            "specialization": specialization,
            "execution_type": "specialized",
        }

    async def _execute_security_focused_task(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Execute task with security focus."""
        # Simulate security-focused execution
        await asyncio.sleep(0.1)
        return {
            "success": True,
            "result": f"Security-focused execution of: {task}",
            "security_level": self.security_config.security_level.value if self.security_config else "medium",
            "execution_type": "security_focused",
        }

    async def _execute_performance_optimized_task(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Execute task with performance optimization."""
        # Simulate performance-optimized execution
        await asyncio.sleep(0.05)  # Faster execution
        return {
            "success": True,
            "result": f"Performance-optimized execution of: {task}",
            "performance_profile": self.performance_config.performance_profile.value
            if self.performance_config
            else "balanced",
            "execution_type": "performance_optimized",
        }

    async def _execute_generic_task(self, task: str, context: dict[str, Any] | None) -> dict[str, Any]:
        """Execute generic task."""
        # Simulate generic execution
        await asyncio.sleep(0.1)
        return {"success": True, "result": f"Generic execution of: {task}", "execution_type": "generic"}

    def get_agent_stats(self) -> dict[str, Any]:
        """Get agent statistics."""
        try:
            avg_execution_time = self.total_execution_time / self.execution_count if self.execution_count > 0 else 0.0

            return {
                "name": self.name,
                "agent_type": self.agent_type.value,
                "created_at": self.created_at,
                "execution_count": self.execution_count,
                "total_execution_time": self.total_execution_time,
                "average_execution_time": avg_execution_time,
                "error_count": self.error_count,
                "error_rate": self.error_count / self.execution_count if self.execution_count > 0 else 0.0,
                "last_execution": self.last_execution,
                "uptime": time.time() - self.created_at,
            }

        except Exception as e:
            logger.error(f"Failed to get agent stats: {e}")
            return {"error": str(e)}

    def update_config(self, config_updates: dict[str, Any]) -> None:
        """Update agent configuration."""
        try:
            # Update model config
            if "model_config" in config_updates and self.model_config:
                for key, value in config_updates["model_config"].items():
                    if hasattr(self.model_config, key):
                        setattr(self.model_config, key, value)

            # Update tool config
            if "tool_config" in config_updates and self.tool_config:
                for key, value in config_updates["tool_config"].items():
                    if hasattr(self.tool_config, key):
                        setattr(self.tool_config, key, value)

            # Update security config
            if "security_config" in config_updates and self.security_config:
                for key, value in config_updates["security_config"].items():
                    if hasattr(self.security_config, key):
                        setattr(self.security_config, key, value)

            # Update performance config
            if "performance_config" in config_updates and self.performance_config:
                for key, value in config_updates["performance_config"].items():
                    if hasattr(self.performance_config, key):
                        setattr(self.performance_config, key, value)

            # Update metadata
            if "metadata" in config_updates:
                self.metadata.update(config_updates["metadata"])

            logger.info(f"Updated configuration for agent: {self.name}")

        except Exception as e:
            logger.error(f"Failed to update agent configuration: {e}")


class AdvancedSubAgentManager:
    """
    Manager for advanced sub-agents.

    This class provides management capabilities for advanced sub-agents including
    creation, configuration, and lifecycle management.
    """

    def __init__(self):
        self.agents: dict[str, AdvancedSubAgent] = {}
        self.agent_types: dict[AgentType, list[str]] = defaultdict(list)
        self.created_at = time.time()

    def create_tool_limited_agent(self, name: str, allowed_tools: set[str], description: str = "") -> AdvancedSubAgent:
        """
        Create sub-agent with limited tool access for security.

        Args:
            name: Agent name
            allowed_tools: Set of allowed tools
            description: Agent description

        Returns:
            Created tool-limited agent
        """
        try:
            config = AdvancedSubAgentConfig(
                agent_type=AgentType.TOOL_LIMITED,
                name=name,
                description=description or f"Tool-limited agent with access to: {', '.join(allowed_tools)}",
                tool_config=ToolConfig(allowed_tools=allowed_tools, require_approval=True),
                security_config=SecurityConfig(
                    security_level=SecurityLevel.HIGH, sandbox_enabled=True, audit_logging=True
                ),
            )

            agent = AdvancedSubAgent(config)
            self._register_agent(agent)

            logger.info(f"Created tool-limited agent: {name}")
            return agent

        except Exception as e:
            logger.error(f"Failed to create tool-limited agent: {e}")
            raise

    def create_custom_model_agent(
        self, name: str, model_config: ModelConfig, description: str = ""
    ) -> AdvancedSubAgent:
        """
        Create sub-agent with custom model configuration.

        Args:
            name: Agent name
            model_config: Model configuration
            description: Agent description

        Returns:
            Created custom model agent
        """
        try:
            config = AdvancedSubAgentConfig(
                agent_type=AgentType.CUSTOM_MODEL,
                name=name,
                description=description or f"Custom model agent using {model_config.model_name}",
                model_config=model_config,
                performance_config=PerformanceConfig(
                    performance_profile=PerformanceProfile.ACCURATE, cache_enabled=True
                ),
            )

            agent = AdvancedSubAgent(config)
            self._register_agent(agent)

            logger.info(f"Created custom model agent: {name}")
            return agent

        except Exception as e:
            logger.error(f"Failed to create custom model agent: {e}")
            raise

    def create_specialized_agent(self, name: str, specialization: str, description: str = "") -> AdvancedSubAgent:
        """
        Create specialized sub-agent.

        Args:
            name: Agent name
            specialization: Specialization domain
            description: Agent description

        Returns:
            Created specialized agent
        """
        try:
            config = AdvancedSubAgentConfig(
                agent_type=AgentType.SPECIALIZED,
                name=name,
                description=description or f"Specialized agent for {specialization}",
                metadata={"specialization": specialization},
                performance_config=PerformanceConfig(
                    performance_profile=PerformanceProfile.COMPREHENSIVE, cache_enabled=True
                ),
            )

            agent = AdvancedSubAgent(config)
            self._register_agent(agent)

            logger.info(f"Created specialized agent: {name} for {specialization}")
            return agent

        except Exception as e:
            logger.error(f"Failed to create specialized agent: {e}")
            raise

    def create_security_focused_agent(
        self, name: str, security_level: SecurityLevel = SecurityLevel.HIGH, description: str = ""
    ) -> AdvancedSubAgent:
        """
        Create security-focused sub-agent.

        Args:
            name: Agent name
            security_level: Security level
            description: Agent description

        Returns:
            Created security-focused agent
        """
        try:
            config = AdvancedSubAgentConfig(
                agent_type=AgentType.SECURITY_FOCUSED,
                name=name,
                description=description or f"Security-focused agent with {security_level.value} security",
                security_config=SecurityConfig(
                    security_level=security_level,
                    sandbox_enabled=True,
                    network_access=False,
                    file_access_restricted=True,
                    audit_logging=True,
                ),
                tool_config=ToolConfig(require_approval=True, approval_timeout=300),
            )

            agent = AdvancedSubAgent(config)
            self._register_agent(agent)

            logger.info(f"Created security-focused agent: {name}")
            return agent

        except Exception as e:
            logger.error(f"Failed to create security-focused agent: {e}")
            raise

    def create_performance_optimized_agent(
        self, name: str, performance_profile: PerformanceProfile = PerformanceProfile.FAST, description: str = ""
    ) -> AdvancedSubAgent:
        """
        Create performance-optimized sub-agent.

        Args:
            name: Agent name
            performance_profile: Performance profile
            description: Agent description

        Returns:
            Created performance-optimized agent
        """
        try:
            config = AdvancedSubAgentConfig(
                agent_type=AgentType.PERFORMANCE_OPTIMIZED,
                name=name,
                description=description or f"Performance-optimized agent with {performance_profile.value} profile",
                performance_config=PerformanceConfig(
                    performance_profile=performance_profile,
                    max_execution_time=30,
                    memory_limit_mb=256,
                    cache_enabled=True,
                    optimization_level="aggressive",
                ),
            )

            agent = AdvancedSubAgent(config)
            self._register_agent(agent)

            logger.info(f"Created performance-optimized agent: {name}")
            return agent

        except Exception as e:
            logger.error(f"Failed to create performance-optimized agent: {e}")
            raise

    def _register_agent(self, agent: AdvancedSubAgent) -> None:
        """Register agent in the manager."""
        self.agents[agent.name] = agent
        self.agent_types[agent.agent_type].append(agent.name)

    def get_agent(self, name: str) -> AdvancedSubAgent | None:
        """Get agent by name."""
        return self.agents.get(name)

    def get_agents_by_type(self, agent_type: AgentType) -> list[AdvancedSubAgent]:
        """Get agents by type."""
        return [self.agents[name] for name in self.agent_types[agent_type] if name in self.agents]

    def get_all_agents(self) -> list[AdvancedSubAgent]:
        """Get all agents."""
        return list(self.agents.values())

    def remove_agent(self, name: str) -> bool:
        """Remove agent from manager."""
        try:
            if name in self.agents:
                agent = self.agents[name]
                del self.agents[name]
                self.agent_types[agent.agent_type].remove(name)
                logger.info(f"Removed agent: {name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove agent: {e}")
            return False

    def get_manager_stats(self) -> dict[str, Any]:
        """Get manager statistics."""
        try:
            total_agents = len(self.agents)
            total_executions = sum(agent.execution_count for agent in self.agents.values())
            total_errors = sum(agent.error_count for agent in self.agents.values())

            return {
                "total_agents": total_agents,
                "agents_by_type": {agent_type.value: len(agents) for agent_type, agents in self.agent_types.items()},
                "total_executions": total_executions,
                "total_errors": total_errors,
                "error_rate": total_errors / total_executions if total_executions > 0 else 0.0,
                "uptime": time.time() - self.created_at,
            }

        except Exception as e:
            logger.error(f"Failed to get manager stats: {e}")
            return {"error": str(e)}


# Global advanced sub-agent manager instance
_advanced_agent_manager = None


def get_advanced_agent_manager() -> AdvancedSubAgentManager:
    """Get the global advanced sub-agent manager instance."""
    global _advanced_agent_manager
    if _advanced_agent_manager is None:
        _advanced_agent_manager = AdvancedSubAgentManager()
    return _advanced_agent_manager
