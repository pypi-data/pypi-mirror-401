"""
Synthesis Engine

Combines multiple stakeholder perspectives into a coherent, implementable
architecture description with proper conflict resolution and integration.
"""

import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field

from src.prompts.manager import PromptManager

from .outputs import ISOIEEEFormatter
from .schemas import SynthesisResult


class SynthesisRefinementResult(BaseModel):
    """Structured output for synthesis refinement."""

    model_config = ConfigDict(strict=True, extra="forbid")

    refined_synthesis: str = Field(description="The refined synthesis incorporating stakeholder feedback")
    changes_made: list[str] = Field(description="List of specific changes made based on feedback")
    conflicts_resolved: list[str] = Field(description="List of conflicts that were resolved")


class SynthesisEngine:
    """
    Synthesizes multiple stakeholder contributions into a unified architecture description.

    Handles conflict resolution, integration of perspectives, and creation of
    implementable architecture descriptions.
    """

    def __init__(self, llm: ChatOpenAI | None = None, prompt_manager: PromptManager | None = None):
        self.logger = logging.getLogger(__name__)

        # LLM setup
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.1)

        # Prompt management
        self.prompt_manager = prompt_manager or PromptManager()

        self.logger.info("SynthesisEngine initialized")

    def synthesize_contributions(
        self, contributions: dict[str, list[str]], integration_challenge: str, charter: str | None = None
    ) -> str:
        """
        Synthesize stakeholder contributions into a unified architecture description.

        Args:
            contributions: Dictionary of stakeholder -> list of contributions
            integration_challenge: Original integration challenge
            charter: Optional charter for the session

        Returns:
            Synthesized architecture description
        """

        self.logger.info(f"Synthesizing contributions from {len(contributions)} stakeholders")

        try:
            # Build synthesis prompt
            synthesis_prompt = self._build_synthesis_prompt(contributions, integration_challenge, charter)

            # Use LangGraph's native structured output
            structured_llm = self.llm.with_structured_output(SynthesisResult)

            synthesis = structured_llm.invoke(synthesis_prompt)
            self.logger.info(f"Synthesis completed successfully")
            return synthesis

        except Exception as e:
            self.logger.error(f"Error in synthesis: {e}")
            raise

    def _build_synthesis_prompt(
        self, contributions: dict[str, list[str]], integration_challenge: str, charter: str | None
    ) -> str:
        """Build the synthesis prompt"""

        # Get base synthesis prompt
        base_prompt = self.prompt_manager.get_synthesis_prompt()

        # Format contributions
        formatted_contributions = self._format_contributions(contributions)

        # Build context
        context = f"""
## Integration Challenge

{integration_challenge}

## Charter

{charter or "No specific charter provided"}

## Stakeholder Contributions

{formatted_contributions}

## Synthesis Requirements

Create a comprehensive architecture description that:

1. **Addresses Core Requirements**: Fully satisfies the integration challenge
2. **Integrates All Perspectives**: Incorporates insights from all stakeholders
3. **Resolves Conflicts**: Identifies and resolves contradictions between stakeholder views
4. **Provides Implementation Guidance**: Includes concrete, actionable recommendations
5. **Maintains Quality**: Ensures technical soundness and operational viability

## Output Structure

Organize your synthesis with these sections:

1. **Executive Summary**: High-level overview of the architecture
2. **Core Architecture**: Fundamental design decisions and patterns
3. **Domain Integration**: How different stakeholder concerns are addressed
4. **Implementation Plan**: Phased approach to implementation
5. **Quality Assurance**: Testing, monitoring, and validation strategies
6. **Risk Mitigation**: Identified risks and mitigation approaches

Be specific, practical, and comprehensive in your synthesis.
"""

        return f"{base_prompt}\n\n{context}"

    def _format_contributions(self, contributions: dict[str, Any]) -> str:
        """Format stakeholder contributions for synthesis"""

        if not contributions:
            return "No stakeholder contributions available."

        formatted = []

        for stakeholder, contribution in contributions.items():
            formatted.append(f"\n### {stakeholder.replace('_', ' ').title()} Stakeholder")

            if hasattr(contribution, "perspective"):
                # It's a StakeholderAnalysis object
                formatted.append(f"**Perspective**: {contribution.perspective}")
                formatted.append(f"**Aspects**: {', '.join(contribution.aspects)}")
                formatted.append(f"**Analysis**: {contribution.analysis}")
            else:
                # Fallback for other formats
                formatted.append(f"**Contribution**: {str(contribution)}")

            formatted.append("")  # Empty line for readability

        return "\n".join(formatted)

    def refine_synthesis(self, original_synthesis: str, feedback: dict[str, str], integration_challenge: str) -> str:
        """
        Refine a synthesis based on stakeholder feedback.

        Args:
            original_synthesis: The original synthesis to refine
            feedback: Dictionary of stakeholder -> feedback
            integration_challenge: Original integration challenge

        Returns:
            Refined synthesis
        """

        self.logger.info(f"Refining synthesis with feedback from {len(feedback)} stakeholders")

        try:
            # Build refinement prompt
            refinement_prompt = f"""
You are refining an architecture synthesis based on stakeholder feedback.

## Original Integration Challenge

{integration_challenge}

## Original Synthesis

{original_synthesis}

## Stakeholder Feedback

{self._format_feedback(feedback)}

## Refinement Task

Based on the feedback provided:

1. **Address Specific Concerns**: Incorporate valid points raised by stakeholders
2. **Resolve Conflicts**: Find balanced solutions for contradictory feedback
3. **Maintain Quality**: Ensure the refined synthesis remains coherent and implementable
4. **Preserve Strengths**: Keep aspects that stakeholders found well-addressed
5. **Add Missing Elements**: Include critical concerns that were overlooked

Produce a refined synthesis that addresses the feedback while maintaining overall quality and coherence.
"""

            messages = [
                SystemMessage(content=refinement_prompt),
                HumanMessage(content="Please provide the refined synthesis incorporating the stakeholder feedback."),
            ]

            # Use structured output with the LLM
            structured_llm = self.llm.with_structured_output(SynthesisRefinementResult, method="function_calling")

            response = structured_llm.invoke(messages)

            self.logger.info(f"Synthesis refinement completed ({len(response.refined_synthesis)} chars)")
            self.logger.info(f"Changes made: {len(response.changes_made)}")
            self.logger.info(f"Conflicts resolved: {len(response.conflicts_resolved)}")

            return response.refined_synthesis

        except Exception as e:
            self.logger.error(f"Error in synthesis refinement: {e}")
            raise

    def _format_feedback(self, feedback: dict[str, str]) -> str:
        """Format stakeholder feedback for refinement"""

        if not feedback:
            return "No feedback provided."

        formatted = []

        for stakeholder, stakeholder_feedback in feedback.items():
            formatted.append(f"\n### {stakeholder.replace('_', ' ').title()} Feedback")
            formatted.append(stakeholder_feedback)
            formatted.append("")  # Empty line for readability

        return "\n".join(formatted)

    def extract_implementation_plan(self, synthesis_result: SynthesisResult) -> dict[str, Any] | None:
        """
        Extracts the implementation plan from the synthesis result object.
        """
        try:
            # The plan is now directly accessible via the Pydantic model
            # For now, we'll treat the 'decisions' as the core of the plan
            return {"decisions": [d.dict() for d in synthesis_result.decisions]}
        except Exception as e:
            self.logger.warning(f"Could not extract implementation plan from synthesis object: {e}")
            return None

    def format_iso_ieee(
        self,
        synthesis_result: SynthesisResult,
        stakeholder_contributions: dict,
        integration_challenge: str = "",
        architecture_decisions: list = None,
    ) -> str:
        """
        Formats the architecture description according to enhanced ISO/IEEE 42010 standards.
        """
        formatter = ISOIEEEFormatter(
            synthesis_result,
            stakeholder_contributions,
            integration_challenge=integration_challenge,
            architecture_decisions=architecture_decisions or [],
        )
        return formatter.format()
