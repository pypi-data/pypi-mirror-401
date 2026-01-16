"""
Advanced Observability - Metrics and Dashboards

Provides detailed metrics collection and dashboard integration for
the CCE agent's stakeholder generation process.

Enhanced with Phase 6 observability features including:
- Semantic retrieval metrics
- Dynamic model selection tracking
- MCP integration monitoring
- AIDER tooling performance
"""

import json
import logging
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from typing import Any

try:
    from langsmith import Client

    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

# Import Phase 6 components for enhanced observability
try:
    from src.semantic.embeddings import SimilarityResult

    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False

try:
    from models import ModelTier, TaskType

    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False


@dataclass
class SemanticRetrievalMetrics:
    """Metrics for semantic memory retrieval operations."""

    query_count: int = 0
    total_query_time: float = 0.0
    average_similarity_scores: list[float] = None
    retrieval_success_rate: float = 0.0
    embedding_cache_hits: int = 0
    embedding_cache_misses: int = 0

    def __post_init__(self):
        if self.average_similarity_scores is None:
            self.average_similarity_scores = []


@dataclass
class ModelSelectionMetrics:
    """Metrics for dynamic model selection and usage."""

    model_selections: dict[str, int] = None  # model_name -> selection count
    task_type_selections: dict[str, int] = None  # task_type -> selection count
    fallback_usage: dict[str, int] = None  # model_name -> fallback count
    rate_limit_hits: dict[str, int] = None  # model_name -> rate limit count
    selection_latency: list[float] = None  # selection decision times
    cost_tracking: dict[str, float] = None  # model_name -> estimated cost

    def __post_init__(self):
        if self.model_selections is None:
            self.model_selections = {}
        if self.task_type_selections is None:
            self.task_type_selections = {}
        if self.fallback_usage is None:
            self.fallback_usage = {}
        if self.rate_limit_hits is None:
            self.rate_limit_hits = {}
        if self.selection_latency is None:
            self.selection_latency = []
        if self.cost_tracking is None:
            self.cost_tracking = {}


@dataclass
class AIDERToolingMetrics:
    """Metrics for AIDER tooling performance."""

    edit_operations: int = 0
    successful_edits: int = 0
    failed_edits: int = 0
    validation_runs: int = 0
    validation_successes: int = 0
    tree_sitter_queries: int = 0
    repomap_generations: int = 0
    average_edit_time: float = 0.0

    @property
    def edit_success_rate(self) -> float:
        """Calculate edit success rate."""
        if self.edit_operations == 0:
            return 0.0
        return self.successful_edits / self.edit_operations

    @property
    def validation_success_rate(self) -> float:
        """Calculate validation success rate."""
        if self.validation_runs == 0:
            return 0.0
        return self.validation_successes / self.validation_runs


