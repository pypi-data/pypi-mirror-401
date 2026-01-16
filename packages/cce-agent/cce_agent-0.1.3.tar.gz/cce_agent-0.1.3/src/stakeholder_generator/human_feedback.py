"""
Human-in-the-Loop Integration

Uses LangGraph's native interrupt functionality for human feedback collection
in the multi-stakeholder architecture description generator.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.types import interrupt


class FeedbackAction(Enum):
    """Available human feedback actions"""

    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    RETRY = "retry"


@dataclass
class HumanFeedback:
    """Human feedback structure for LangGraph interrupts"""

    action: FeedbackAction
    comments: str | None = None
    modifications: dict[str, Any] | None = None


def should_interrupt_for_quality(quality_score: float | None = None) -> bool:
    """
    Determine if human intervention is needed based on quality scores.

    This follows LangGraph best practices for conditional interrupts.

    Args:
        quality_score: Current quality assessment (0.0-1.0)

    Returns:
        True if human review is needed
    """
    if quality_score is None:
        return True  # Review if no quality score

    # Quality-based interrupt thresholds
    if quality_score < 0.6:
        return True  # Low quality - require review
    elif quality_score < 0.8:
        return True  # Medium quality - human review recommended
    else:
        return False  # High quality - auto-approve


def create_human_review_interrupt(
    reason: str, current_state: dict[str, Any], review_data: dict[str, Any]
) -> dict[str, Any]:
    """
    Create a LangGraph interrupt for human review using the native interrupt() function.

    This uses LangGraph's proper interrupt pattern instead of custom implementation.

    Args:
        reason: Reason for the interrupt
        current_state: Current graph state
        review_data: Data for human review

    Returns:
        Updated state after interrupt
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Creating human review interrupt: {reason}")

    # Create interrupt message for human review
    interrupt_message = f"""
🛑 Human Review Required

**Reason**: {reason}

**Current Phase**: {current_state.get("current_phase", "Unknown")}

**Quality Score**: {current_state.get("quality_score", "Not assessed")}

**Stakeholders Completed**: {len(current_state.get("completed_stakeholders", []))}

**Review Data**: 
{_format_review_data(review_data)}

Please review and provide feedback:
- Type 'approve' to continue
- Type 'reject' to retry current phase  
- Type 'modify' with changes to update state
"""

    # Use LangGraph's native interrupt function
    feedback = interrupt(
        {
            "type": "human_review",
            "reason": reason,
            "message": interrupt_message,
            "current_state": current_state,
            "review_data": review_data,
        }
    )

    # Process the human feedback
    if isinstance(feedback, str):
        if feedback.lower() == "approve":
            action = FeedbackAction.APPROVE
        elif feedback.lower() == "reject":
            action = FeedbackAction.REJECT
        else:
            action = FeedbackAction.MODIFY

        human_feedback = HumanFeedback(action=action, comments=feedback)
    elif isinstance(feedback, dict):
        human_feedback = HumanFeedback(
            action=FeedbackAction(feedback.get("action", "approve")),
            comments=feedback.get("comments"),
            modifications=feedback.get("modifications"),
        )
    else:
        # Default to approve if no clear feedback
        human_feedback = HumanFeedback(action=FeedbackAction.APPROVE)

    logger.info(f"Human feedback received: {human_feedback.action.value}")

    # Update state based on feedback
    updated_state = current_state.copy()

    if human_feedback.action == FeedbackAction.APPROVE:
        updated_state["human_approval"] = True
        updated_state["should_continue"] = True
    elif human_feedback.action == FeedbackAction.REJECT:
        updated_state["human_approval"] = False
        updated_state["should_continue"] = False
        updated_state["retry_reason"] = human_feedback.comments
    elif human_feedback.action == FeedbackAction.MODIFY:
        updated_state["human_approval"] = True
        updated_state["should_continue"] = True
        if human_feedback.modifications:
            updated_state.update(human_feedback.modifications)

    # Add human feedback to messages
    feedback_message = HumanMessage(
        content=f"Human feedback: {human_feedback.action.value}. {human_feedback.comments or ''}",
        additional_kwargs={"feedback_action": human_feedback.action.value, "feedback_reason": reason},
    )

    updated_state["messages"] = updated_state.get("messages", []) + [feedback_message]

    return updated_state


def _format_review_data(review_data: dict[str, Any]) -> str:
    """Format review data for human display"""
    if not review_data:
        return "No specific data to review"

    formatted = []
    for key, value in review_data.items():
        if isinstance(value, dict) or isinstance(value, list):
            formatted.append(f"**{key.replace('_', ' ').title()}**: {len(value)} items")
        else:
            formatted.append(f"**{key.replace('_', ' ').title()}**: {value}")

    return "\n".join(formatted)


# Convenience functions for common interrupt scenarios
def create_quality_review_interrupt(state: dict[str, Any]) -> dict[str, Any]:
    """Create interrupt for quality review"""
    return create_human_review_interrupt(
        reason="Quality review required",
        current_state=state,
        review_data={
            "quality_score": state.get("quality_score"),
            "synthesis_result": state.get("synthesis_result"),
            "stakeholder_contributions": state.get("stakeholder_contributions", {}),
        },
    )


def create_synthesis_review_interrupt(state: dict[str, Any]) -> dict[str, Any]:
    """Create interrupt for synthesis review"""
    return create_human_review_interrupt(
        reason="Synthesis review requested",
        current_state=state,
        review_data={
            "synthesis_result": state.get("synthesis_result"),
            "completed_stakeholders": state.get("completed_stakeholders", []),
        },
    )


def create_final_approval_interrupt(state: dict[str, Any]) -> dict[str, Any]:
    """Create interrupt for final approval"""
    return create_human_review_interrupt(
        reason="Final architecture description approval",
        current_state=state,
        review_data={
            "architecture_document_path": state.get("architecture_document_path"),
            "quality_score": state.get("quality_score"),
            "implementation_readiness": state.get("implementation_readiness"),
        },
    )
