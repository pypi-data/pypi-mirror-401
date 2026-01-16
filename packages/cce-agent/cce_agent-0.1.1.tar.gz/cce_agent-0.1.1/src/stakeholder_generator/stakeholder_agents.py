"""
Stakeholder Agents - Individual Domain Experts

Each stakeholder agent represents a specific domain expertise and provides
focused analysis and recommendations for the architecture description.
"""

import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
try:
    from langchain_openai import ChatOpenAI
except ImportError:  # pragma: no cover - optional dependency
    ChatOpenAI = None
try:
    from langchain_anthropic import ChatAnthropic
except ImportError:  # pragma: no cover - optional dependency
    ChatAnthropic = None
from pydantic import BaseModel, ConfigDict, Field

from src.prompts.manager import PromptManager


class StakeholderFeedbackResult(BaseModel):
    """Structured output for stakeholder feedback."""

    model_config = ConfigDict(strict=True, extra="forbid")

    feedback: str = Field(description="Detailed feedback on the synthesis")
    concerns: list[str] = Field(description="List of specific concerns raised")
    recommendations: list[str] = Field(description="List of specific recommendations")
    domain_support_score: float = Field(
        description="Score (0.0-1.0) for how well synthesis supports domain requirements"
    )


class StakeholderType(Enum):
    """Types of stakeholder agents available"""

    AIDER_INTEGRATION = "aider_integration"
    CONTEXT_ENGINEERING = "context_engineering"
    LANGGRAPH_ARCHITECTURE = "langgraph_architecture"
    PRODUCTION_STABILITY = "production_stability"
    DEVELOPER_EXPERIENCE = "developer_experience"


@dataclass
class StakeholderContext:
    """Context provided to stakeholder for analysis"""

    integration_challenge: str
    charter: str
    previous_contributions: dict[str, list[str]]
    messages: list[BaseMessage]
    additional_context: dict[str, Any] | None = None


