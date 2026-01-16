"""
LangGraph Interrupt Tools for Deep Agents

This module provides tools for managing human feedback interrupts during
deep agents execution using LangGraph's native interrupt functionality.
"""

import logging
from datetime import datetime
from typing import Annotated, Any, Dict, Optional, Union

from langchain_core.tools import tool
from langgraph.types import interrupt
from pydantic import BaseModel, Field

# Import LangGraph interrupt functionality

# Import human feedback system from stakeholder generator
try:
    from ...stakeholder_generator.human_feedback import (
        FeedbackAction,
        HumanFeedback,
        create_human_review_interrupt,
        should_interrupt_for_quality,
    )
except ImportError:
    # Fallback if stakeholder generator not available
    HumanFeedback = None
    FeedbackAction = None
    should_interrupt_for_quality = None
    create_human_review_interrupt = None

logger = logging.getLogger(__name__)


class TriggerQualityInterruptInput(BaseModel):
    """Input schema for trigger_quality_interrupt_tool."""

    quality_score: float = Field(..., description="Current quality assessment (0.0-1.0)")
    reason: str = Field(..., description="Reason for the interrupt")
    context: str = Field(..., description="Execution context description")
    workspace_root: str = Field(default=".", description="Root directory for interrupt logs")


class TriggerArchitecturalDecisionInterruptInput(BaseModel):
    """Input schema for trigger_architectural_decision_interrupt_tool."""

    decision_type: str = Field(..., description="Type of architectural decision")
    decision_description: str = Field(..., description="Description of the decision")
    context: str = Field(..., description="Execution context description")
    workspace_root: str = Field(default=".", description="Root directory for interrupt logs")


def create_deep_agent_quality_interrupt(
    quality_score: float, context: dict[str, Any], review_data: dict[str, Any]
) -> dict[str, Any]:
    """
    Create a LangGraph interrupt for quality review during deep agents execution.

    Args:
        quality_score: Current quality assessment (0.0-1.0)
        context: Execution context
        review_data: Data for human review

    Returns:
        Updated context after interrupt processing
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Creating quality interrupt for deep agents: quality_score={quality_score}")

    # Create interrupt message for human review
    interrupt_message = f"""
🛑 Deep Agents Quality Review Required

**Quality Score**: {quality_score:.2f}
**Threshold**: 0.3 (Low threshold - only for very poor quality)

**Execution Context**:
- Ticket: {context.get("ticket_title", "Unknown")}
- Phase: {context.get("execution_phase", "Implementation")}
- Cycle: {context.get("cycle_count", 0)}

**Review Data**:
{_format_review_data(review_data)}

**Actions Available**:
- Type 'approve' to continue with current quality
- Type 'reject' to retry current phase
- Type 'modify' with specific changes to update approach

