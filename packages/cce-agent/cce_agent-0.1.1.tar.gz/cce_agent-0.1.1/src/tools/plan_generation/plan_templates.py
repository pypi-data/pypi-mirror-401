"""
Plan Template Library

This module provides reusable plan templates for common development scenarios.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class PlanTemplateLibrary:
    """Library of proven plan templates for common development scenarios."""

    TEMPLATES = {
        "feature_development": {
            "phases": [
                {
                    "name": "Requirements Analysis",
                    "description": "Analyze and document feature requirements",
                    "tasks": ["Gather requirements", "Define acceptance criteria", "Identify stakeholders"],
                    "deliverables": ["Requirements document", "Acceptance criteria"],
                    "acceptance_criteria": ["Requirements validated", "Stakeholders aligned"],
                },
                {
                    "name": "Technical Design",
                    "description": "Design the technical implementation approach",
                    "tasks": ["Architecture design", "API design", "Database design", "Security review"],
                    "deliverables": ["Technical specification", "API documentation", "Database schema"],
                    "acceptance_criteria": ["Design approved", "Security reviewed"],
                },
                {
                    "name": "Implementation",
                    "description": "Implement the core functionality",
                    "tasks": ["Core development", "Unit testing", "Integration testing", "Code review"],
                    "deliverables": ["Working feature", "Test coverage", "Documentation"],
                    "acceptance_criteria": ["Feature complete", "Tests passing", "Code reviewed"],
                },
                {
                    "name": "Testing and Validation",
                    "description": "Comprehensive testing and validation",
                    "tasks": ["Integration testing", "User acceptance testing", "Performance testing"],
                    "deliverables": ["Test results", "Performance metrics", "User feedback"],
                    "acceptance_criteria": ["All tests passing", "Performance acceptable", "User approved"],
                },
            ],
            "stakeholders": ["PM", "architect", "developer", "QA"],
            "risk_factors": ["scope_creep", "integration_complexity", "user_expectations"],
            "success_criteria": [
                "All functionality implemented as specified",
                "Tests pass with adequate coverage",
                "Documentation updated and accurate",
                "User acceptance testing completed successfully",
            ],
        },
        "bug_fixing": {
            "phases": [
                {
                    "name": "Investigation",
                    "description": "Investigate and reproduce the bug",
                    "tasks": ["Bug reproduction", "Root cause analysis", "Impact assessment"],
                    "deliverables": ["Bug report", "Root cause analysis", "Impact assessment"],
                    "acceptance_criteria": ["Bug reproduced", "Root cause identified"],
                },
                {
                    "name": "Fix Implementation",
                    "description": "Implement the bug fix",
                    "tasks": ["Code fix", "Unit tests", "Regression tests"],
                    "deliverables": ["Fixed code", "Test coverage", "Documentation"],
                    "acceptance_criteria": ["Fix implemented", "Tests passing"],
                },
                {
                    "name": "Validation",
                    "description": "Validate the fix and ensure no regressions",
                    "tasks": ["Integration testing", "Regression testing", "User validation"],
                    "deliverables": ["Test results", "Validation report"],
                    "acceptance_criteria": ["Bug fixed", "No regressions", "User confirmed"],
                },
            ],
            "stakeholders": ["developer", "QA", "PM"],
            "risk_factors": ["regression_risk", "side_effects", "timeline_pressure"],
            "success_criteria": [
                "Bug is fixed and verified",
                "No regressions introduced",
                "Tests pass with adequate coverage",
                "User confirms fix works correctly",
            ],
        },
        "performance_optimization": {
            "phases": [
                {
                    "name": "Profiling and Analysis",
                    "description": "Profile system and identify performance bottlenecks",
                    "tasks": ["Performance profiling", "Bottleneck identification", "Baseline establishment"],
                    "deliverables": ["Profile report", "Bottleneck analysis", "Performance baseline"],
                    "acceptance_criteria": ["Bottlenecks identified", "Baseline established"],
                },
                {
                    "name": "Optimization Implementation",
                    "description": "Implement performance optimizations",
                    "tasks": ["Code optimization", "Algorithm improvements", "Resource optimization"],
                    "deliverables": ["Optimized code", "Performance improvements", "Documentation"],
                    "acceptance_criteria": ["Optimizations implemented", "Performance improved"],
                },
                {
                    "name": "Validation and Monitoring",
                    "description": "Validate performance improvements and set up monitoring",
                    "tasks": ["Performance testing", "Load testing", "Monitoring setup"],
                    "deliverables": ["Performance metrics", "Load test results", "Monitoring dashboard"],
                    "acceptance_criteria": ["Performance targets met", "Monitoring active", "System stable"],
                },
            ],
            "stakeholders": ["architect", "developer", "QA", "devops"],
            "risk_factors": ["system_stability", "complexity_increase", "performance_regression"],
            "success_criteria": [
                "Performance targets are met or exceeded",
                "System stability is maintained",
                "Performance monitoring is in place",
                "No regressions in functionality",
            ],
        },
        "refactoring": {
            "phases": [
                {
                    "name": "Analysis and Planning",
                    "description": "Analyze current code and plan refactoring approach",
                    "tasks": ["Code analysis", "Technical debt assessment", "Refactoring planning"],
                    "deliverables": ["Analysis report", "Refactoring plan", "Risk assessment"],
                    "acceptance_criteria": ["Analysis complete", "Plan approved"],
                },
                {
                    "name": "Incremental Refactoring",
                    "description": "Perform refactoring in small, safe increments",
                    "tasks": ["Code refactoring", "Test updates", "Documentation updates"],
                    "deliverables": ["Refactored code", "Updated tests", "Updated documentation"],
                    "acceptance_criteria": ["Refactoring complete", "Tests passing", "No regressions"],
                },
                {
                    "name": "Validation and Cleanup",
                    "description": "Validate refactoring results and clean up",
                    "tasks": ["Integration testing", "Performance testing", "Code review", "Cleanup"],
                    "deliverables": ["Test results", "Performance metrics", "Review feedback", "Clean codebase"],
                    "acceptance_criteria": [
                        "All tests passing",
                        "Performance maintained",
                        "Code reviewed",
                        "Cleanup complete",
                    ],
                },
            ],
            "stakeholders": ["architect", "developer", "QA"],
            "risk_factors": ["breaking_changes", "test_coverage", "system_stability"],
            "success_criteria": [
                "Refactoring completed without breaking changes",
                "Code quality improved as measured by metrics",
                "All tests pass with adequate coverage",
                "System performance maintained or improved",
            ],
        },
        "infrastructure": {
            "phases": [
                {
                    "name": "Infrastructure Planning",
                    "description": "Plan infrastructure changes and requirements",
                    "tasks": ["Requirements analysis", "Architecture design", "Security review", "Cost analysis"],
                    "deliverables": [
                        "Infrastructure plan",
                        "Architecture diagram",
                        "Security assessment",
                        "Cost estimate",
                    ],
                    "acceptance_criteria": ["Plan approved", "Security reviewed", "Cost approved"],
                },
                {
                    "name": "Implementation and Setup",
                    "description": "Implement infrastructure changes",
                    "tasks": ["Infrastructure setup", "Configuration", "Monitoring setup", "Backup setup"],
                    "deliverables": ["Infrastructure code", "Configuration files", "Monitoring setup", "Backup system"],
                    "acceptance_criteria": ["Infrastructure deployed", "Monitoring active", "Backups configured"],
                },
                {
                    "name": "Testing and Deployment",
                    "description": "Test and deploy infrastructure changes",
                    "tasks": ["Infrastructure testing", "Deployment", "Validation", "Documentation"],
                    "deliverables": ["Test results", "Deployment logs", "Validation report", "Documentation"],
                    "acceptance_criteria": ["Tests passing", "Deployment successful", "System validated", "Documented"],
                },
            ],
            "stakeholders": ["architect", "devops", "QA", "security"],
            "risk_factors": ["system_downtime", "data_loss", "security_vulnerabilities", "cost_overrun"],
            "success_criteria": [
                "Infrastructure deployed successfully",
                "All systems operational and stable",
                "Security requirements met",
                "Monitoring and backup systems in place",
            ],
        },
    }

    def get_base_template(self, domain_type: str) -> dict[str, Any]:
        """Get base template for domain type with intelligent customization."""
        return self.TEMPLATES.get(domain_type, self.TEMPLATES["feature_development"])

    def get_customized_template(self, domain_type: str, complexity_level: str, risk_level: str) -> dict[str, Any]:
        """Get customized template based on domain type, complexity, and risk level."""
        base_template = self.get_base_template(domain_type)
        customized = base_template.copy()

        # Adjust phases based on complexity
        if complexity_level == "simple":
            # Simplify phases for simple tasks
            if len(customized["phases"]) > 2:
                customized["phases"] = customized["phases"][:2]
        elif complexity_level == "complex":
            # Add additional phases for complex tasks
            if domain_type == "feature_development":
                additional_phase = {
                    "name": "Advanced Testing",
                    "description": "Comprehensive testing for complex feature",
                    "tasks": ["Stress testing", "Security testing", "Compatibility testing"],
                    "deliverables": ["Advanced test results", "Security report", "Compatibility matrix"],
                    "acceptance_criteria": [
                        "All advanced tests passing",
                        "Security validated",
                        "Compatibility confirmed",
                    ],
                }
                customized["phases"].insert(-1, additional_phase)

        # Adjust risk factors based on risk level
        if risk_level == "high":
            customized["risk_factors"].extend(["timeline_pressure", "resource_constraints"])
        elif risk_level == "critical":
            customized["risk_factors"].extend(["system_stability", "data_integrity", "security_vulnerabilities"])

        return customized

    def get_all_templates(self) -> dict[str, dict[str, Any]]:
        """Get all available templates."""
        return self.TEMPLATES.copy()

    def add_custom_template(self, name: str, template: dict[str, Any]) -> None:
        """Add a custom template to the library."""
        self.TEMPLATES[name] = template
        logger.info(f"Added custom template: {name}")

    def validate_template(self, template: dict[str, Any]) -> bool:
        """Validate that a template has the required structure."""
        required_keys = ["phases", "stakeholders", "risk_factors"]

        if not all(key in template for key in required_keys):
            return False

        # Validate phases structure
        for phase in template["phases"]:
            phase_required_keys = ["name", "description", "tasks", "deliverables", "acceptance_criteria"]
            if not all(key in phase for key in phase_required_keys):
                return False

        return True
