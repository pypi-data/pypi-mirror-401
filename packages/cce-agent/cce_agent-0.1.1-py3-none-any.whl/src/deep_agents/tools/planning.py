"""
Planning Tool Integration for CCE Deep Agent

This module implements TodoWrite-inspired planning tools for task management
and context preservation, based on LangChain Deep Agents patterns.
"""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class PlanStatus(Enum):
    """Status of a plan step."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PlanStep(BaseModel):
    """Individual step in a plan."""

    id: str
    description: str
    status: PlanStatus = PlanStatus.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: float | None = None
    completed_at: float | None = None
    result: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class Plan(BaseModel):
    """Complete plan with multiple steps."""

    id: str
    title: str
    description: str
    steps: list[PlanStep] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    status: PlanStatus = PlanStatus.PENDING
    metadata: dict[str, Any] = field(default_factory=dict)


class PlanManager:
    """Manages plans and their execution state."""

    def __init__(self):
        self.plans: dict[str, Plan] = {}
        self.active_plan: str | None = None

    def create_plan(self, title: str, description: str, steps: list[str]) -> Plan:
        """
        Create a new plan with the given title, description, and steps.

        Args:
            title: Plan title
            description: Plan description
            steps: List of step descriptions

        Returns:
            Created plan
        """
        plan_id = str(uuid.uuid4())
        plan_steps = [PlanStep(id=str(uuid.uuid4()), description=step, status=PlanStatus.PENDING) for step in steps]

        plan = Plan(id=plan_id, title=title, description=description, steps=plan_steps, status=PlanStatus.PENDING)

        self.plans[plan_id] = plan
        return plan

    def update_plan_step(
        self, plan_id: str, step_id: str, status: PlanStatus, result: str | None = None, error: str | None = None
    ) -> bool:
        """
        Update the status of a plan step.

        Args:
            plan_id: Plan ID
            step_id: Step ID
            status: New status
            result: Optional result text
            error: Optional error text

        Returns:
            True if step was updated, False if not found
        """
        if plan_id not in self.plans:
            return False

        plan = self.plans[plan_id]
        for step in plan.steps:
            if step.id == step_id:
                step.status = status
                step.result = result
                step.error = error

                if status == PlanStatus.IN_PROGRESS and not step.started_at:
                    step.started_at = time.time()
                elif status in [PlanStatus.COMPLETED, PlanStatus.FAILED, PlanStatus.CANCELLED]:
                    step.completed_at = time.time()

                plan.updated_at = time.time()
                self._update_plan_status(plan)
                return True

        return False

    def get_plan(self, plan_id: str) -> Plan | None:
        """Get a plan by ID."""
        return self.plans.get(plan_id)

    def get_active_plan(self) -> Plan | None:
        """Get the currently active plan."""
        if self.active_plan:
            return self.plans.get(self.active_plan)
        return None

    def set_active_plan(self, plan_id: str) -> bool:
        """
        Set the active plan.

        Args:
            plan_id: Plan ID to set as active

        Returns:
            True if plan was set as active, False if not found
        """
        if plan_id in self.plans:
            self.active_plan = plan_id
            return True
        return False

    def list_plans(self) -> list[Plan]:
        """List all plans."""
        return list(self.plans.values())

    def get_plan_progress(self, plan_id: str) -> dict[str, Any] | None:
        """
        Get progress information for a plan.

        Args:
            plan_id: Plan ID

        Returns:
            Progress information or None if plan not found
        """
        if plan_id not in self.plans:
            return None

        plan = self.plans[plan_id]
        total_steps = len(plan.steps)
        completed_steps = sum(1 for step in plan.steps if step.status == PlanStatus.COMPLETED)
        failed_steps = sum(1 for step in plan.steps if step.status == PlanStatus.FAILED)
        in_progress_steps = sum(1 for step in plan.steps if step.status == PlanStatus.IN_PROGRESS)

        return {
            "plan_id": plan_id,
            "title": plan.title,
            "status": plan.status.value,
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "failed_steps": failed_steps,
            "in_progress_steps": in_progress_steps,
            "progress_percentage": (completed_steps / total_steps * 100) if total_steps > 0 else 0,
            "created_at": plan.created_at,
            "updated_at": plan.updated_at,
        }

    def _update_plan_status(self, plan: Plan) -> None:
        """Update the overall plan status based on step statuses."""
        if not plan.steps:
            plan.status = PlanStatus.PENDING
            return

        step_statuses = [step.status for step in plan.steps]

        if all(status == PlanStatus.COMPLETED for status in step_statuses):
            plan.status = PlanStatus.COMPLETED
        elif any(status == PlanStatus.FAILED for status in step_statuses):
            plan.status = PlanStatus.FAILED
        elif any(status == PlanStatus.IN_PROGRESS for status in step_statuses):
            plan.status = PlanStatus.IN_PROGRESS
        else:
            plan.status = PlanStatus.PENDING


# Global plan manager instance (lazy initialization to avoid import side effects)
_plan_manager: PlanManager | None = None


def get_plan_manager() -> PlanManager:
    """Get the global plan manager instance (lazy initialized)."""
    global _plan_manager
    if _plan_manager is None:
        _plan_manager = PlanManager()
    return _plan_manager


# Pydantic schemas for planning tools
class CreatePlanInput(BaseModel):
    """Input schema for create_plan tool."""

    description: str = Field(..., description="Description of the overall task")
    steps: list[str] = Field(..., description="List of step descriptions")


class UpdatePlanInput(BaseModel):
    """Input schema for update_plan tool."""

    plan_id: str = Field(..., description="ID of the plan to update")
    step_id: str = Field(..., description="ID of the step to update")
    status: str = Field(..., description="New status for the step")
    result: str | None = Field(default=None, description="Result or notes for the step")


class GetPlanInput(BaseModel):
    """Input schema for get_plan tool."""

    plan_id: str = Field(..., description="ID of the plan to retrieve")


class ListPlansInput(BaseModel):
    """Input schema for list_plans tool."""

    status_filter: str | None = Field(default=None, description="Filter plans by status")


class SetActivePlanInput(BaseModel):
    """Input schema for set_active_plan tool."""

    plan_id: str = Field(..., description="ID of the plan to set as active")


class GetActivePlanInput(BaseModel):
    """Input schema for get_active_plan tool."""

    pass  # No parameters needed


@tool(
    args_schema=CreatePlanInput,
    description="Create a structured plan for complex tasks with step-by-step breakdown",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def create_plan(description: str, steps: list[str]) -> str:
    """
    Create a structured plan for complex tasks.

    Args:
        description: Description of the overall task
        steps: List of step descriptions

    Returns:
        Plan ID and summary
    """
    try:
        plan_manager = get_plan_manager()
        plan = plan_manager.create_plan(title=f"Plan: {description[:50]}...", description=description, steps=steps)

        plan_manager.set_active_plan(plan.id)

        return f"Created plan {plan.id} with {len(steps)} steps. Plan is now active."

    except Exception as e:
        return f"Failed to create plan: {str(e)}"


@tool(
    args_schema=UpdatePlanInput,
    description="Update the status of a plan step with type safety and comprehensive error handling",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def update_plan(plan_id: str, step_id: str, status: str, result: str | None = None) -> str:
    """
    Update the status of a plan step.

    Args:
        plan_id: Plan ID
        step_id: Step ID
        status: New status (pending, in_progress, completed, failed, cancelled)
        result: Optional result text

    Returns:
        Update confirmation
    """
    try:
        # Type safety check - ensure status is a string
        if not isinstance(status, str):
            return f"Error: status must be a string, got {type(status).__name__}: {status}"

        # Type safety check - ensure result is a string or None
        if result is not None and not isinstance(result, str):
            return f"Error: result must be a string or None, got {type(result).__name__}: {result}"

        status_enum = PlanStatus(status.lower())
        success = get_plan_manager().update_plan_step(plan_id, step_id, status_enum, result)

        if success:
            return f"Updated step {step_id} in plan {plan_id} to {status}"
        else:
            return f"Failed to update step {step_id} in plan {plan_id}"

    except ValueError:
        return f"Invalid status: {status}. Valid statuses: pending, in_progress, completed, failed, cancelled"
    except Exception as e:
        return f"Failed to update plan: {str(e)}"


@tool(
    args_schema=GetPlanInput,
    description="Get the current status and details of a specific plan",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def get_plan_status(plan_id: str) -> str:
    """
    Get the current status and progress of a plan.

    Args:
        plan_id: Plan ID

    Returns:
        Plan status and progress information
    """
    try:
        progress = get_plan_manager().get_plan_progress(plan_id)
        if progress:
            return (
                f"Plan {plan_id}: {progress['title']}\n"
                f"Status: {progress['status']}\n"
                f"Progress: {progress['completed_steps']}/{progress['total_steps']} steps "
                f"({progress['progress_percentage']:.1f}%)\n"
                f"Failed: {progress['failed_steps']}, In Progress: {progress['in_progress_steps']}"
            )
        else:
            return f"Plan {plan_id} not found"

    except Exception as e:
        return f"Failed to get plan status: {str(e)}"


@tool(
    args_schema=ListPlansInput,
    description="List all available plans with their current status and progress",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def list_plans() -> str:
    """
    List all available plans.

    Returns:
        List of all plans with their status
    """
    try:
        plans = get_plan_manager().list_plans()
        if not plans:
            return "No plans available"

        result = "Available Plans:\n"
        for plan in plans:
            progress = get_plan_manager().get_plan_progress(plan.id)
            if progress:
                result += f"- {plan.id}: {plan.title} ({progress['status']}, {progress['progress_percentage']:.1f}%)\n"

        return result

    except Exception as e:
        return f"Failed to list plans: {str(e)}"


@tool(
    args_schema=SetActivePlanInput,
    description="Set the active plan for execution with validation and error handling",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def set_active_plan(plan_id: str) -> str:
    """
    Set the active plan for current operations.

    Args:
        plan_id: Plan ID to set as active

    Returns:
        Confirmation of active plan
    """
    try:
        success = get_plan_manager().set_active_plan(plan_id)
        if success:
            return f"Set plan {plan_id} as active"
        else:
            return f"Plan {plan_id} not found"

    except Exception as e:
        return f"Failed to set active plan: {str(e)}"


@tool(
    args_schema=GetActivePlanInput,
    description="Get the currently active plan with detailed status information",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def get_active_plan() -> str:
    """
    Get the currently active plan.

    Returns:
        Active plan information or "No active plan"
    """
    try:
        active_plan = get_plan_manager().get_active_plan()
        if active_plan:
            progress = get_plan_manager().get_plan_progress(active_plan.id)
            if progress:
                return (
                    f"Active Plan: {active_plan.id}\n"
                    f"Title: {active_plan.title}\n"
                    f"Status: {progress['status']}\n"
                    f"Progress: {progress['completed_steps']}/{progress['total_steps']} steps"
                )
        return "No active plan"

    except Exception as e:
        return f"Failed to get active plan: {str(e)}"


# Planning tools list for easy import
PLANNING_TOOLS = [create_plan, update_plan, get_plan_status, list_plans, set_active_plan, get_active_plan]