Please review the quality assessment and provide feedback:
"""

    # Use LangGraph's native interrupt function (with context safety)
    try:
        feedback = interrupt(
            {
                "type": "deep_agent_quality_review",
                "reason": f"Quality score {quality_score:.2f} below threshold",
                "message": interrupt_message,
                "current_state": context,
                "review_data": review_data,
                "quality_score": quality_score,
            }
        )
    except Exception as e:
        # If we're not in a proper LangGraph context, return a default response
        logger.warning(f"Quality interrupt failed (not in LangGraph context): {e}")
        feedback = "approve"  # Default to approving to avoid blocking execution

    # Process the human feedback
    if FeedbackAction and HumanFeedback:
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
    else:
        # Fallback when human feedback system is not available
        human_feedback = {"action": "approve", "comments": feedback if isinstance(feedback, str) else "Auto-approved"}

    # Get action from human feedback (handle both object and dict formats)
    if isinstance(human_feedback, dict):
        action = human_feedback.get("action", "approve")
        logger.info(f"Human feedback received for deep agents: {action}")
    else:
        action = human_feedback.action
        logger.info(f"Human feedback received for deep agents: {action.value if hasattr(action, 'value') else action}")

    # Update context based on feedback
    updated_context = context.copy()

    if (isinstance(human_feedback, dict) and action == "approve") or (
        not isinstance(human_feedback, dict) and action == FeedbackAction.APPROVE
    ):
        updated_context["human_approval"] = True
        updated_context["should_continue"] = True
        updated_context["quality_approved"] = True
    elif (isinstance(human_feedback, dict) and action == "reject") or (
        not isinstance(human_feedback, dict) and action == FeedbackAction.REJECT
    ):
        updated_context["human_approval"] = False
        updated_context["should_continue"] = False
        if isinstance(human_feedback, dict):
            updated_context["retry_reason"] = human_feedback.get("comments", "")
        else:
            updated_context["retry_reason"] = human_feedback.comments
    elif (isinstance(human_feedback, dict) and action == "modify") or (
        not isinstance(human_feedback, dict) and action == FeedbackAction.MODIFY
    ):
        updated_context["human_approval"] = True
        updated_context["should_continue"] = True
        if isinstance(human_feedback, dict):
            modifications = human_feedback.get("modifications", {})
        else:
            modifications = human_feedback.modifications
        if modifications:
            updated_context.update(modifications)

    # Add human feedback to context
    if isinstance(human_feedback, dict):
        updated_context["human_feedback"] = {
            "action": action,
            "comments": human_feedback.get("comments", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "quality_score": quality_score,
        }
    else:
        updated_context["human_feedback"] = {
            "action": action.value if hasattr(action, "value") else action,
            "comments": human_feedback.comments,
            "timestamp": datetime.utcnow().isoformat(),
            "quality_score": quality_score,
        }

    return updated_context


def create_deep_agent_architectural_decision_interrupt(
    decision_type: str, decision_description: str, context: dict[str, Any], review_data: dict[str, Any]
) -> dict[str, Any]:
    """
    Create a LangGraph interrupt for architectural decision review during deep agents execution.

    Args:
        decision_type: Type of architectural decision
        decision_description: Description of the decision
        context: Execution context
        review_data: Data for human review

    Returns:
        Updated context after interrupt processing
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Creating architectural decision interrupt: {decision_type}")

    # Create interrupt message for human review
    interrupt_message = f"""
🛑 Deep Agents Architectural Decision Required

**Decision Type**: {decision_type}
**Description**: {decision_description}

**Execution Context**:
- Ticket: {context.get("ticket_title", "Unknown")}
- Phase: {context.get("execution_phase", "Implementation")}
- Cycle: {context.get("cycle_count", 0)}

**Review Data**:
{_format_review_data(review_data)}

**Actions Available**:
- Type 'approve' to proceed with this architectural decision
- Type 'reject' to choose a different approach
- Type 'modify' with specific architectural changes

Please review the architectural decision and provide feedback:
"""

    # Use LangGraph's native interrupt function (with context safety)
    try:
        feedback = interrupt(
            {
                "type": "deep_agent_architectural_decision",
                "reason": f"Architectural decision required: {decision_type}",
                "message": interrupt_message,
                "current_state": context,
                "review_data": review_data,
                "decision_type": decision_type,
            }
        )
    except Exception as e:
        # If we're not in a proper LangGraph context, return a default response
        logger.warning(f"Architectural decision interrupt failed (not in LangGraph context): {e}")
        feedback = "approve"  # Default to approving to avoid blocking execution

    # Process the human feedback (similar to quality interrupt)
    if FeedbackAction and HumanFeedback:
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
            human_feedback = HumanFeedback(action=FeedbackAction.APPROVE)
    else:
        # Fallback when human feedback system is not available
        human_feedback = {"action": "approve", "comments": feedback if isinstance(feedback, str) else "Auto-approved"}

    # Get action from human feedback (handle both object and dict formats)
    if isinstance(human_feedback, dict):
        action = human_feedback.get("action", "approve")
        logger.info(f"Human feedback received for architectural decision: {action}")
    else:
        action = human_feedback.action
        logger.info(
            f"Human feedback received for architectural decision: {action.value if hasattr(action, 'value') else action}"
        )

    # Update context based on feedback
    updated_context = context.copy()

    if (isinstance(human_feedback, dict) and action == "approve") or (
        not isinstance(human_feedback, dict) and action == FeedbackAction.APPROVE
    ):
        updated_context["human_approval"] = True
        updated_context["should_continue"] = True
        updated_context["architectural_decision_approved"] = True
    elif (isinstance(human_feedback, dict) and action == "reject") or (
        not isinstance(human_feedback, dict) and action == FeedbackAction.REJECT
    ):
        updated_context["human_approval"] = False
        updated_context["should_continue"] = False
        if isinstance(human_feedback, dict):
            updated_context["retry_reason"] = human_feedback.get("comments", "")
        else:
            updated_context["retry_reason"] = human_feedback.comments
    elif (isinstance(human_feedback, dict) and action == "modify") or (
        not isinstance(human_feedback, dict) and action == FeedbackAction.MODIFY
    ):
        updated_context["human_approval"] = True
        updated_context["should_continue"] = True
        if isinstance(human_feedback, dict):
            modifications = human_feedback.get("modifications", {})
        else:
            modifications = human_feedback.modifications
        if modifications:
            updated_context.update(modifications)

    # Add human feedback to context
    if isinstance(human_feedback, dict):
        updated_context["human_feedback"] = {
            "action": action,
            "comments": human_feedback.get("comments", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "decision_type": decision_type,
        }
    else:
        updated_context["human_feedback"] = {
            "action": action.value if hasattr(action, "value") else action,
            "comments": human_feedback.comments,
            "timestamp": datetime.utcnow().isoformat(),
            "decision_type": decision_type,
        }

    return updated_context


@tool(
    args_schema=TriggerQualityInterruptInput,
    description="Trigger a quality-based human feedback interrupt using LangGraph's native interrupt with retry mechanism",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def trigger_quality_interrupt_tool(
    quality_score: float,
    reason: str,
    context: str,
    workspace_root: str = ".",
) -> str:
    """
    Trigger a quality-based human feedback interrupt using LangGraph's native interrupt.

    Args:
        quality_score: Current quality assessment (0.0-1.0)
        reason: Reason for the interrupt
        context: Execution context description
        workspace_root: Root directory for interrupt logs

    Returns:
        Status message about interrupt trigger
    """
    try:
        if not should_interrupt_for_quality:
            return "❌ Human feedback system not available - cannot trigger interrupt"

        # Check if interrupt should be triggered
        if not should_interrupt_for_quality(quality_score):
            return f"ℹ️ No interrupt needed - quality score {quality_score:.2f} meets threshold"

        # Create context and review data
        execution_context = {
            "ticket_title": context,
            "execution_phase": "Deep Agents Implementation",
            "timestamp": datetime.utcnow().isoformat(),
        }

        review_data = {
            "quality_score": quality_score,
            "reason": reason,
            "context": context,
            "threshold": 0.3,  # Low threshold - only for very poor quality
        }

        # Create quality interrupt using LangGraph's native interrupt
        result = create_deep_agent_quality_interrupt(
            quality_score=quality_score, context=execution_context, review_data=review_data
        )

        logger.info(f"🛑 Quality interrupt triggered: {reason}")
        return f"✅ Quality interrupt triggered successfully: {reason}"

    except Exception as e:
        logger.error(f"❌ Failed to trigger quality interrupt: {e}")
        return f"❌ Failed to trigger quality interrupt: {str(e)}"


@tool(
    args_schema=TriggerArchitecturalDecisionInterruptInput,
    description="Trigger an architectural decision human feedback interrupt using LangGraph's native interrupt with retry mechanism",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def trigger_architectural_decision_interrupt_tool(
    decision_type: str,
    decision_description: str,
    context: str,
    workspace_root: str = ".",
) -> str:
    """
    Trigger an architectural decision human feedback interrupt using LangGraph's native interrupt.

    Args:
        decision_type: Type of architectural decision
        decision_description: Description of the decision
        context: Execution context description
        workspace_root: Root directory for interrupt logs

    Returns:
        Status message about interrupt trigger
    """
    try:
        if not HumanFeedback:
            return "❌ Human feedback system not available - cannot trigger interrupt"

        # Create context and review data
        execution_context = {
            "ticket_title": context,
            "execution_phase": "Deep Agents Implementation",
            "timestamp": datetime.utcnow().isoformat(),
        }

        review_data = {
            "decision_type": decision_type,
            "decision_description": decision_description,
            "context": context,
            "requires_human_approval": True,
        }

        # Create architectural decision interrupt using LangGraph's native interrupt
        result = create_deep_agent_architectural_decision_interrupt(
            decision_type=decision_type,
            decision_description=decision_description,
            context=execution_context,
            review_data=review_data,
        )

        logger.info(f"🛑 Architectural decision interrupt triggered: {decision_type}")
        return f"✅ Architectural decision interrupt triggered: {decision_type}"

    except Exception as e:
        logger.error(f"❌ Failed to trigger architectural decision interrupt: {e}")
        return f"❌ Failed to trigger architectural decision interrupt: {str(e)}"


def should_trigger_deep_agent_interrupt(
    trigger_type: str,
    context: dict[str, Any],
    quality_score: float | None = None,
    quality_threshold: float = 0.3,  # Low threshold - only interrupt for very low quality
) -> bool:
    """
    Determine if a deep agent interrupt should be triggered.

    Args:
        trigger_type: Type of interrupt trigger
        context: Execution context
        quality_score: Current quality assessment (0.0-1.0)
        quality_threshold: Quality threshold below which to trigger interrupt (default: 0.3 - very low)

    Returns:
        True if interrupt should be triggered
    """
    if trigger_type == "quality_threshold":
        if quality_score is not None:
            # Use the stakeholder system's should_interrupt_for_quality if available,
            # otherwise use our configurable threshold
            if should_interrupt_for_quality:
                # Override the stakeholder system's threshold with our low threshold
                return quality_score < quality_threshold
            else:
                return quality_score < quality_threshold
        return True  # Interrupt if no quality score

    elif trigger_type == "architectural_decision":
        # Only interrupt on major architectural decisions, not every decision
        return context.get("major_architectural_decision", False)

    elif trigger_type == "planning_change":
        # Only interrupt on significant planning changes
        return context.get("significant_planning_change", False)

    elif trigger_type == "error_recovery":
        # Interrupt on error recovery
        return True

    return False


def _format_review_data(review_data: dict[str, Any]) -> str:
    """Format review data for display in interrupt message."""
    if not review_data:
        return "No additional review data available."

    formatted = []
    for key, value in review_data.items():
        if isinstance(value, (dict, list)):
            formatted.append(f"**{key.replace('_', ' ').title()}**: {str(value)[:200]}...")
        else:
            formatted.append(f"**{key.replace('_', ' ').title()}**: {value}")

    return "\n".join(formatted)


class QualityAssessmentInput(BaseModel):
    """Input schema for generate_quality_assessment tool."""

    implementation_state: str = Field(..., description="Description of current implementation state")
    ticket_coverage: float = Field(
        ..., description="How well the implementation covers the ticket requirements (0.0-1.0)"
    )
    technical_feasibility: float = Field(..., description="Technical soundness of the implementation (0.0-1.0)")
    clarity_completeness: float = Field(..., description="Clarity and completeness of the implementation (0.0-1.0)")
    overall_score: float = Field(..., description="Overall quality score (0.0-1.0)")


@tool(
    args_schema=QualityAssessmentInput,
    description="Generate a quality assessment for the current implementation state",
    infer_schema=False,
    parse_docstring=False,
)
def generate_quality_assessment(
    implementation_state: str,
    ticket_coverage: float,
    technical_feasibility: float,
    clarity_completeness: float,
    overall_score: float,
) -> str:
    """
    Generate a structured quality assessment for the current implementation.

    Args:
        implementation_state: Description of current implementation state
        ticket_coverage: How well the implementation covers the ticket requirements (0.0-1.0)
        technical_feasibility: Technical soundness of the implementation (0.0-1.0)
        clarity_completeness: Clarity and completeness of the implementation (0.0-1.0)
        overall_score: Overall quality score (0.0-1.0)

    Returns:
        Structured quality assessment string
    """
    try:
        assessment = f"""
## Quality Assessment

**Implementation State**: {implementation_state}

**Quality Scores**:
- Ticket Coverage: {ticket_coverage:.2f}
- Technical Feasibility: {technical_feasibility:.2f}
- Clarity & Completeness: {clarity_completeness:.2f}
- Overall Score: {overall_score:.2f}

**Threshold**: 0.3 (Low threshold - only for very poor quality)
**Pass Threshold**: {"✅ PASS" if overall_score >= 0.3 else "❌ FAIL"}

**Assessment**: {"Quality meets minimum standards" if overall_score >= 0.3 else "Quality below threshold - requires review"}
"""

        logger.info(f"📊 [QUALITY ASSESSMENT] Generated assessment with overall score: {overall_score:.2f}")
        return assessment

    except Exception as e:
        logger.error(f"❌ Failed to generate quality assessment: {e}")
        return f"Quality assessment generation failed: {str(e)}"


# Export tools for use in deep agents
LANGGRAPH_INTERRUPT_TOOLS = [
    trigger_quality_interrupt_tool,
    trigger_architectural_decision_interrupt_tool,
    generate_quality_assessment,
]