@dataclass
class SessionMetrics:
    """Metrics for a complete stakeholder session"""

    session_id: str
    start_time: float
    end_time: float | None
    duration: float | None

    # Stakeholder metrics
    stakeholders_count: int
    stakeholders_completed: int
    stakeholder_contributions: dict[str, int]  # stakeholder -> contribution count
    stakeholder_durations: dict[str, float]  # stakeholder -> analysis duration

    # Message metrics
    total_messages: int
    message_types: dict[str, int]  # message type -> count
    message_lengths: dict[str, list[int]]  # message type -> list of lengths

    # Quality metrics
    synthesis_quality_score: float | None
    implementation_readiness: float | None
    ticket_coverage: float | None
    stakeholder_balance: float | None

    # Performance metrics
    llm_calls: int
    total_tokens_used: int | None
    average_response_time: float | None

    # Outcome metrics (moved before optional fields to fix dataclass ordering)
    final_status: str  # "completed", "failed", "timeout", "cancelled"
    output_generated: bool

    # Phase 6 enhanced metrics
    semantic_metrics: SemanticRetrievalMetrics | None = None
    model_selection_metrics: ModelSelectionMetrics | None = None
    aider_metrics: AIDERToolingMetrics | None = None
    output_size: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StakeholderMetrics:
    """Metrics for individual stakeholder performance"""

    stakeholder_type: str
    session_id: str

    # Analysis metrics
    analysis_start_time: float
    analysis_end_time: float | None
    analysis_duration: float | None
    analysis_success: bool

    # Content metrics
    contribution_count: int
    total_contribution_length: int
    average_contribution_length: float

    # Quality metrics
    domain_coverage_score: float | None
    technical_depth_score: float | None

    # Performance metrics
    llm_calls: int
    tokens_used: int | None
    errors_encountered: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MetricsCollector:
    """
    Collects and aggregates metrics for the CCE stakeholder generation process.

    Provides detailed insights into performance, quality, and usage patterns
    with optional LangSmith integration for dashboards.
    """

    def __init__(self, langsmith_client: Any | None = None, enable_detailed_tracking: bool = True):
        self.logger = logging.getLogger(__name__)

        # LangSmith integration - auto-initialize if not provided
        if langsmith_client is None and LANGSMITH_AVAILABLE:
            try:
                self.langsmith_client = Client()
            except Exception as e:
                self.logger.warning(f"Failed to initialize LangSmith client: {e}")
                self.langsmith_client = None
        else:
            self.langsmith_client = langsmith_client

        self.langsmith_available = LANGSMITH_AVAILABLE and self.langsmith_client is not None

        # Configuration
        self.enable_detailed_tracking = enable_detailed_tracking

        # In-memory metrics storage
        self.session_metrics: dict[str, SessionMetrics] = {}
        self.stakeholder_metrics: dict[str, list[StakeholderMetrics]] = defaultdict(list)

        # Performance tracking
        self.operation_timings: dict[str, list[float]] = defaultdict(list)
        self.error_counts: dict[str, int] = Counter()

        self.logger.info(f"MetricsCollector initialized (LangSmith: {self.langsmith_available})")

    def start_session(self, session_id: str, stakeholders: list[str]) -> None:
        """Start tracking a new session"""

        self.session_metrics[session_id] = SessionMetrics(
            session_id=session_id,
            start_time=time.time(),
            end_time=None,
            duration=None,
            stakeholders_count=len(stakeholders),
            stakeholders_completed=0,
            stakeholder_contributions={},
            stakeholder_durations={},
            total_messages=0,
            message_types={},
            message_lengths={},
            synthesis_quality_score=None,
            implementation_readiness=None,
            ticket_coverage=None,
            stakeholder_balance=None,
            llm_calls=0,
            total_tokens_used=None,
            average_response_time=None,
            final_status="running",
            output_generated=False,
            output_size=None,
        )

        self.logger.info(f"Started session tracking: {session_id}")

    def end_session(self, session_id: str, final_status: str = "completed") -> None:
        """End session tracking"""

        if session_id not in self.session_metrics:
            self.logger.warning(f"Session {session_id} not found for ending")
            return

        session = self.session_metrics[session_id]
        session.end_time = time.time()
        session.duration = session.end_time - session.start_time
        session.final_status = final_status

        self.logger.info(f"Ended session tracking: {session_id} ({final_status}, {session.duration:.2f}s)")

        # Send to LangSmith if available
        if self.langsmith_available:
            self._send_session_to_langsmith(session)

    def record_stakeholder_start(self, session_id: str, stakeholder_type: str) -> None:
        """Record stakeholder analysis start"""

        stakeholder_metric = StakeholderMetrics(
            stakeholder_type=stakeholder_type,
            session_id=session_id,
            analysis_start_time=time.time(),
            analysis_end_time=None,
            analysis_duration=None,
            analysis_success=False,
            contribution_count=0,
            total_contribution_length=0,
            average_contribution_length=0.0,
            domain_coverage_score=None,
            technical_depth_score=None,
            llm_calls=0,
            tokens_used=None,
            errors_encountered=0,
        )

        self.stakeholder_metrics[session_id].append(stakeholder_metric)

        self.logger.debug(f"Started stakeholder tracking: {stakeholder_type} in {session_id}")

    def record_stakeholder_completion(
        self, session_id: str, stakeholder_type: str, contribution: str, success: bool = True
    ) -> None:
        """Record stakeholder analysis completion"""

        # Find the stakeholder metric
        stakeholder_metric = None
        for metric in self.stakeholder_metrics[session_id]:
            if metric.stakeholder_type == stakeholder_type and metric.analysis_end_time is None:
                stakeholder_metric = metric
                break

        if not stakeholder_metric:
            self.logger.warning(f"Stakeholder metric not found: {stakeholder_type} in {session_id}")
            return

        # Update stakeholder metrics
        stakeholder_metric.analysis_end_time = time.time()
        stakeholder_metric.analysis_duration = (
            stakeholder_metric.analysis_end_time - stakeholder_metric.analysis_start_time
        )
        stakeholder_metric.analysis_success = success
        stakeholder_metric.contribution_count = 1
        stakeholder_metric.total_contribution_length = len(contribution)
        stakeholder_metric.average_contribution_length = len(contribution)

        # Update session metrics
        if session_id in self.session_metrics:
            session = self.session_metrics[session_id]
            session.stakeholders_completed += 1
            session.stakeholder_contributions[stakeholder_type] = 1
            session.stakeholder_durations[stakeholder_type] = stakeholder_metric.analysis_duration

        self.logger.debug(f"Completed stakeholder tracking: {stakeholder_type} in {session_id}")

    def record_message(self, session_id: str, message_type: str, message_length: int) -> None:
        """Record a message in the session"""

        if session_id not in self.session_metrics:
            return

        session = self.session_metrics[session_id]
        session.total_messages += 1

        if message_type not in session.message_types:
            session.message_types[message_type] = 0
        session.message_types[message_type] += 1

        if message_type not in session.message_lengths:
            session.message_lengths[message_type] = []
        session.message_lengths[message_type].append(message_length)

    def record_quality_scores(
        self,
        session_id: str,
        synthesis_quality: float | None = None,
        implementation_readiness: float | None = None,
        ticket_coverage: float | None = None,
        stakeholder_balance: float | None = None,
    ) -> None:
        """Record quality assessment scores"""

        if session_id not in self.session_metrics:
            return

        session = self.session_metrics[session_id]

        if synthesis_quality is not None:
            session.synthesis_quality_score = synthesis_quality
        if implementation_readiness is not None:
            session.implementation_readiness = implementation_readiness
        if ticket_coverage is not None:
            session.ticket_coverage = ticket_coverage
        if stakeholder_balance is not None:
            session.stakeholder_balance = stakeholder_balance

        self.logger.debug(f"Updated quality scores for session {session_id}")

    def record_llm_call(
        self, session_id: str, tokens_used: int | None = None, response_time: float | None = None
    ) -> None:
        """Record an LLM call"""

        if session_id not in self.session_metrics:
            return

        session = self.session_metrics[session_id]
        session.llm_calls += 1

        if tokens_used is not None:
            if session.total_tokens_used is None:
                session.total_tokens_used = 0
            session.total_tokens_used += tokens_used

        if response_time is not None:
            # Update running average
            if session.average_response_time is None:
                session.average_response_time = response_time
            else:
                # Simple running average
                total_time = session.average_response_time * (session.llm_calls - 1) + response_time
                session.average_response_time = total_time / session.llm_calls

    def record_output(self, session_id: str, output_size: int) -> None:
        """Record final output generation"""

        if session_id not in self.session_metrics:
            return

        session = self.session_metrics[session_id]
        session.output_generated = True
        session.output_size = output_size

    def record_operation_timing(self, operation: str, duration: float) -> None:
        """Record timing for a specific operation"""
        self.operation_timings[operation].append(duration)

    def record_error(self, error_type: str) -> None:
        """Record an error occurrence"""
        self.error_counts[error_type] += 1

    def get_session_summary(self, session_id: str) -> dict[str, Any] | None:
        """Get summary metrics for a session"""

        if session_id not in self.session_metrics:
            return None

        session = self.session_metrics[session_id]
        stakeholder_metrics = self.stakeholder_metrics.get(session_id, [])

        summary = {
            "session_overview": session.to_dict(),
            "stakeholder_details": [metric.to_dict() for metric in stakeholder_metrics],
            "performance_summary": {
                "total_duration": session.duration,
                "average_stakeholder_duration": (
                    sum(session.stakeholder_durations.values()) / len(session.stakeholder_durations)
                    if session.stakeholder_durations
                    else 0
                ),
                "llm_calls": session.llm_calls,
                "tokens_per_call": (
                    session.total_tokens_used / session.llm_calls
                    if session.total_tokens_used and session.llm_calls > 0
                    else None
                ),
                "average_response_time": session.average_response_time,
            },
            "quality_summary": {
                "synthesis_quality": session.synthesis_quality_score,
                "implementation_readiness": session.implementation_readiness,
                "ticket_coverage": session.ticket_coverage,
                "stakeholder_balance": session.stakeholder_balance,
                "overall_quality": self._calculate_overall_quality(session),
            },
        }

        return summary

    def get_aggregate_metrics(self) -> dict[str, Any]:
        """Get aggregate metrics across all sessions"""

        if not self.session_metrics:
            return {"error": "No sessions recorded"}

        sessions = list(self.session_metrics.values())
        completed_sessions = [s for s in sessions if s.final_status == "completed"]

        aggregate = {
            "total_sessions": len(sessions),
            "completed_sessions": len(completed_sessions),
            "success_rate": len(completed_sessions) / len(sessions) if sessions else 0,
            "duration_stats": self._calculate_duration_stats(completed_sessions),
            "quality_stats": self._calculate_quality_stats(completed_sessions),
            "performance_stats": self._calculate_performance_stats(completed_sessions),
            "stakeholder_stats": self._calculate_stakeholder_stats(),
            "error_summary": dict(self.error_counts),
            "operation_timings": {
                op: {
                    "count": len(times),
                    "average": sum(times) / len(times) if times else 0,
                    "min": min(times) if times else 0,
                    "max": max(times) if times else 0,
                }
                for op, times in self.operation_timings.items()
            },
        }

        return aggregate

    def _calculate_overall_quality(self, session: SessionMetrics) -> float | None:
        """Calculate overall quality score for a session"""

        scores = [
            session.synthesis_quality_score,
            session.implementation_readiness,
            session.ticket_coverage,
            session.stakeholder_balance,
        ]

        valid_scores = [s for s in scores if s is not None]

        if not valid_scores:
            return None

        return sum(valid_scores) / len(valid_scores)

    def _calculate_duration_stats(self, sessions: list[SessionMetrics]) -> dict[str, float]:
        """Calculate duration statistics"""

        durations = [s.duration for s in sessions if s.duration is not None]

        if not durations:
            return {}

        return {
            "average": sum(durations) / len(durations),
            "min": min(durations),
            "max": max(durations),
            "median": sorted(durations)[len(durations) // 2],
        }

    def _calculate_quality_stats(self, sessions: list[SessionMetrics]) -> dict[str, Any]:
        """Calculate quality statistics"""

        quality_metrics = {
            "synthesis_quality": [s.synthesis_quality_score for s in sessions if s.synthesis_quality_score is not None],
            "implementation_readiness": [
                s.implementation_readiness for s in sessions if s.implementation_readiness is not None
            ],
            "ticket_coverage": [s.ticket_coverage for s in sessions if s.ticket_coverage is not None],
            "stakeholder_balance": [s.stakeholder_balance for s in sessions if s.stakeholder_balance is not None],
        }

        stats = {}
        for metric_name, values in quality_metrics.items():
            if values:
                stats[metric_name] = {
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                }
            else:
                stats[metric_name] = {"count": 0}

        return stats

    def _calculate_performance_stats(self, sessions: list[SessionMetrics]) -> dict[str, Any]:
        """Calculate performance statistics"""

        llm_calls = [s.llm_calls for s in sessions]
        token_usage = [s.total_tokens_used for s in sessions if s.total_tokens_used is not None]
        response_times = [s.average_response_time for s in sessions if s.average_response_time is not None]

        return {
            "llm_calls": {
                "total": sum(llm_calls),
                "average_per_session": sum(llm_calls) / len(llm_calls) if llm_calls else 0,
            },
            "token_usage": {
                "total": sum(token_usage) if token_usage else 0,
                "average_per_session": sum(token_usage) / len(token_usage) if token_usage else 0,
            },
            "response_times": {
                "average": sum(response_times) / len(response_times) if response_times else 0,
                "min": min(response_times) if response_times else 0,
                "max": max(response_times) if response_times else 0,
            },
        }

    def _calculate_stakeholder_stats(self) -> dict[str, Any]:
        """Calculate stakeholder-specific statistics"""

        all_stakeholder_metrics = []
        for session_metrics in self.stakeholder_metrics.values():
            all_stakeholder_metrics.extend(session_metrics)

        if not all_stakeholder_metrics:
            return {}

        # Group by stakeholder type
        by_type = defaultdict(list)
        for metric in all_stakeholder_metrics:
            by_type[metric.stakeholder_type].append(metric)

        stats = {}
        for stakeholder_type, metrics in by_type.items():
            durations = [m.analysis_duration for m in metrics if m.analysis_duration is not None]
            success_rate = sum(1 for m in metrics if m.analysis_success) / len(metrics)

            stats[stakeholder_type] = {
                "total_analyses": len(metrics),
                "success_rate": success_rate,
                "average_duration": sum(durations) / len(durations) if durations else 0,
                "average_contribution_length": sum(m.average_contribution_length for m in metrics) / len(metrics),
            }

        return stats

    def _send_session_to_langsmith(self, session: SessionMetrics) -> None:
        """Send session metrics to LangSmith"""

        if not self.langsmith_available:
            return

        try:
            # Create feedback scores for LangSmith
            feedback_scores = {}
            if session.synthesis_quality_score is not None:
                feedback_scores["synthesis_quality"] = session.synthesis_quality_score
            if session.implementation_readiness is not None:
                feedback_scores["implementation_readiness"] = session.implementation_readiness
            if session.ticket_coverage is not None:
                feedback_scores["ticket_coverage"] = session.ticket_coverage
            if session.stakeholder_balance is not None:
                feedback_scores["stakeholder_balance"] = session.stakeholder_balance

            # Send session data as a run to LangSmith
            self.langsmith_client.create_run(
                name=f"stakeholder_session_{session.session_id}",
                run_type="chain",
                inputs={"session_id": session.session_id},
                outputs={
                    "final_status": session.final_status,
                    "stakeholders_completed": session.stakeholders_completed,
                    "quality_scores": feedback_scores,
                },
                tags=["cce_stakeholder_session", f"status_{session.final_status}"],
                extra={
                    "duration": session.duration,
                    "llm_calls": session.llm_calls,
                    "total_tokens": session.total_tokens_used,
                    "stakeholder_count": session.stakeholders_count,
                    "message_count": session.total_messages,
                },
            )

            self.logger.info(f"Sent session {session.session_id} to LangSmith")

        except Exception as e:
            self.logger.error(f"Failed to send session to LangSmith: {e}")

    # Phase 6 Enhanced Tracking Methods

    def track_semantic_retrieval(
        self, session_id: str, query: str, results: list[Any], query_time: float, similarity_scores: list[float]
    ):
        """Track semantic memory retrieval operation."""
        if session_id not in self.session_metrics:
            return

        session = self.session_metrics[session_id]
        if session.semantic_metrics is None:
            session.semantic_metrics = SemanticRetrievalMetrics()

        metrics = session.semantic_metrics
        metrics.query_count += 1
        metrics.total_query_time += query_time
        metrics.average_similarity_scores.extend(similarity_scores)

        # Calculate success rate (results with similarity > threshold)
        successful_results = sum(1 for score in similarity_scores if score > 0.7)
        metrics.retrieval_success_rate = successful_results / len(similarity_scores) if similarity_scores else 0.0

        self.logger.debug(f"📊 Tracked semantic retrieval: {len(results)} results in {query_time:.3f}s")

    def track_model_selection(
        self,
        session_id: str,
        task_type: str,
        selected_model: str,
        fallback_used: bool = False,
        selection_time: float = 0.0,
        estimated_cost: float = 0.0,
    ):
        """Track dynamic model selection decision."""
        if session_id not in self.session_metrics:
            return

        session = self.session_metrics[session_id]
        if session.model_selection_metrics is None:
            session.model_selection_metrics = ModelSelectionMetrics()

        metrics = session.model_selection_metrics
        metrics.model_selections[selected_model] = metrics.model_selections.get(selected_model, 0) + 1
        metrics.task_type_selections[task_type] = metrics.task_type_selections.get(task_type, 0) + 1

        if fallback_used:
            metrics.fallback_usage[selected_model] = metrics.fallback_usage.get(selected_model, 0) + 1

        if selection_time > 0:
            metrics.selection_latency.append(selection_time)

        if estimated_cost > 0:
            metrics.cost_tracking[selected_model] = metrics.cost_tracking.get(selected_model, 0.0) + estimated_cost

        self.logger.debug(f"📊 Tracked model selection: {selected_model} for {task_type}")

    def track_rate_limit_hit(self, session_id: str, model_name: str):
        """Track when a model hits rate limits."""
        if session_id not in self.session_metrics:
            return

        session = self.session_metrics[session_id]
        if session.model_selection_metrics is None:
            session.model_selection_metrics = ModelSelectionMetrics()

        metrics = session.model_selection_metrics
        metrics.rate_limit_hits[model_name] = metrics.rate_limit_hits.get(model_name, 0) + 1

        self.logger.debug(f"📊 Tracked rate limit hit: {model_name}")

    def track_aider_operation(self, session_id: str, operation_type: str, success: bool, duration: float = 0.0):
        """Track AIDER tooling operations."""
        if session_id not in self.session_metrics:
            return

        session = self.session_metrics[session_id]
        if session.aider_metrics is None:
            session.aider_metrics = AIDERToolingMetrics()

        metrics = session.aider_metrics

        if operation_type == "edit":
            metrics.edit_operations += 1
            if success:
                metrics.successful_edits += 1
            else:
                metrics.failed_edits += 1

            if duration > 0:
                # Update running average
                total_time = metrics.average_edit_time * (metrics.edit_operations - 1) + duration
                metrics.average_edit_time = total_time / metrics.edit_operations

        elif operation_type == "validation":
            metrics.validation_runs += 1
            if success:
                metrics.validation_successes += 1

        elif operation_type == "tree_sitter":
            metrics.tree_sitter_queries += 1

        elif operation_type == "repomap":
            metrics.repomap_generations += 1

        self.logger.debug(f"📊 Tracked AIDER operation: {operation_type} ({'success' if success else 'failure'})")

    def get_phase6_summary(self, session_id: str) -> dict[str, Any]:
        """Get Phase 6 enhanced metrics summary for a session."""
        if session_id not in self.session_metrics:
            return {}

        session = self.session_metrics[session_id]
        summary = {}

        # Semantic retrieval summary
        if session.semantic_metrics:
            sem = session.semantic_metrics
            avg_query_time = sem.total_query_time / sem.query_count if sem.query_count > 0 else 0.0
            avg_similarity = (
                sum(sem.average_similarity_scores) / len(sem.average_similarity_scores)
                if sem.average_similarity_scores
                else 0.0
            )

            summary["semantic_retrieval"] = {
                "query_count": sem.query_count,
                "average_query_time": avg_query_time,
                "average_similarity": avg_similarity,
                "success_rate": sem.retrieval_success_rate,
                "cache_hit_rate": sem.embedding_cache_hits / (sem.embedding_cache_hits + sem.embedding_cache_misses)
                if (sem.embedding_cache_hits + sem.embedding_cache_misses) > 0
                else 0.0,
            }

        # Model selection summary
        if session.model_selection_metrics:
            mod = session.model_selection_metrics
            total_selections = sum(mod.model_selections.values())
            avg_latency = sum(mod.selection_latency) / len(mod.selection_latency) if mod.selection_latency else 0.0
            total_cost = sum(mod.cost_tracking.values())

            summary["model_selection"] = {
                "total_selections": total_selections,
                "unique_models_used": len(mod.model_selections),
                "fallback_rate": sum(mod.fallback_usage.values()) / total_selections if total_selections > 0 else 0.0,
                "average_selection_latency": avg_latency,
                "estimated_total_cost": total_cost,
                "rate_limit_incidents": sum(mod.rate_limit_hits.values()),
            }

        # AIDER tooling summary
        if session.aider_metrics:
            aid = session.aider_metrics
            summary["aider_tooling"] = {
                "edit_success_rate": aid.edit_success_rate,
                "validation_success_rate": aid.validation_success_rate,
                "total_operations": aid.edit_operations
                + aid.validation_runs
                + aid.tree_sitter_queries
                + aid.repomap_generations,
                "average_edit_time": aid.average_edit_time,
            }

        return summary

    def export_metrics(self, format: str = "json") -> str | dict[str, Any]:
        """Export all metrics in specified format"""

        data = {
            "export_timestamp": time.time(),
            "sessions": {sid: session.to_dict() for sid, session in self.session_metrics.items()},
            "stakeholder_metrics": {
                sid: [metric.to_dict() for metric in metrics] for sid, metrics in self.stakeholder_metrics.items()
            },
            "aggregate_metrics": self.get_aggregate_metrics(),
        }

        if format.lower() == "json":
            return json.dumps(data, indent=2)
        else:
            return data