class StakeholderAgent:
    """
    Individual stakeholder agent with domain-specific expertise.

    Each agent represents a particular viewpoint and set of concerns
    in the architecture description process.
    """

    STAKEHOLDER_DOMAINS = {
        StakeholderType.AIDER_INTEGRATION: {
            "name": "AIDER Integration Specialist",
            "domain": "AIDER-inspired tooling and capabilities",
            "focus_areas": [
                "RepoMap and semantic codebase understanding",
                "Multi-strategy editing (UnifiedDiff, EditBlock, WholeFile)",
                "Validation pipelines and automated testing",
                "Git operations and safety mechanisms",
                "Tool integration patterns",
            ],
        },
        StakeholderType.CONTEXT_ENGINEERING: {
            "name": "Context Engineering Specialist",
            "domain": "Context management and memory architectures",
            "focus_areas": [
                "Multi-layered memory systems (Working, Episodic, Procedural)",
                "Token optimization and aggressive trimming",
                "Semantic context injection and retrieval",
                "Prompt caching and optimization",
                "Context switching strategies",
            ],
        },
        StakeholderType.LANGGRAPH_ARCHITECTURE: {
            "name": "LangGraph Architecture Specialist",
            "domain": "LangGraph orchestration and state management",
            "focus_areas": [
                "StateGraph design and composition",
                "Multi-agent coordination patterns",
                "Checkpointing and persistence",
                "Tool integration and execution flows",
                "Graph observability and debugging",
            ],
        },
        StakeholderType.PRODUCTION_STABILITY: {
            "name": "Production Stability Specialist",
            "domain": "Operational reliability and performance",
            "focus_areas": [
                "Error handling and recovery strategies",
                "Performance optimization and monitoring",
                "Failure mode analysis and mitigation",
                "Rollback and safety mechanisms",
                "Resource management and scaling",
            ],
        },
        StakeholderType.DEVELOPER_EXPERIENCE: {
            "name": "Developer Experience Specialist",
            "domain": "API design and maintainability",
            "focus_areas": [
                "Clean API design and interfaces",
                "Debugging capabilities and tooling",
                "Documentation and onboarding",
                "Testing strategies and maintainability",
                "Code organization and modularity",
            ],
        },
    }

    def __init__(
        self,
        stakeholder_type: StakeholderType,
        llm: ChatOpenAI | None = None,
        prompt_manager: PromptManager | None = None,
    ):
        self.stakeholder_type = stakeholder_type
        self.config = self.STAKEHOLDER_DOMAINS[stakeholder_type]
        self.logger = logging.getLogger(f"{__name__}.{stakeholder_type.value}")

        # LLM setup
        self.logger.info(f"Initializing LLM for {self.config['name']}...")
        print(f"🔍 [DEBUG] {self.config['name']}: Initializing LLM...")
        self.llm = llm or self._build_default_llm()
        self.logger.info(f"LLM initialized successfully for {self.config['name']}")
        print(f"✅ [DEBUG] {self.config['name']}: LLM initialized successfully")

        # Prompt management
        self.logger.info(f"Initializing PromptManager for {self.config['name']}...")
        print(f"🔍 [DEBUG] {self.config['name']}: Initializing PromptManager...")
        self.prompt_manager = prompt_manager or PromptManager()
        self.logger.info(f"PromptManager initialized successfully for {self.config['name']}")
        print(f"✅ [DEBUG] {self.config['name']}: PromptManager initialized successfully")

        self.logger.info(f"Initialized {self.config['name']}")

    def _build_default_llm(self):
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if anthropic_key and ChatAnthropic:
            return ChatAnthropic(
                model=os.getenv("STAKEHOLDER_MODEL_ANTHROPIC", "claude-3-haiku-20240307"),
                temperature=0.1,
                api_key=anthropic_key,
            )

        if openai_key and ChatOpenAI:
            return ChatOpenAI(
                model=os.getenv("STAKEHOLDER_MODEL_OPENAI", "gpt-4o"),
                temperature=0.1,
            )

        if ChatOpenAI:
            return ChatOpenAI(model="gpt-4o", temperature=0.1)

        if ChatAnthropic:
            return ChatAnthropic(
                model=os.getenv("STAKEHOLDER_MODEL_ANTHROPIC", "claude-3-haiku-20240307"),
                temperature=0.1,
                api_key=anthropic_key,
            )

        raise RuntimeError("No supported LLM client available for stakeholder agents.")

    def analyze(self, context: StakeholderContext) -> str:
        """
        Perform stakeholder-specific analysis of the integration challenge.

        Args:
            context: Analysis context including challenge, charter, and history

        Returns:
            Detailed analysis and recommendations from this stakeholder's perspective
        """

        self.logger.info(f"Starting analysis for {self.config['name']}")
        print(f"🔍 [DEBUG] {self.config['name']}: Starting analysis...")

        try:
            # Log context details
            self.logger.info(f"Context integration_challenge length: {len(context.integration_challenge)}")
            print(f"🔍 [DEBUG] {self.config['name']}: Context length: {len(context.integration_challenge)} chars")

            # Build the analysis prompt
            self.logger.info(f"Building analysis prompt...")
            print(f"🔍 [DEBUG] {self.config['name']}: Building analysis prompt...")
            prompt = self._build_analysis_prompt(context)

            self.logger.info(f"Prompt length: {len(prompt)} chars")
            print(f"🔍 [DEBUG] {self.config['name']}: Prompt length: {len(prompt)} chars")

            # Use LangGraph's native structured output
            from .schemas import StakeholderAnalysis

            self.logger.info(f"Creating structured LLM...")
            print(f"🔍 [DEBUG] {self.config['name']}: Creating structured LLM...")
            structured_llm = self.llm.with_structured_output(StakeholderAnalysis)

            self.logger.info(f"Invoking LLM...")
            print(f"🔍 [DEBUG] {self.config['name']}: Invoking LLM...")
            response = structured_llm.invoke(prompt)

            self.logger.info(f"Completed analysis for {self.config['name']}")
            self.logger.info(f"Response type: {type(response)}, perspective: {response.perspective}")
            print(f"✅ [DEBUG] {self.config['name']}: Analysis completed successfully")
            print(f"🔍 [DEBUG] {self.config['name']}: Response type: {type(response)}")

            return response

        except Exception as e:
            self.logger.error(f"Error in analysis for {self.config['name']}: {e}")
            import traceback

            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            # Return a fallback object
            from .schemas import StakeholderAnalysis

            return StakeholderAnalysis(
                perspective="Error", aspects=[], analysis=f"Failed to generate valid analysis due to an error: {e}"
            )

    def _build_analysis_prompt(self, context: StakeholderContext) -> str:
        """Build the analysis prompt for this stakeholder"""

        self.logger.info(f"Building prompt for {self.stakeholder_type.value}...")
        print(f"🔍 [DEBUG] {self.config['name']}: Building prompt for {self.stakeholder_type.value}...")

        # Get stakeholder-specific prompt template
        try:
            stakeholder_prompt = self.prompt_manager.get_stakeholder_prompt(self.stakeholder_type.value, self.config)
            self.logger.info(f"Prompt template loaded successfully, length: {len(stakeholder_prompt)}")
            print(f"🔍 [DEBUG] {self.config['name']}: Prompt template loaded, length: {len(stakeholder_prompt)}")
        except Exception as e:
            self.logger.error(f"Failed to load prompt template: {e}")
            print(f"❌ [DEBUG] {self.config['name']}: Failed to load prompt template: {e}")
            raise

        # Build context sections
        context_sections = {
            "integration_challenge": context.integration_challenge,
            "charter": context.charter or "No specific charter provided",
            "focus_areas": self._format_focus_areas(),
            "previous_contributions": self._format_previous_contributions(context.previous_contributions),
            "analysis_guidance": self._get_analysis_guidance(),
        }

        # Compose final prompt
        return self.prompt_manager.compose_stakeholder_analysis_prompt(stakeholder_prompt, context_sections)

    def _format_focus_areas(self) -> str:
        """Format the focus areas for this stakeholder"""
        areas = self.config["focus_areas"]
        return "\n".join(f"- {area}" for area in areas)

    def _format_previous_contributions(self, contributions: dict[str, list[str]]) -> str:
        """Format previous stakeholder contributions for context"""
        if not contributions:
            return "No previous contributions yet."

        formatted = []
        for stakeholder, stakeholder_contribs in contributions.items():
            if stakeholder != self.stakeholder_type.value:  # Don't include own contributions
                formatted.append(f"\n**{stakeholder.title()}:**")
                for i, contrib in enumerate(stakeholder_contribs, 1):
                    # Truncate long contributions for context
                    truncated = contrib[:500] + "..." if len(contrib) > 500 else contrib
                    formatted.append(f"  {i}. {truncated}")

        return "\n".join(formatted) if formatted else "No relevant previous contributions."

    def _get_analysis_guidance(self) -> str:
        """Get specific analysis guidance for this stakeholder type"""

        guidance = {
            StakeholderType.AIDER_INTEGRATION: """
Focus on how AIDER's capabilities can be integrated effectively:
- Evaluate RepoMap requirements for semantic understanding
- Assess multi-strategy editing needs (when to use UnifiedDiff vs EditBlock vs WholeFile)
- Consider validation pipeline integration points
- Address Git safety and rollback mechanisms
- Identify tool composition patterns
""",
            StakeholderType.CONTEXT_ENGINEERING: """
Focus on context management and memory architecture:
- Analyze memory layer requirements (Working, Episodic, Procedural)
- Evaluate token optimization strategies
- Consider context injection and retrieval patterns
- Assess prompt caching opportunities
- Address context switching and trimming needs
""",
            StakeholderType.LANGGRAPH_ARCHITECTURE: """
Focus on LangGraph orchestration and state management:
- Design StateGraph structure and composition
- Evaluate multi-agent coordination needs
- Consider checkpointing and persistence requirements
- Assess tool integration patterns
- Address observability and debugging needs
""",
            StakeholderType.PRODUCTION_STABILITY: """
Focus on operational reliability and performance:
- Identify failure modes and recovery strategies
- Evaluate performance bottlenecks and optimization opportunities
- Consider monitoring and observability requirements
- Assess rollback and safety mechanisms
- Address resource management and scaling concerns
""",
            StakeholderType.DEVELOPER_EXPERIENCE: """
Focus on API design and maintainability:
- Evaluate interface design and usability
- Consider debugging and troubleshooting capabilities
- Assess documentation and onboarding requirements
- Address testing strategies and maintainability
- Consider code organization and modularity
""",
        }

        return guidance.get(self.stakeholder_type, "Provide analysis from your domain perspective.")

    def provide_feedback(self, synthesis: str, context: StakeholderContext) -> str:
        """
        Provide feedback on a synthesis from this stakeholder's perspective.

        Args:
            synthesis: The synthesis to review
            context: Original context for reference

        Returns:
            Feedback and recommendations
        """

        self.logger.info(f"Providing feedback from {self.config['name']}")

        try:
            # Build feedback prompt
            prompt = f"""You are the {self.config["name"]} reviewing an architecture synthesis.

Your domain expertise: {self.config["domain"]}

Your focus areas:
{self._format_focus_areas()}

Original Integration Challenge:
{context.integration_challenge}

Synthesis to Review:
{synthesis}

Please provide feedback from your domain perspective:
1. What aspects are well-addressed?
2. What critical concerns are missing or inadequately addressed?
3. What specific recommendations do you have for improvement?
4. How well does this synthesis support your domain's requirements?

Be specific and constructive in your feedback."""

            messages = [
                SystemMessage(content=prompt),
                HumanMessage(content="Please provide your detailed feedback on this synthesis."),
            ]

            # Use structured output with the LLM
            structured_llm = self.llm.with_structured_output(StakeholderFeedbackResult, method="function_calling")

            response = structured_llm.invoke(messages)

            self.logger.info(f"Completed feedback from {self.config['name']} ({len(response.feedback)} chars)")
            self.logger.info(f"Concerns raised: {len(response.concerns)}")
            self.logger.info(f"Recommendations: {len(response.recommendations)}")
            self.logger.info(f"Domain support score: {response.domain_support_score}")

            return response.feedback

        except Exception as e:
            self.logger.error(f"Error providing feedback from {self.config['name']}: {e}")
            raise

    def get_domain_info(self) -> dict[str, Any]:
        """Get information about this stakeholder's domain"""
        return {
            "type": self.stakeholder_type.value,
            "name": self.config["name"],
            "domain": self.config["domain"],
            "focus_areas": self.config["focus_areas"],
        }
