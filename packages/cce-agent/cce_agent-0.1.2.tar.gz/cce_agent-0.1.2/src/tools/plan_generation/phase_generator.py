"""
Phase Generator for Intelligent Plan Creation

This module provides dynamic phase generation capabilities based on topic analysis.
"""

import logging
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .topic_analyzer import PlanTopicAnalysis

logger = logging.getLogger(__name__)


class PhaseGenerationOutput(BaseModel):
    """Structured output for phase generation."""

    model_config = ConfigDict(strict=True, extra="forbid")

    phases: list[dict[str, Any]] = Field(description="List of implementation phases")
    dependencies: list[str] = Field(description="List of dependencies between phases")
    risks: list[str] = Field(description="List of identified risks")
    estimated_duration: str = Field(description="Estimated total duration")


class PlanPhaseGenerator:
    """Generate intelligent implementation phases based on topic analysis."""

    def __init__(self, architect_llm=None):
        """Initialize the phase generator with architect model."""
        self.architect_llm = architect_llm or self._create_default_llm()
        self.logger = logging.getLogger(f"{__name__}.PlanPhaseGenerator")

    def _create_default_llm(self):
        """Create default LLM for phase generation."""
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=4096)
        except ImportError:
            self.logger.warning("LangChain OpenAI not available, using fallback")
            return None

    async def generate_phases(self, topic_analysis: PlanTopicAnalysis, semantic_analysis: str = "") -> dict[str, Any]:
        """Generate implementation phases based on topic analysis."""
        try:
            if self.llm:
                return await self._generate_llm_phases(topic_analysis, semantic_analysis)
            else:
                return self._generate_template_phases(topic_analysis)
        except Exception as e:
            self.logger.error(f"Phase generation failed: {e}")
            return self._generate_fallback_phases(topic_analysis)

    async def _generate_llm_phases(self, topic_analysis: PlanTopicAnalysis, semantic_analysis: str) -> dict[str, Any]:
        """Generate phases using LLM intelligence."""
        phase_prompt = f"""
        Generate intelligent implementation phases for this topic:
        
        Topic Analysis:
        - Domain Type: {topic_analysis.domain_type}
        - Complexity Level: {topic_analysis.complexity_level}
        - Architectural Scope: {topic_analysis.architectural_scope}
        - Technology Stack: {topic_analysis.technology_stack}
        - Estimated Effort: {topic_analysis.estimated_effort}
        - Risk Level: {topic_analysis.risk_level}
        - Stakeholders: {topic_analysis.stakeholders_needed}
        
        Semantic File Analysis: {semantic_analysis[:1500]}
        
        Create phases that are:
        1. Specific to this domain type ({topic_analysis.domain_type})
        2. Appropriate for complexity level ({topic_analysis.complexity_level})
        3. Address the architectural scope ({topic_analysis.architectural_scope})
        4. Include necessary stakeholder involvement
        5. Have realistic effort estimates
        6. Include risk mitigation
        
        Return structured phases in JSON format with:
        - phases: array of phase objects with name, description, tasks, deliverables, acceptance_criteria
        - dependencies: array of dependencies
        - risks: array of risk factors
        - estimated_duration: string estimate
        """

        # Use structured output with the LLM
        structured_llm = self.llm.with_structured_output(PhaseGenerationOutput, method="function_calling")

        response = await structured_llm.ainvoke(phase_prompt)

        # Convert Pydantic model to dict format
        return response.model_dump()

    def _generate_template_phases(self, topic_analysis: PlanTopicAnalysis) -> dict[str, Any]:
        """Generate phases using template-based approach."""
        template = self._get_template_for_domain(topic_analysis.domain_type)
        return self._customize_template(template, topic_analysis)

    def _get_template_for_domain(self, domain_type: str) -> dict[str, Any]:
        """Get base template for domain type."""
        templates = {
            "feature": {
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
                ]
            },
            "bugfix": {
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
                ]
            },
            "refactor": {
                "phases": [
                    {
                        "name": "Analysis",
                        "description": "Analyze current code and identify refactoring opportunities",
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
                        "name": "Validation",
                        "description": "Validate refactoring results and performance",
                        "tasks": ["Integration testing", "Performance testing", "Code review"],
                        "deliverables": ["Test results", "Performance metrics", "Review feedback"],
                        "acceptance_criteria": ["All tests passing", "Performance maintained", "Code reviewed"],
                    },
                ]
            },
            "infrastructure": {
                "phases": [
                    {
                        "name": "Infrastructure Planning",
                        "description": "Plan infrastructure changes and requirements",
                        "tasks": ["Requirements analysis", "Architecture design", "Security review"],
                        "deliverables": ["Infrastructure plan", "Architecture diagram", "Security assessment"],
                        "acceptance_criteria": ["Plan approved", "Security reviewed"],
                    },
                    {
                        "name": "Implementation",
                        "description": "Implement infrastructure changes",
                        "tasks": ["Infrastructure setup", "Configuration", "Monitoring setup"],
                        "deliverables": ["Infrastructure code", "Configuration files", "Monitoring setup"],
                        "acceptance_criteria": ["Infrastructure deployed", "Monitoring active"],
                    },
                    {
                        "name": "Testing and Deployment",
                        "description": "Test and deploy infrastructure changes",
                        "tasks": ["Infrastructure testing", "Deployment", "Validation"],
                        "deliverables": ["Test results", "Deployment logs", "Validation report"],
                        "acceptance_criteria": ["Tests passing", "Deployment successful", "System validated"],
                    },
                ]
            },
            "performance": {
                "phases": [
                    {
                        "name": "Profiling and Analysis",
                        "description": "Profile system and identify performance bottlenecks",
                        "tasks": ["Performance profiling", "Bottleneck identification", "Baseline establishment"],
                        "deliverables": ["Profile report", "Bottleneck analysis", "Performance baseline"],
                        "acceptance_criteria": ["Bottlenecks identified", "Baseline established"],
                    },
                    {
                        "name": "Optimization",
                        "description": "Implement performance optimizations",
                        "tasks": ["Code optimization", "Algorithm improvements", "Resource optimization"],
                        "deliverables": ["Optimized code", "Performance improvements", "Documentation"],
                        "acceptance_criteria": ["Optimizations implemented", "Performance improved"],
                    },
                    {
                        "name": "Validation",
                        "description": "Validate performance improvements",
                        "tasks": ["Performance testing", "Load testing", "Regression testing"],
                        "deliverables": ["Performance metrics", "Load test results", "Validation report"],
                        "acceptance_criteria": ["Performance targets met", "No regressions", "System stable"],
                    },
                ]
            },
        }

        return templates.get(domain_type, templates["feature"])

    def _customize_template(self, template: dict[str, Any], topic_analysis: PlanTopicAnalysis) -> dict[str, Any]:
        """Customize template based on topic analysis."""
        customized = template.copy()

        # Adjust phases based on complexity
        if topic_analysis.complexity_level == "simple":
            # Remove some phases for simple tasks
            if len(customized["phases"]) > 2:
                customized["phases"] = customized["phases"][:2]
        elif topic_analysis.complexity_level == "complex":
            # Add additional phases for complex tasks
            if topic_analysis.domain_type == "feature":
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

        # Add dependencies and risks
        customized["dependencies"] = self._generate_dependencies(topic_analysis)
        customized["risks"] = self._generate_risks(topic_analysis)
        customized["estimated_duration"] = self._estimate_duration(topic_analysis)

        return customized

    def _generate_dependencies(self, topic_analysis: PlanTopicAnalysis) -> list[str]:
        """Generate dependencies based on topic analysis."""
        dependencies = ["Codebase analysis", "Stakeholder review"]

        if "frontend" in topic_analysis.architectural_scope:
            dependencies.append("UI/UX design")
        if "database" in topic_analysis.architectural_scope:
            dependencies.append("Database schema review")
        if "api" in topic_analysis.architectural_scope:
            dependencies.append("API specification")
        if topic_analysis.risk_level in ["high", "critical"]:
            dependencies.append("Risk mitigation planning")

        return dependencies

    def _generate_risks(self, topic_analysis: PlanTopicAnalysis) -> list[str]:
        """Generate risks based on topic analysis."""
        risks = ["Technical complexity", "Integration challenges"]

        if topic_analysis.risk_level == "high":
            risks.extend(["Scope creep", "Resource constraints", "Timeline pressure"])
        elif topic_analysis.risk_level == "critical":
            risks.extend(["System stability", "Data integrity", "Security vulnerabilities"])

        if "database" in topic_analysis.architectural_scope:
            risks.append("Data migration complexity")
        if "frontend" in topic_analysis.architectural_scope:
            risks.append("User experience impact")

        return risks

    def _estimate_duration(self, topic_analysis: PlanTopicAnalysis) -> str:
        """Estimate duration based on topic analysis."""
        base_duration = {
            "simple": "1-2 weeks",
            "moderate": "2-4 weeks",
            "complex": "4-8 weeks",
            "enterprise": "8+ weeks",
        }

        duration = base_duration.get(topic_analysis.complexity_level, "2-4 weeks")

        if topic_analysis.risk_level in ["high", "critical"]:
            duration += " (with risk buffer)"

        return duration

    def _parse_phase_response(self, response_content: str, topic_analysis: PlanTopicAnalysis) -> dict[str, Any]:
        """Parse LLM response into structured phase structure."""
        try:
            import json

            # Try to extract JSON from response
            if "{" in response_content and "}" in response_content:
                start = response_content.find("{")
                end = response_content.rfind("}") + 1
                json_str = response_content[start:end]
                return json.loads(json_str)
        except Exception as e:
            self.logger.warning(f"Failed to parse phase response: {e}")

        # Fallback to template-based generation
        return self._generate_template_phases(topic_analysis)

    def _generate_fallback_phases(self, topic_analysis: PlanTopicAnalysis) -> dict[str, Any]:
        """Generate fallback phases when all else fails."""
        return {
            "phases": [
                {
                    "name": "Analysis and Design",
                    "description": f"Analyze requirements for {topic_analysis.topic}",
                    "tasks": ["Requirement analysis", "Technical design", "Risk assessment"],
                    "deliverables": ["Requirements document", "Technical specification"],
                    "acceptance_criteria": ["Requirements validated", "Design approved"],
                },
                {
                    "name": "Implementation",
                    "description": f"Implement {topic_analysis.topic}",
                    "tasks": ["Core implementation", "Integration", "Unit testing"],
                    "deliverables": ["Working implementation", "Test coverage"],
                    "acceptance_criteria": ["Functionality complete", "Tests passing"],
                },
                {
                    "name": "Validation and Deployment",
                    "description": f"Validate and deploy {topic_analysis.topic}",
                    "tasks": ["Integration testing", "User acceptance", "Deployment"],
                    "deliverables": ["Validated system", "Deployment documentation"],
                    "acceptance_criteria": ["System validated", "Successfully deployed"],
                },
            ],
            "dependencies": ["Codebase analysis", "Stakeholder review"],
            "risks": ["Technical complexity", "Integration challenges"],
            "estimated_duration": "To be determined based on scope",
        }
