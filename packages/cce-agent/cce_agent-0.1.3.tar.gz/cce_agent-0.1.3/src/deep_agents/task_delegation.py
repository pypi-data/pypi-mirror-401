"""
Task Delegation Patterns for CCE Deep Agent.

This module implements task delegation patterns to replace command orchestration
with more flexible sub-agent delegation, enabling specialized workflows while
preserving deterministic execution guarantees.
"""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from .stakeholder_agents import STAKEHOLDER_AGENTS_BY_NAME


class TaskType(Enum):
    """Types of tasks that can be delegated to sub-agents."""

    RESEARCH = "research"
    ANALYSIS = "analysis"
    IMPLEMENTATION = "implementation"
    VALIDATION = "validation"
    OPTIMIZATION = "optimization"


class TaskStatus(Enum):
    """Status of delegated tasks."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """A task to be delegated to a sub-agent."""

    id: str
    task_type: TaskType
    description: str
    subagent_name: str
    context: dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict[str, Any] | None = None
    error_message: str | None = None
    metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(UTC)
        if self.metadata is None:
            self.metadata = {}


class TaskDelegator:
    """
    Manages task delegation to specialized sub-agents.

    Replaces command orchestration with flexible task delegation patterns
    while preserving deterministic execution guarantees.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_tasks: dict[str, Task] = {}
        self.completed_tasks: list[Task] = []
        self.task_counter = 0

        self.logger.info("🎯 TaskDelegator initialized")

    def delegate_research(self, query: str, subagent_type: str, context: dict[str, Any] | None = None) -> Task:
        """
        Delegate research tasks to specialized sub-agents.

        Args:
            query: Research query or topic
            subagent_type: Type of sub-agent to delegate to
            context: Additional context for the research task

        Returns:
            Task object representing the delegated research
        """
        return self._create_task(
            task_type=TaskType.RESEARCH,
            description=f"Research: {query}",
            subagent_name=subagent_type,
            context=context or {},
        )

    def delegate_analysis(self, context: str, subagent_type: str, analysis_type: str = "general") -> Task:
        """
        Delegate analysis tasks with context sharing.

        Args:
            context: Context to analyze
            subagent_type: Type of sub-agent to delegate to
            analysis_type: Type of analysis to perform

        Returns:
            Task object representing the delegated analysis
        """
        return self._create_task(
            task_type=TaskType.ANALYSIS,
            description=f"Analysis ({analysis_type}): {context[:100]}...",
            subagent_name=subagent_type,
            context={"context": context, "analysis_type": analysis_type},
        )

    def delegate_implementation(
        self, specification: str, subagent_type: str, target_files: list[str] | None = None
    ) -> Task:
        """
        Delegate implementation tasks to specialized sub-agents.

        Args:
            specification: Implementation specification
            subagent_type: Type of sub-agent to delegate to
            target_files: Files to be modified (if any)

        Returns:
            Task object representing the delegated implementation
        """
        return self._create_task(
            task_type=TaskType.IMPLEMENTATION,
            description=f"Implementation: {specification[:100]}...",
            subagent_name=subagent_type,
            context={"specification": specification, "target_files": target_files or []},
        )

    def delegate_validation(self, validation_target: str, subagent_type: str, validation_type: str = "quality") -> Task:
        """
        Delegate validation tasks to specialized sub-agents.

        Args:
            validation_target: What to validate
            subagent_type: Type of sub-agent to delegate to
            validation_type: Type of validation to perform

        Returns:
            Task object representing the delegated validation
        """
        return self._create_task(
            task_type=TaskType.VALIDATION,
            description=f"Validation ({validation_type}): {validation_target[:100]}...",
            subagent_name=subagent_type,
            context={"validation_target": validation_target, "validation_type": validation_type},
        )

    def delegate_optimization(
        self, optimization_target: str, subagent_type: str, optimization_type: str = "performance"
    ) -> Task:
        """
        Delegate optimization tasks to specialized sub-agents.

        Args:
            optimization_target: What to optimize
            subagent_type: Type of sub-agent to delegate to
            optimization_type: Type of optimization to perform

        Returns:
            Task object representing the delegated optimization
        """
        return self._create_task(
            task_type=TaskType.OPTIMIZATION,
            description=f"Optimization ({optimization_type}): {optimization_target[:100]}...",
            subagent_name=subagent_type,
            context={"optimization_target": optimization_target, "optimization_type": optimization_type},
        )

    def _create_task(self, task_type: TaskType, description: str, subagent_name: str, context: dict[str, Any]) -> Task:
        """
        Create a new task for delegation.

        Args:
            task_type: Type of task
            description: Task description
            subagent_name: Name of sub-agent to delegate to
            context: Task context

        Returns:
            Created task object
        """
        # Validate sub-agent exists
        if subagent_name not in STAKEHOLDER_AGENTS_BY_NAME:
            raise ValueError(f"Unknown sub-agent: {subagent_name}")

        # Generate unique task ID
        self.task_counter += 1
        task_id = f"task_{self.task_counter}_{task_type.value}_{subagent_name}"

        # Create task
        task = Task(
            id=task_id, task_type=task_type, description=description, subagent_name=subagent_name, context=context
        )

        # Store active task
        self.active_tasks[task_id] = task

        self.logger.info(f"📋 Created task {task_id}: {description}")

        return task

    def start_task(self, task_id: str) -> Task:
        """
        Mark a task as started.

        Args:
            task_id: ID of task to start

        Returns:
            Updated task object
        """
        if task_id not in self.active_tasks:
            raise ValueError(f"Task not found: {task_id}")

        task = self.active_tasks[task_id]
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now(UTC)

        self.logger.info(f"▶️ Started task {task_id}")

        return task

    def complete_task(self, task_id: str, result: dict[str, Any]) -> Task:
        """
        Mark a task as completed with results.

        Args:
            task_id: ID of task to complete
            result: Task results

        Returns:
            Updated task object
        """
        if task_id not in self.active_tasks:
            raise ValueError(f"Task not found: {task_id}")

        task = self.active_tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now(UTC)
        task.result = result

        # Move to completed tasks
        self.completed_tasks.append(task)
        del self.active_tasks[task_id]

        self.logger.info(f"✅ Completed task {task_id}")

        return task

    def fail_task(self, task_id: str, error_message: str) -> Task:
        """
        Mark a task as failed with error message.

        Args:
            task_id: ID of task to fail
            error_message: Error message

        Returns:
            Updated task object
        """
        if task_id not in self.active_tasks:
            raise ValueError(f"Task not found: {task_id}")

        task = self.active_tasks[task_id]
        task.status = TaskStatus.FAILED
        task.completed_at = datetime.now(UTC)
        task.error_message = error_message

        # Move to completed tasks
        self.completed_tasks.append(task)
        del self.active_tasks[task_id]

        self.logger.error(f"❌ Failed task {task_id}: {error_message}")

        return task

    def get_task_status(self, task_id: str) -> TaskStatus | None:
        """
        Get the status of a task.

        Args:
            task_id: ID of task to check

        Returns:
            Task status or None if not found
        """
        if task_id in self.active_tasks:
            return self.active_tasks[task_id].status

        # Check completed tasks
        for task in self.completed_tasks:
            if task.id == task_id:
                return task.status

        return None

    def get_active_tasks(self) -> list[Task]:
        """Get all active tasks."""
        return list(self.active_tasks.values())

    def get_completed_tasks(self) -> list[Task]:
        """Get all completed tasks."""
        return self.completed_tasks.copy()

    def get_tasks_by_subagent(self, subagent_name: str) -> list[Task]:
        """
        Get all tasks (active and completed) for a specific sub-agent.

        Args:
            subagent_name: Name of sub-agent

        Returns:
            List of tasks for the sub-agent
        """
        tasks = []

        # Check active tasks
        for task in self.active_tasks.values():
            if task.subagent_name == subagent_name:
                tasks.append(task)

        # Check completed tasks
        for task in self.completed_tasks:
            if task.subagent_name == subagent_name:
                tasks.append(task)

        return tasks

    def get_task_statistics(self) -> dict[str, Any]:
        """
        Get statistics about task delegation.

        Returns:
            Dictionary with task statistics
        """
        total_tasks = len(self.active_tasks) + len(self.completed_tasks)

        # Count by status
        status_counts = {}
        for task in self.active_tasks.values():
            status_counts[task.status.value] = status_counts.get(task.status.value, 0) + 1

        for task in self.completed_tasks:
            status_counts[task.status.value] = status_counts.get(task.status.value, 0) + 1

        # Count by sub-agent
        subagent_counts = {}
        for task in self.active_tasks.values():
            subagent_counts[task.subagent_name] = subagent_counts.get(task.subagent_name, 0) + 1

        for task in self.completed_tasks:
            subagent_counts[task.subagent_name] = subagent_counts.get(task.subagent_name, 0) + 1

        return {
            "total_tasks": total_tasks,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "status_counts": status_counts,
            "subagent_counts": subagent_counts,
        }
