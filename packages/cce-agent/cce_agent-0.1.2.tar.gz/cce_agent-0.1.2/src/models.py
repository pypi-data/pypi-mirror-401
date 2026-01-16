"""
Dynamic Model Selection & Fallbacks for CCE Agent

Provides intelligent model selection based on task requirements,
with fallback strategies and rate limiting capabilities.
"""

import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

try:
    from langchain_anthropic import ChatAnthropic
    from langchain_openai import ChatOpenAI

    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False

from datetime import datetime

from langchain_core.language_models import BaseChatModel


@dataclass
class GitHubComment:
    """Represents a GitHub issue comment."""

    id: int
    author: str
    body: str
    created_at: datetime
    updated_at: datetime
    reactions: dict[str, int] = field(default_factory=dict)


@dataclass
class Ticket:
    """Enhanced GitHub ticket/issue representation."""

    number: int
    title: str
    description: str
    url: str
    labels: list[str] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    # Enhanced GitHub metadata
    state: str = "open"  # open/closed
    author: str = ""
    assignees: list[str] = field(default_factory=list)
    milestone: str | None = None

    # Comments and interactions
    comments: list["GitHubComment"] = field(default_factory=list)
    reactions: dict[str, int] = field(default_factory=dict)

    @property
    def body(self) -> str:
        """Alias for description to maintain compatibility."""
        return self.description

    @property
    def assignee(self) -> str | None:
        """Single assignee for backward compatibility."""
        return self.assignees[0] if self.assignees else None


