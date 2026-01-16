"""
Workflow Tools

Tools for workflow management, task tracking, planning, and human interaction.
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from langchain_core.tools import tool

from .models import (
    PlanItem,
    SessionPlanResponse,
    SessionPlanResult,
)

logger = logging.getLogger(__name__)


@dataclass
class TaskStatus:
    """Task status tracking"""

    task_id: str
    status: str  # "completed", "not_completed", "in_progress"
    summary: str
    reasoning: str
    timestamp: datetime


@dataclass
class PlanUpdate:
    """Plan update tracking"""

    plan_id: str
    update_reasoning: str
    changes: list[str]
    timestamp: datetime


@dataclass
class HumanHelpRequest:
    """Human help request tracking"""

    request_id: str
    help_request: str
    status: str  # "pending", "resolved"
    response: str | None = None
    timestamp: datetime = None


class ScratchpadManager:
    """Simple in-memory scratchpad for state management"""

    def __init__(self):
        self._data: dict[str, Any] = {}

    def write(self, key: str, value: Any) -> None:
        """Write data to scratchpad"""
        self._data[key] = value

    def read(self, key: str) -> Any:
        """Read data from scratchpad"""
        return self._data.get(key)

    def clear(self) -> None:
        """Clear all scratchpad data"""
        self._data.clear()

    def get_all(self) -> dict[str, Any]:
        """Get all scratchpad data"""
        return self._data.copy()


# Global state managers (in production, these would be persistent)
_task_statuses: dict[str, TaskStatus] = {}
_plan_updates: dict[str, PlanUpdate] = {}
_human_help_requests: dict[str, HumanHelpRequest] = {}
_technical_notes: list[str] = []
_conversation_summaries: list[str] = []
_scratchpad: ScratchpadManager | None = None


def get_scratchpad() -> ScratchpadManager:
    """Get the scratchpad instance (lazy initialized)."""
    global _scratchpad
    if _scratchpad is None:
        _scratchpad = ScratchpadManager()
    return _scratchpad


@tool
async def scratchpad(action: str, key: str | None = None, value: str | None = None) -> dict[str, Any]:
    """
    Simple scratchpad for storing and retrieving temporary data.

    Args:
        action: Action to perform ("write", "read", "clear", "list")
        key: Key for the data (required for write/read)
        value: Value to store (required for write)

    Returns:
        Dictionary containing scratchpad operation results
    """
    try:
        if action == "write":
            if not key or value is None:
                return {"success": False, "result": "Write action requires both key and value", "status": "error"}
            get_scratchpad().write(key, value)
            return {
                "success": True,
                "result": f"Successfully wrote to scratchpad with key '{key}'",
                "status": "success",
            }

        elif action == "read":
            if not key:
                return {"success": False, "result": "Read action requires a key", "status": "error"}
            value = get_scratchpad().read(key)
            if value is None:
                return {"success": True, "result": f"No value found for key '{key}'", "status": "success"}
            return {"success": True, "result": f"Value for key '{key}': {value}", "status": "success"}

        elif action == "clear":
            get_scratchpad().clear()
            return {"success": True, "result": "Scratchpad cleared successfully", "status": "success"}

        elif action == "list":
            all_data = get_scratchpad().get_all()
            if not all_data:
                return {"success": True, "result": "Scratchpad is empty", "status": "success"}
            return {
                "success": True,
                "result": f"Scratchpad contents: {json.dumps(all_data, indent=2)}",
                "status": "success",
            }

        else:
            return {
                "success": False,
                "result": f"Unknown action: {action}. Valid actions: write, read, clear, list",
                "status": "error",
            }

    except Exception as e:
        return {"success": False, "result": f"Error in scratchpad operation: {str(e)}", "status": "error"}


@tool
async def request_human_help(help_request: str) -> dict[str, Any]:
    """
    Request help from a human when stuck or unable to continue.

    Args:
        help_request: The help request to send to the human. Should be concise but descriptive.
                     This should be a request which the user can help with, such as providing
                     context into where a function lives/is used within a codebase, or answering
                     questions about how to run scripts. The user does NOT have access to the
                     filesystem you're running on, and thus can not make changes to the code for you.

    Returns:
        Dictionary containing the help request status
    """
    try:
        request_id = f"help_{len(_human_help_requests) + 1}"

        help_request_obj = HumanHelpRequest(
            request_id=request_id, help_request=help_request, status="pending", timestamp=datetime.now()
        )

        _human_help_requests[request_id] = help_request_obj

        logger.info(f"Human help requested: {help_request[:100]}...")

        return {
            "success": True,
            "result": f"Help request submitted successfully. Request ID: {request_id}\n\n"
            f"Request: {help_request}\n\n"
            f"Status: Pending human response. Execution will pause until help is provided.",
            "status": "success",
            "request_id": request_id,
        }

    except Exception as e:
        return {"success": False, "result": f"Error submitting help request: {str(e)}", "status": "error"}


@tool
async def session_plan(title: str, plan_items: list[str], reasoning: str) -> SessionPlanResponse:
    """
    Create a session plan for the current work session.

    Args:
        title: The title of the plan. Should be a short, one sentence description
               of the user's request/plan generated to fulfill it.
        plan_items: List of plan items that need to be completed
        reasoning: Reasoning for why this plan was created

    Returns:
        Structured session plan results
    """
    try:
        plan_id = f"plan_{len(_plan_updates) + 1}"

        plan_update = PlanUpdate(
            plan_id=plan_id, update_reasoning=reasoning, changes=plan_items, timestamp=datetime.now()
        )

        _plan_updates[plan_id] = plan_update

        logger.info(f"Session plan created: {title}")

        # Create structured plan items
        structured_plan_items = [
            PlanItem(id=f"item_{i + 1}", description=item, status="pending", priority=1)
            for i, item in enumerate(plan_items)
        ]

        plan_result = SessionPlanResult(
            plan_id=plan_id,
            title=title,
            plan_items=structured_plan_items,
            reasoning=reasoning,
            created_at=datetime.now(),
        )

        return SessionPlanResponse(
            success=True,
            result=f"Session plan created successfully with {len(plan_items)} items",
            status="success",
            plan=plan_result,
            metadata={"plan_id": plan_id},
        )

    except Exception as e:
        return SessionPlanResponse(
            success=False,
            result=f"Error creating session plan: {str(e)}",
            status="error",
            error_code="PLAN_CREATION_ERROR",
            error_hint="Check plan items format and try again",
        )


@tool
async def update_plan(update_plan_reasoning: str, plan_changes: list[str]) -> dict[str, Any]:
    """
    Update the current plan with new information or changes.

    Args:
        update_plan_reasoning: The reasoning for why you are updating the plan.
                              This should include context which will be useful when
                              actually updating the plan, such as what plan items to
                              update, edit, or remove, along with any other context
                              that would be useful when updating the plan.
        plan_changes: List of specific changes to make to the plan

    Returns:
        Dictionary containing the plan update status
    """
    try:
        plan_id = f"update_{len(_plan_updates) + 1}"

        plan_update = PlanUpdate(
            plan_id=plan_id, update_reasoning=update_plan_reasoning, changes=plan_changes, timestamp=datetime.now()
        )

        _plan_updates[plan_id] = plan_update

        logger.info(f"Plan updated: {update_plan_reasoning[:100]}...")

        return {
            "success": True,
            "result": f"Plan updated successfully.\n\n"
            f"Reasoning: {update_plan_reasoning}\n\n"
            f"Changes:\n" + "\n".join(f"- {change}" for change in plan_changes),
            "status": "success",
            "plan_id": plan_id,
        }

    except Exception as e:
        return {"success": False, "result": f"Error updating plan: {str(e)}", "status": "error"}


@tool
async def mark_task_completed(completed_task_summary: str) -> dict[str, Any]:
    """
    Mark the current task as completed with a summary of actions taken.

    Args:
        completed_task_summary: A detailed summary of the actions you took to complete
                               the current task. This should include what was accomplished,
                               any files that were modified, and any important decisions made.

    Returns:
        Dictionary containing the task completion status
    """
    try:
        task_id = f"task_{len(_task_statuses) + 1}"

        task_status = TaskStatus(
            task_id=task_id,
            status="completed",
            summary=completed_task_summary,
            reasoning="Task completed successfully",
            timestamp=datetime.now(),
        )

        _task_statuses[task_id] = task_status

        logger.info(f"Task marked as completed: {task_id}")

        return {
            "success": True,
            "result": f"Task marked as completed successfully.\n\n"
            f"Task ID: {task_id}\n\n"
            f"Summary: {completed_task_summary}",
            "status": "success",
            "task_id": task_id,
        }

    except Exception as e:
        return {"success": False, "result": f"Error marking task as completed: {str(e)}", "status": "error"}


@tool
async def mark_task_not_completed(reasoning: str) -> dict[str, Any]:
    """
    Mark the current task as not completed with reasoning.

    Args:
        reasoning: A concise reasoning summary for the status of the current task,
                  explaining why you think it is not completed.

    Returns:
        Dictionary containing the task status
    """
    try:
        task_id = f"task_{len(_task_statuses) + 1}"

        task_status = TaskStatus(
            task_id=task_id,
            status="not_completed",
            summary="Task not completed",
            reasoning=reasoning,
            timestamp=datetime.now(),
        )

        _task_statuses[task_id] = task_status

        logger.info(f"Task marked as not completed: {task_id}")

        return {
            "success": True,
            "result": f"Task marked as not completed.\n\nTask ID: {task_id}\n\nReasoning: {reasoning}",
            "status": "success",
            "task_id": task_id,
        }

    except Exception as e:
        return {"success": False, "result": f"Error marking task as not completed: {str(e)}", "status": "error"}


@tool
async def diagnose_error(diagnosis: str) -> dict[str, Any]:
    """
    Diagnose an error that occurred during execution.

    Args:
        diagnosis: The diagnosis of the error, including what went wrong,
                  potential causes, and suggested solutions.

    Returns:
        Dictionary containing the error diagnosis
    """
    try:
        diagnosis_id = f"diagnosis_{len(_task_statuses) + 1}"

        logger.info(f"Error diagnosis provided: {diagnosis[:100]}...")

        return {
            "success": True,
            "result": f"Error diagnosis recorded successfully.\n\n"
            f"Diagnosis ID: {diagnosis_id}\n\n"
            f"Diagnosis: {diagnosis}",
            "status": "success",
            "diagnosis_id": diagnosis_id,
        }

    except Exception as e:
        return {"success": False, "result": f"Error recording diagnosis: {str(e)}", "status": "error"}


@tool
async def write_technical_notes(notes: str) -> dict[str, Any]:
    """
    Write technical notes based on the conversation history.

    Args:
        notes: The notes you've generated based on the conversation history.
               These should be technical in nature and useful for future reference.

    Returns:
        Dictionary containing the notes status
    """
    try:
        _technical_notes.append(notes)

        logger.info(f"Technical notes written: {len(_technical_notes)} total notes")

        return {
            "success": True,
            "result": f"Technical notes written successfully.\n\n"
            f"Notes: {notes}\n\n"
            f"Total notes: {len(_technical_notes)}",
            "status": "success",
        }

    except Exception as e:
        return {"success": False, "result": f"Error writing technical notes: {str(e)}", "status": "error"}


@tool
async def conversation_history_summary(reasoning: str) -> dict[str, Any]:
    """
    Generate a summary of the conversation history.

    Args:
        reasoning: The reasoning for why this summary is being generated
                  and what key points should be included.

    Returns:
        Dictionary containing the summary status
    """
    try:
        summary_id = f"summary_{len(_conversation_summaries) + 1}"

        summary = f"Summary {summary_id}: {reasoning}"
        _conversation_summaries.append(summary)

        logger.info(f"Conversation summary generated: {summary_id}")

        return {
            "success": True,
            "result": f"Conversation summary generated successfully.\n\n"
            f"Summary ID: {summary_id}\n\n"
            f"Reasoning: {reasoning}\n\n"
            f"Total summaries: {len(_conversation_summaries)}",
            "status": "success",
            "summary_id": summary_id,
        }

    except Exception as e:
        return {"success": False, "result": f"Error generating conversation summary: {str(e)}", "status": "error"}


__all__ = [
    "scratchpad",
    "request_human_help",
    "session_plan",
    "update_plan",
    "mark_task_completed",
    "mark_task_not_completed",
    "diagnose_error",
    "write_technical_notes",
    "conversation_history_summary",
]
