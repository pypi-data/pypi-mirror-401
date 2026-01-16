"""
Decision Tracking Utilities

Provides utilities for capturing and managing architecture decisions
throughout the stakeholder analysis process.
"""

import logging
from datetime import datetime
from typing import Any


class DecisionTracker:
    """
    Utility class for tracking architecture decisions during stakeholder analysis.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def capture_stakeholder_decision(
        self, stakeholder_type: str, decision: str, rationale: str, context: str, consequences: str | None = None
    ) -> dict[str, Any]:
        """
        Capture a decision made during stakeholder analysis.

        Args:
            stakeholder_type: Type of stakeholder making the decision
            decision: The decision that was made
            rationale: Reasoning behind the decision
            context: Context in which the decision was made
            consequences: Expected consequences of the decision

        Returns:
            Dictionary containing the captured decision
        """
        decision_record = {
            "id": f"decision_{int(datetime.utcnow().timestamp())}",
            "timestamp": datetime.utcnow().isoformat(),
            "stakeholder_type": stakeholder_type,
            "decision": decision,
            "rationale": rationale,
            "context": context,
            "consequences": consequences or "Consequences to be determined",
            "status": "proposed",
            "phase": "stakeholder_analysis",
        }

        self.logger.debug(f"Captured decision from {stakeholder_type}: {decision[:50]}...")
        return decision_record

    def capture_synthesis_decision(
        self,
        decision: str,
        rationale: str,
        context: str,
        stakeholder_inputs: list[str],
        consequences: str | None = None,
    ) -> dict[str, Any]:
        """
        Capture a decision made during synthesis.

        Args:
            decision: The decision that was made
            rationale: Reasoning behind the decision
            context: Context in which the decision was made
            stakeholder_inputs: List of stakeholder types that contributed to this decision
            consequences: Expected consequences of the decision

        Returns:
            Dictionary containing the captured decision
        """
        decision_record = {
            "id": f"decision_{int(datetime.utcnow().timestamp())}",
            "timestamp": datetime.utcnow().isoformat(),
            "stakeholder_type": "synthesis_engine",
            "decision": decision,
            "rationale": rationale,
            "context": context,
            "stakeholder_inputs": stakeholder_inputs,
            "consequences": consequences or "Consequences to be determined",
            "status": "accepted",
            "phase": "synthesis",
        }

        self.logger.debug(f"Captured synthesis decision: {decision[:50]}...")
        return decision_record

    def capture_quality_decision(
        self, decision: str, rationale: str, quality_scores: dict[str, float], consequences: str | None = None
    ) -> dict[str, Any]:
        """
        Capture a decision made during quality assessment.

        Args:
            decision: The decision that was made
            rationale: Reasoning behind the decision
            quality_scores: Quality scores that influenced the decision
            consequences: Expected consequences of the decision

        Returns:
            Dictionary containing the captured decision
        """
        decision_record = {
            "id": f"decision_{int(datetime.utcnow().timestamp())}",
            "timestamp": datetime.utcnow().isoformat(),
            "stakeholder_type": "quality_gates",
            "decision": decision,
            "rationale": rationale,
            "context": f"Quality assessment with scores: {quality_scores}",
            "quality_scores": quality_scores,
            "consequences": consequences or "Consequences to be determined",
            "status": "accepted",
            "phase": "quality_review",
        }

        self.logger.debug(f"Captured quality decision: {decision[:50]}...")
        return decision_record

    def update_decision_status(
        self, decision: dict[str, Any], new_status: str, reason: str | None = None
    ) -> dict[str, Any]:
        """
        Update the status of a decision.

        Args:
            decision: The decision record to update
            new_status: New status for the decision
            reason: Reason for the status change

        Returns:
            Updated decision record
        """
        decision["status"] = new_status
        decision["status_updated"] = datetime.utcnow().isoformat()
        if reason:
            decision["status_reason"] = reason

        self.logger.debug(f"Updated decision {decision['id']} status to {new_status}")
        return decision

    def get_decisions_by_phase(self, decisions: list[dict[str, Any]], phase: str) -> list[dict[str, Any]]:
        """
        Get all decisions from a specific phase.

        Args:
            decisions: List of all decisions
            phase: Phase to filter by

        Returns:
            List of decisions from the specified phase
        """
        return [d for d in decisions if d.get("phase") == phase]

    def get_decisions_by_stakeholder(
        self, decisions: list[dict[str, Any]], stakeholder_type: str
    ) -> list[dict[str, Any]]:
        """
        Get all decisions from a specific stakeholder type.

        Args:
            decisions: List of all decisions
            stakeholder_type: Stakeholder type to filter by

        Returns:
            List of decisions from the specified stakeholder
        """
        return [d for d in decisions if d.get("stakeholder_type") == stakeholder_type]

    def summarize_decisions(self, decisions: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Create a summary of all decisions.

        Args:
            decisions: List of all decisions

        Returns:
            Summary of decisions by phase and stakeholder
        """
        summary = {"total_decisions": len(decisions), "by_phase": {}, "by_stakeholder": {}, "by_status": {}}

        for decision in decisions:
            phase = decision.get("phase", "unknown")
            stakeholder = decision.get("stakeholder_type", "unknown")
            status = decision.get("status", "unknown")

            summary["by_phase"][phase] = summary["by_phase"].get(phase, 0) + 1
            summary["by_stakeholder"][stakeholder] = summary["by_stakeholder"].get(stakeholder, 0) + 1
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1

        return summary
