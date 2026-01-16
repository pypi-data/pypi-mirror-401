"""
Plan Validation System

This module provides validation capabilities for generated plans to ensure
they are coherent, complete, and actionable.
"""

import logging
from typing import Any

from .topic_analyzer import PlanTopicAnalysis

logger = logging.getLogger(__name__)


class PlanValidator:
    """Validates generated plans for coherence, completeness, and actionability."""

    def __init__(self):
        """Initialize the plan validator."""
        self.logger = logging.getLogger(f"{__name__}.PlanValidator")

    def validate_plan(
        self, plan_structure: dict[str, Any], topic_analysis: PlanTopicAnalysis | None = None
    ) -> dict[str, Any]:
        """Validate a plan structure and return validation results."""
        validation_results = {"valid": True, "errors": [], "warnings": [], "suggestions": []}

        # Validate basic structure
        self._validate_basic_structure(plan_structure, validation_results)

        # Validate phases
        self._validate_phases(plan_structure.get("phases", []), validation_results)

        # Validate dependencies
        self._validate_dependencies(plan_structure.get("dependencies", []), validation_results)

        # Validate risks
        self._validate_risks(plan_structure.get("risks", []), validation_results)

        # Validate against topic analysis if provided
        if topic_analysis:
            self._validate_against_topic_analysis(plan_structure, topic_analysis, validation_results)

        # Determine overall validity
        validation_results["valid"] = len(validation_results["errors"]) == 0

        return validation_results

    def _validate_basic_structure(self, plan_structure: dict[str, Any], validation_results: dict[str, Any]) -> None:
        """Validate basic plan structure."""
        required_keys = ["phases"]

        for key in required_keys:
            if key not in plan_structure:
                validation_results["errors"].append(f"Missing required key: {key}")

        # Check if phases is a list
        if "phases" in plan_structure and not isinstance(plan_structure["phases"], list):
            validation_results["errors"].append("Phases must be a list")

        # Check if phases list is empty
        if "phases" in plan_structure and len(plan_structure["phases"]) == 0:
            validation_results["errors"].append("Plan must have at least one phase")

    def _validate_phases(self, phases: list[dict[str, Any]], validation_results: dict[str, Any]) -> None:
        """Validate individual phases."""
        if not phases:
            return

        required_phase_keys = ["name", "description", "tasks", "deliverables", "acceptance_criteria"]

        for i, phase in enumerate(phases):
            phase_name = phase.get("name", f"Phase {i + 1}")

            # Check required keys
            for key in required_phase_keys:
                if key not in phase:
                    validation_results["errors"].append(f"Phase '{phase_name}' missing required key: {key}")

            # Validate tasks
            if "tasks" in phase:
                if not isinstance(phase["tasks"], list) or len(phase["tasks"]) == 0:
                    validation_results["warnings"].append(f"Phase '{phase_name}' has no tasks or tasks is not a list")

            # Validate deliverables
            if "deliverables" in phase:
                if not isinstance(phase["deliverables"], list) or len(phase["deliverables"]) == 0:
                    validation_results["warnings"].append(
                        f"Phase '{phase_name}' has no deliverables or deliverables is not a list"
                    )

            # Validate acceptance criteria
            if "acceptance_criteria" in phase:
                if not isinstance(phase["acceptance_criteria"], list) or len(phase["acceptance_criteria"]) == 0:
                    validation_results["warnings"].append(
                        f"Phase '{phase_name}' has no acceptance criteria or acceptance_criteria is not a list"
                    )

            # Check for reasonable phase names
            if "name" in phase:
                phase_name_lower = phase["name"].lower()
                if len(phase_name_lower) < 3:
                    validation_results["warnings"].append(f"Phase '{phase_name}' has a very short name")

                # Check for common phase patterns
                common_phases = ["analysis", "design", "implementation", "testing", "deployment", "validation"]
                if not any(pattern in phase_name_lower for pattern in common_phases):
                    validation_results["suggestions"].append(
                        f"Phase '{phase_name}' might benefit from a more descriptive name"
                    )

    def _validate_dependencies(self, dependencies: list[str], validation_results: dict[str, Any]) -> None:
        """Validate dependencies."""
        if not dependencies:
            validation_results["warnings"].append("No dependencies specified - consider adding relevant dependencies")
            return

        # Check for reasonable dependencies
        reasonable_dependencies = [
            "codebase analysis",
            "stakeholder review",
            "requirements",
            "design",
            "testing",
            "documentation",
            "security review",
            "performance testing",
            "user feedback",
        ]

        for dep in dependencies:
            dep_lower = dep.lower()
            if not any(reasonable in dep_lower for reasonable in reasonable_dependencies):
                validation_results["suggestions"].append(
                    f"Dependency '{dep}' might not be standard - consider if it's necessary"
                )

    def _validate_risks(self, risks: list[str], validation_results: dict[str, Any]) -> None:
        """Validate risks."""
        if not risks:
            validation_results["warnings"].append("No risks specified - consider adding relevant risk factors")
            return

        # Check for reasonable risks
        reasonable_risks = [
            "technical complexity",
            "integration challenges",
            "timeline pressure",
            "resource constraints",
            "scope creep",
            "system stability",
            "data integrity",
            "security vulnerabilities",
            "performance regression",
            "user experience impact",
            "breaking changes",
        ]

        for risk in risks:
            risk_lower = risk.lower()
            if not any(reasonable in risk_lower for reasonable in reasonable_risks):
                validation_results["suggestions"].append(
                    f"Risk '{risk}' might not be standard - consider if it's relevant"
                )

    def _validate_against_topic_analysis(
        self, plan_structure: dict[str, Any], topic_analysis: PlanTopicAnalysis, validation_results: dict[str, Any]
    ) -> None:
        """Validate plan against topic analysis."""
        phases = plan_structure.get("phases", [])

        # Check if number of phases matches complexity
        if topic_analysis.complexity_level == "simple" and len(phases) > 3:
            validation_results["warnings"].append("Plan has many phases for a simple task - consider simplifying")
        elif topic_analysis.complexity_level == "complex" and len(phases) < 3:
            validation_results["warnings"].append(
                "Plan has few phases for a complex task - consider adding more detail"
            )

        # Check if phases match domain type
        domain_phase_mapping = {
            "feature": ["analysis", "design", "implementation", "testing"],
            "bugfix": ["investigation", "fix", "validation"],
            "refactor": ["analysis", "refactoring", "validation"],
            "infrastructure": ["planning", "implementation", "deployment"],
            "performance": ["profiling", "optimization", "validation"],
        }

        expected_phases = domain_phase_mapping.get(topic_analysis.domain_type, [])
        phase_names = [phase.get("name", "").lower() for phase in phases]

        for expected_phase in expected_phases:
            if not any(expected_phase in phase_name for phase_name in phase_names):
                validation_results["suggestions"].append(
                    f"Consider adding a phase related to '{expected_phase}' for {topic_analysis.domain_type} tasks"
                )

        # Check if architectural scope is addressed
        if topic_analysis.architectural_scope:
            scope_phases = []
            for phase in phases:
                phase_desc = phase.get("description", "").lower()
                for scope in topic_analysis.architectural_scope:
                    if scope.lower() in phase_desc:
                        scope_phases.append(scope)

            missing_scopes = set(topic_analysis.architectural_scope) - set(scope_phases)
            if missing_scopes:
                validation_results["suggestions"].append(
                    f"Consider addressing these architectural scopes: {', '.join(missing_scopes)}"
                )

    def get_validation_summary(self, validation_results: dict[str, Any]) -> str:
        """Get a human-readable validation summary."""
        if validation_results["valid"]:
            summary = "✅ Plan validation passed"
        else:
            summary = "❌ Plan validation failed"

        if validation_results["errors"]:
            summary += f"\n\nErrors ({len(validation_results['errors'])}):"
            for error in validation_results["errors"]:
                summary += f"\n  • {error}"

        if validation_results["warnings"]:
            summary += f"\n\nWarnings ({len(validation_results['warnings'])}):"
            for warning in validation_results["warnings"]:
                summary += f"\n  • {warning}"

        if validation_results["suggestions"]:
            summary += f"\n\nSuggestions ({len(validation_results['suggestions'])}):"
            for suggestion in validation_results["suggestions"]:
                summary += f"\n  • {suggestion}"

        return summary