@dataclass
class TokenUsage:
    """Token usage tracking for a specific operation."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    model_name: str
    operation: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolCall:
    """Represents a tool call made during execution."""

    tool_name: str
    arguments: dict[str, Any]
    result: str | None = None
    error: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    duration_seconds: float = 0.0


@dataclass
class CycleCompleteSignal:
    """Signal details when an agent requests to end a cycle."""

    summary: str
    work_remaining: str
    next_focus_suggestion: str
    method: str = "tool_call"
    raw_content: str | None = None


@dataclass
class PlanResult:
    """Lightweight plan summary used for decision gating."""

    plan: str
    structured_phases: list[dict[str, Any]] | None = None
    plan_complete: bool | None = None


@dataclass
class ReconciliationResult:
    """Signals derived from reconciliation for decision gating."""

    plan_complete: bool | None = None
    tests_passing: bool | None = None
    critical_errors: list[str] = field(default_factory=list)
    agent_signaled_completion: bool | None = None
    agent_signaled_failure: bool | None = None


@dataclass
class CycleResult:
    """Results from an execution cycle."""

    cycle_number: int
    status: str  # "success", "failure", "running"
    orientation: str
    start_time: datetime
    end_time: datetime | None = None
    messages_count: int = 0
    tool_calls: list[ToolCall] = field(default_factory=list)
    token_usage: list[TokenUsage] = field(default_factory=list)
    final_summary: str = ""
    commit_sha: str | None = None
    commit_message: str | None = None
    step_count: int = 0
    duration_seconds: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    tests_run: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    linting_passed: bool | None = None
    cycle_summary: str = ""
    next_focus_suggestion: str | None = None
    work_remaining: str | None = None
    files_created: list[str] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)
    files_deleted: list[str] = field(default_factory=list)

    # Wrap-up tracking (optional)
    soft_limit: int | None = None
    soft_limit_reached: bool | None = None
    step_count: int | None = None
    steps_in_main_phase: int | None = None
    steps_in_wrap_up_phase: int | None = None
    wrap_up_issues: list[str] = field(default_factory=list)
    wrap_up_tests_run: bool | None = None
    wrap_up_tests_passed: bool | None = None
    wrap_up_linting_run: bool | None = None
    wrap_up_linting_passed: bool | None = None
    wrap_up_cycle_report_prepared: bool | None = None

    # Cycle completion signal (optional)
    cycle_summary: str | None = None
    work_remaining: str | None = None
    next_focus_suggestion: str | None = None
    ready_to_end: bool | None = None
    cycle_complete_signal_method: str | None = None
    cycle_metrics: dict[str, Any] | None = None

    # Legacy fields for backward compatibility
    history: list[str] = field(default_factory=list)
    final_thought: str = ""

    def _sanitize_value(self, value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        if isinstance(value, list):
            return [self._sanitize_value(item) for item in value]
        if isinstance(value, dict):
            return {str(key): self._sanitize_value(val) for key, val in value.items()}
        if hasattr(value, "__dataclass_fields__"):
            return {field: self._sanitize_value(getattr(value, field)) for field in value.__dataclass_fields__}
        return str(value)

    def _serialize_tool_call(self, tool_call: ToolCall) -> dict[str, Any]:
        return {
            "tool_name": tool_call.tool_name,
            "arguments": self._sanitize_value(tool_call.arguments),
            "result": self._sanitize_value(tool_call.result),
            "error": self._sanitize_value(tool_call.error),
            "timestamp": self._sanitize_value(tool_call.timestamp),
            "duration_seconds": self._sanitize_value(tool_call.duration_seconds),
        }

    def _serialize_token_usage(self, usage: TokenUsage) -> dict[str, Any]:
        return {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "model_name": usage.model_name,
            "operation": usage.operation,
            "timestamp": self._sanitize_value(usage.timestamp),
        }

    def to_dict(self) -> dict[str, Any]:
        cycle_summary = self.cycle_summary or self.final_summary
        return {
            "cycle_number": self.cycle_number,
            "status": self.status,
            "orientation": self.orientation,
            "start_time": self._sanitize_value(self.start_time),
            "end_time": self._sanitize_value(self.end_time),
            "duration_seconds": self.duration_seconds,
            "messages_count": self.messages_count,
            "step_count": self.step_count,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "linting_passed": self.linting_passed,
            "cycle_summary": cycle_summary,
            "final_summary": self.final_summary,
            "next_focus_suggestion": self.next_focus_suggestion,
            "work_remaining": self.work_remaining,
            "files_created": self._sanitize_value(self.files_created),
            "files_modified": self._sanitize_value(self.files_modified),
            "files_deleted": self._sanitize_value(self.files_deleted),
            "soft_limit": self.soft_limit,
            "soft_limit_reached": self.soft_limit_reached,
            "steps_in_main_phase": self.steps_in_main_phase,
            "steps_in_wrap_up_phase": self.steps_in_wrap_up_phase,
            "wrap_up_issues": self._sanitize_value(self.wrap_up_issues),
            "tool_calls_count": len(self.tool_calls),
            "token_usage_count": len(self.token_usage),
            "tool_calls": [self._serialize_tool_call(call) for call in self.tool_calls],
            "token_usage": [self._serialize_token_usage(usage) for usage in self.token_usage],
            "cycle_metrics": self._sanitize_value(self.cycle_metrics),
            "history_count": len(self.history),
        }

    def to_summary(self) -> dict[str, Any]:
        cycle_summary = self.cycle_summary or self.final_summary
        return {
            "cycle_number": self.cycle_number,
            "status": self.status,
            "orientation": self.orientation,
            "duration_seconds": self.duration_seconds,
            "messages_count": self.messages_count,
            "step_count": self.step_count,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "linting_passed": self.linting_passed,
            "cycle_summary": cycle_summary,
            "next_focus_suggestion": self.next_focus_suggestion,
            "work_remaining": self.work_remaining,
            "files_created": self.files_created,
            "files_modified": self.files_modified,
            "files_deleted": self.files_deleted,
            "soft_limit": self.soft_limit,
            "soft_limit_reached": self.soft_limit_reached,
            "steps_in_main_phase": self.steps_in_main_phase,
            "steps_in_wrap_up_phase": self.steps_in_wrap_up_phase,
            "wrap_up_issues": self.wrap_up_issues,
        }


@dataclass
class TestAttempt:
    """Record of a single test attempt during execution."""

    test_path: str
    attempt_number: int
    passed: bool
    failure_reason: str | None = None
    fix_applied: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class OrientationResult:
    """Orientation for an execution cycle."""

    focus: str
    focus_description: str
    relevant_files: list[str]
    relevant_plan_items: list[str]
    suggested_approach: str
    acceptance_criteria: list[str]
    target_steps: int = 20
    previous_cycle_summary: str | None = None
    previous_suggestion: str | None = None
    cycle_number: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CycleReconciliationResult:
    """Reconciliation output for an execution cycle."""
    cycle_number: int
    status: str
    items_completed: list[str] = field(default_factory=list)
    items_in_progress: list[str] = field(default_factory=list)
    tests_passed: int = 0
    tests_failed: int = 0
    commit_sha: str | None = None
    next_focus_suggestion: str | None = None
    summary: str = ""
    errors: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PlanningResult:
    """Results from the planning phase."""

    status: str  # "success", "failure"
    iterations: int
    consensus_reached: bool
    shared_plan: str
    technical_analysis: str
    architectural_analysis: str
    messages_count: int = 0
    tool_calls: list[ToolCall] = field(default_factory=list)
    token_usage: list[TokenUsage] = field(default_factory=list)


@dataclass
class RunResult:
    """Complete results from a ticket processing run."""

    ticket: Ticket
    thread_id: str
    status: str  # "success", "failure", "error"
    planning_result: PlanningResult | None = None
    execution_cycles: list[CycleResult] = field(default_factory=list)
    final_summary: str = ""
    error_message: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    total_duration_seconds: float = 0.0


@dataclass
class RunLog:
    """Complete run log with all tracking information."""

    thread_id: str
    run_id: str
    ticket: Ticket
    start_time: datetime
    end_time: datetime | None = None
    status: str = "running"  # "running", "completed", "failed"

    # Planning phase
    planning_result: PlanningResult | None = None

    # Execution phase
    execution_cycles: list[CycleResult] = field(default_factory=list)

    # Aggregated metrics
    total_messages: int = 0
    total_tool_calls: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0

    # Final results
    final_summary: str = ""
    error_message: str = ""

    def generate_thread_id(self) -> str:
        """Generate a unique thread ID for this run."""
        import uuid
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"{timestamp}_{unique_id}_ticket_{self.ticket.number}"

    def add_token_usage(self, usage: TokenUsage) -> None:
        """Add token usage to aggregated totals."""
        self.total_prompt_tokens += usage.prompt_tokens
        self.total_completion_tokens += usage.completion_tokens
        self.total_tokens += usage.total_tokens

    def get_total_tokens(self) -> int:
        """Get total token count for this run."""
        return self.total_tokens


class TaskType(Enum):
    """Types of tasks for model selection."""

    PLANNING = "planning"
    DRAFTING = "drafting"
    VALIDATION = "validation"
    SYNTHESIS = "synthesis"
    ANALYSIS = "analysis"
    EDITING = "editing"
    REVIEW = "review"


class ModelTier(Enum):
    """Model capability tiers."""

    PREMIUM = "premium"  # GPT-4, Claude-3 Opus
    STANDARD = "standard"  # GPT-4o, Claude-3.5 Sonnet
    EFFICIENT = "efficient"  # GPT-3.5, Claude-3 Haiku
    FALLBACK = "fallback"  # Backup models


@dataclass
class ModelConfig:
    """Configuration for a specific model."""

    name: str
    provider: str
    tier: ModelTier
    max_tokens: int = 4096
    temperature: float = 0.0
    cost_per_token: float = 0.0
    rate_limit_rpm: int = 3500
    capabilities: list[str] = field(default_factory=list)

    def create_instance(self, **kwargs) -> BaseChatModel:
        """Create an instance of this model."""
        model_kwargs = {"model": self.name, "max_tokens": self.max_tokens, "temperature": self.temperature, **kwargs}

        if self.provider == "openai":
            return ChatOpenAI(**model_kwargs)
        elif self.provider == "anthropic":
            return ChatAnthropic(**model_kwargs)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")


@dataclass
class RateLimitState:
    """Track rate limiting state for a model."""

    requests_made: int = 0
    window_start: float = field(default_factory=time.time)
    last_request: float = 0.0
    backoff_until: float = 0.0


class ModelSelector:
    """
    Intelligent model selection with fallback strategies.

    Selects appropriate models based on task type, handles rate limiting,
    and provides fallback mechanisms for reliability.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Define available models
        self.models = self._initialize_models()

        # Task-to-model preferences
        self.task_preferences = self._initialize_task_preferences()

        # Rate limiting state
        self.rate_limits: dict[str, RateLimitState] = {}

        # Fallback chains
        self.fallback_chains = self._initialize_fallback_chains()

        self.logger.info(f"🎯 ModelSelector initialized with {len(self.models)} models")

    def _initialize_models(self) -> dict[str, ModelConfig]:
        """Initialize available model configurations."""
        models = {}

        # OpenAI Models
        if os.getenv("OPENAI_API_KEY"):
            models.update(
                {
                    "gpt-4": ModelConfig(
                        name="gpt-4",
                        provider="openai",
                        tier=ModelTier.PREMIUM,
                        max_tokens=8192,
                        cost_per_token=0.03,
                        rate_limit_rpm=3500,
                        capabilities=["reasoning", "analysis", "planning", "synthesis"],
                    ),
                    "gpt-4o": ModelConfig(
                        name="gpt-4o",
                        provider="openai",
                        tier=ModelTier.STANDARD,
                        max_tokens=4096,
                        cost_per_token=0.005,
                        rate_limit_rpm=5000,
                        capabilities=["reasoning", "analysis", "drafting", "editing"],
                    ),
                    "gpt-3.5-turbo": ModelConfig(
                        name="gpt-3.5-turbo",
                        provider="openai",
                        tier=ModelTier.EFFICIENT,
                        max_tokens=4096,
                        cost_per_token=0.001,
                        rate_limit_rpm=10000,
                        capabilities=["drafting", "editing", "validation"],
                    ),
                }
            )

        # Anthropic Models
        if os.getenv("ANTHROPIC_API_KEY"):
            models.update(
                {
                    "claude-3-opus": ModelConfig(
                        name="claude-3-opus-20240229",
                        provider="anthropic",
                        tier=ModelTier.PREMIUM,
                        max_tokens=4096,
                        cost_per_token=0.015,
                        rate_limit_rpm=1000,
                        capabilities=["reasoning", "analysis", "planning", "synthesis"],
                    ),
                    "claude-3.5-sonnet": ModelConfig(
                        name="claude-sonnet-4-20250514",
                        provider="anthropic",
                        tier=ModelTier.STANDARD,
                        max_tokens=8192,
                        cost_per_token=0.003,
                        rate_limit_rpm=2000,
                        capabilities=["reasoning", "analysis", "drafting", "editing"],
                    ),
                    "claude-3-haiku": ModelConfig(
                        name="claude-3-haiku-20240307",
                        provider="anthropic",
                        tier=ModelTier.EFFICIENT,
                        max_tokens=4096,
                        cost_per_token=0.00025,
                        rate_limit_rpm=5000,
                        capabilities=["drafting", "editing", "validation"],
                    ),
                }
            )

        return models

    def _initialize_task_preferences(self) -> dict[TaskType, list[str]]:
        """Initialize task-to-model preferences."""
        return {
            TaskType.PLANNING: ["gpt-4", "claude-3-opus", "claude-3.5-sonnet", "gpt-4o"],
            TaskType.DRAFTING: ["gpt-4o", "claude-3.5-sonnet", "gpt-4", "claude-3-haiku"],
            TaskType.VALIDATION: ["gpt-3.5-turbo", "claude-3-haiku", "gpt-4o"],
            TaskType.SYNTHESIS: ["gpt-4", "claude-3-opus", "claude-3.5-sonnet"],
            TaskType.ANALYSIS: ["gpt-4", "claude-3-opus", "claude-3.5-sonnet", "gpt-4o"],
            TaskType.EDITING: ["gpt-4o", "claude-3.5-sonnet", "gpt-3.5-turbo"],
            TaskType.REVIEW: ["gpt-4", "claude-3.5-sonnet", "gpt-4o"],
        }

    def _initialize_fallback_chains(self) -> dict[str, list[str]]:
        """Initialize fallback chains for each model."""
        return {
            "gpt-4": ["gpt-4o", "claude-3.5-sonnet", "gpt-3.5-turbo"],
            "gpt-4o": ["gpt-4", "claude-3.5-sonnet", "gpt-3.5-turbo"],
            "gpt-3.5-turbo": ["gpt-4o", "claude-3-haiku"],
            "claude-3-opus": ["claude-3.5-sonnet", "gpt-4", "gpt-4o"],
            "claude-3.5-sonnet": ["gpt-4o", "claude-3-opus", "gpt-4"],
            "claude-3-haiku": ["gpt-3.5-turbo", "claude-3.5-sonnet"],
        }

    def select_model(
        self,
        task_type: TaskType,
        context_length: int | None = None,
        cost_priority: bool = False,
        capabilities: list[str] | None = None,
    ) -> str | None:
        """
        Select the best available model for a task.

        Args:
            task_type: Type of task to perform
            context_length: Required context length (tokens)
            cost_priority: Prioritize cost over capability
            capabilities: Required model capabilities

        Returns:
            Model name or None if no suitable model available
        """
        # Get preferred models for this task type
        preferred_models = self.task_preferences.get(task_type, [])

        # Filter by availability
        available_models = [m for m in preferred_models if m in self.models]

        if not available_models:
            self.logger.warning(f"No available models for task type: {task_type}")
            return None

        # Filter by capabilities if specified
        if capabilities:
            available_models = [
                m for m in available_models if all(cap in self.models[m].capabilities for cap in capabilities)
            ]

        # Filter by context length if specified
        if context_length:
            available_models = [m for m in available_models if self.models[m].max_tokens >= context_length]

        # Sort by cost if cost_priority is True
        if cost_priority:
            available_models.sort(key=lambda m: self.models[m].cost_per_token)

        # Check rate limits and select first available
        for model_name in available_models:
            if self._can_use_model(model_name):
                self.logger.debug(f"🎯 Selected model {model_name} for task {task_type}")
                return model_name

        self.logger.warning(f"All preferred models are rate limited for task {task_type}")
        return None

    def _can_use_model(self, model_name: str) -> bool:
        """Check if a model can be used (not rate limited)."""
        if model_name not in self.models:
            return False

        model_config = self.models[model_name]
        rate_state = self.rate_limits.get(model_name, RateLimitState())

        current_time = time.time()

        # Check if we're in a backoff period
        if current_time < rate_state.backoff_until:
            return False

        # Reset window if needed (1 minute windows)
        if current_time - rate_state.window_start > 60:
            rate_state.requests_made = 0
            rate_state.window_start = current_time

        # Check if we're under rate limit
        rpm_limit = model_config.rate_limit_rpm
        return rate_state.requests_made < rpm_limit

    def _record_usage(self, model_name: str):
        """Record usage of a model for rate limiting."""
        if model_name not in self.rate_limits:
            self.rate_limits[model_name] = RateLimitState()

        rate_state = self.rate_limits[model_name]
        current_time = time.time()

        rate_state.requests_made += 1
        rate_state.last_request = current_time

        # If we hit the limit, set a backoff period
        model_config = self.models[model_name]
        if rate_state.requests_made >= model_config.rate_limit_rpm:
            # Backoff for remainder of the minute plus buffer
            rate_state.backoff_until = rate_state.window_start + 70  # 60s + 10s buffer
            self.logger.warning(f"Rate limit reached for {model_name}, backing off until {rate_state.backoff_until}")

    def get_model_with_fallback(
        self, task_type: TaskType, preferred_model: str | None = None, **kwargs
    ) -> BaseChatModel | None:
        """
        Get a model instance with fallback strategy.

        Args:
            task_type: Type of task to perform
            preferred_model: Preferred model name
            **kwargs: Additional arguments for model selection

        Returns:
            Model instance or None if no model available
        """
        # Try preferred model first
        if preferred_model and self._can_use_model(preferred_model):
            try:
                model_config = self.models[preferred_model]
                instance = model_config.create_instance()
                self._record_usage(preferred_model)
                return instance
            except Exception as e:
                self.logger.warning(f"Failed to create preferred model {preferred_model}: {e}")

        # Fall back to task-appropriate selection
        selected_model = self.select_model(task_type, **kwargs)
        if not selected_model:
            return None

        try:
            model_config = self.models[selected_model]
            instance = model_config.create_instance()
            self._record_usage(selected_model)
            return instance
        except Exception as e:
            self.logger.error(f"Failed to create model {selected_model}: {e}")

            # Try fallback chain
            fallback_chain = self.fallback_chains.get(selected_model, [])
            for fallback_model in fallback_chain:
                if fallback_model in self.models and self._can_use_model(fallback_model):
                    try:
                        fallback_config = self.models[fallback_model]
                        instance = fallback_config.create_instance()
                        self._record_usage(fallback_model)
                        self.logger.info(f"🔄 Using fallback model {fallback_model}")
                        return instance
                    except Exception as fallback_error:
                        self.logger.warning(f"Fallback model {fallback_model} also failed: {fallback_error}")
                        continue

        self.logger.error("No available models after trying all fallbacks")
        return None

    def get_available_models(self) -> list[str]:
        """Get list of currently available models."""
        return [name for name in self.models.keys() if self._can_use_model(name)]

    def get_model_info(self, model_name: str) -> dict[str, Any] | None:
        """Get information about a specific model."""
        if model_name not in self.models:
            return None

        config = self.models[model_name]
        rate_state = self.rate_limits.get(model_name, RateLimitState())

        return {
            "name": config.name,
            "provider": config.provider,
            "tier": config.tier.value,
            "max_tokens": config.max_tokens,
            "cost_per_token": config.cost_per_token,
            "capabilities": config.capabilities,
            "available": self._can_use_model(model_name),
            "requests_made": rate_state.requests_made,
            "backoff_until": rate_state.backoff_until if rate_state.backoff_until > time.time() else None,
        }

    def get_system_stats(self) -> dict[str, Any]:
        """Get overall system statistics."""
        total_requests = sum(state.requests_made for state in self.rate_limits.values())
        available_models = len(self.get_available_models())

        return {
            "total_models": len(self.models),
            "available_models": available_models,
            "total_requests": total_requests,
            "rate_limited_models": len(
                [name for name, state in self.rate_limits.items() if state.backoff_until > time.time()]
            ),
        }


# Global model selector instance
_model_selector: ModelSelector | None = None


def get_model_selector() -> ModelSelector:
    """Get the global model selector instance."""
    global _model_selector
    if _model_selector is None:
        _model_selector = ModelSelector()
    return _model_selector


def select_model_for_task(task_type: TaskType, **kwargs) -> BaseChatModel | None:
    """
    Convenience function to select a model for a specific task.

    Args:
        task_type: Type of task to perform
        **kwargs: Additional arguments for model selection

    Returns:
        Model instance or None if no model available
    """
    selector = get_model_selector()
    model_name = selector.select_model(task_type, **kwargs)

    if not model_name:
        return None

    try:
        model_config = selector.models[model_name]
        instance = model_config.create_instance()
        selector._record_usage(model_name)
        return instance
    except Exception as e:
        selector.logger.error(f"Failed to create model {model_name}: {e}")
        return None
