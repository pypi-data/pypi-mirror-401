import json
import logging
from typing import Any

from ..schemas import StakeholderAnalysis
from .stakeholder_agents.stakeholder_config import STAKEHOLDER_CONFIG
from .stakeholder_agents.stakeholder_context import StakeholderContext


class StakeholderAgent:
    def __init__(self, stakeholder_type, llm: Any | None = None):
        self.stakeholder_type = stakeholder_type
        self.name = stakeholder_type.value.replace("_", " ").title()
        self.logger = logging.getLogger(f"StakeholderAgent.{self.stakeholder_type.value}")

        # Initialize LLM
        if llm:
            self.llm = llm
        else:
            from langchain_openai import ChatOpenAI

            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=4096)

        # Initialize PromptManager
        from src.prompts.manager import PromptManager

        self.prompt_manager = PromptManager()

        # Get stakeholder-specific config
        self.domain_info = STAKEHOLDER_CONFIG.get(self.stakeholder_type.value, {})
        self.stakeholder_prompt = self.prompt_manager.get_stakeholder_prompt(
            self.stakeholder_type.value, self.domain_info
        )

    def analyze(self, context: "StakeholderContext") -> StakeholderAnalysis:
        """
        Analyzes the integration challenge and returns a structured Pydantic object.
        """
        self.logger.info(f"Starting analysis for {self.name}")

        prompt = self.prompt_manager.compose_stakeholder_analysis_prompt(
            self.stakeholder_prompt,
            {
                "integration_challenge": context.integration_challenge,
                "charter": context.charter,
                "focus_areas": "\n".join(f"- {area}" for area in self.domain_info.get("focus_areas", [])),
                "previous_contributions": json.dumps(context.previous_contributions, indent=2),
                "analysis_guidance": "Provide your analysis as a single JSON object, following the format specified.",
            },
        )

        # Create a new LLM instance with structured output
        structured_llm = self.llm.with_structured_output(StakeholderAnalysis)

        try:
            response = structured_llm.invoke(prompt)
            self.logger.info(f"Completed analysis for {self.name}")
            self.logger.info(f"Response type: {type(response)}, perspective: {response.perspective}")
            return response
        except Exception as e:
            self.logger.error(f"Failed to get structured response for {self.name}: {e}")
            import traceback

            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            # Return a fallback object
            return StakeholderAnalysis(
                perspective="Error", aspects=[], analysis=f"Failed to generate valid analysis due to an error: {e}"
            )

    def get_domain_info(self) -> dict[str, Any]:
        """
        Returns the domain information for the stakeholder.
        """
        return self.domain_info
