"""
Quality Gates System

Evaluates synthesis results for implementation readiness, ticket coverage,
and overall quality using structured assessment criteria.
"""

import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field

from src.prompts.manager import PromptManager

from .schemas import QualityAssessment


class QuickAssessmentResult(BaseModel):
    """Structured output for quick quality assessment."""

    model_config = ConfigDict(strict=True, extra="forbid")

    overall_score: float = Field(description="Overall quality score (0.0-1.0)")
    implementation_readiness: float = Field(description="Implementation readiness score (0.0-1.0)")
    challenge_coverage: float = Field(description="Challenge coverage score (0.0-1.0)")
    technical_soundness: float = Field(description="Technical soundness score (0.0-1.0)")
    feedback: str = Field(description="Brief feedback on the assessment")
    pass_threshold: bool = Field(description="Whether the assessment passes the quality threshold")


class QualityGates:
    """
    Quality assessment system for architecture descriptions.

    Evaluates synthesis results across multiple dimensions including
    implementation readiness, ticket coverage, and stakeholder satisfaction.
    """

    # Quality assessment criteria
    QUALITY_CRITERIA = {
        "implementation_readiness": {
            "weight": 0.3,
            "description": "How ready is this architecture for implementation?",
            "factors": [
                "Concrete implementation steps provided",
                "Technical details are sufficient",
                "Dependencies are clearly identified",
                "Resource requirements are specified",
                "Timeline is realistic",
            ],
        },
        "ticket_coverage": {
            "weight": 0.25,
            "description": "How well does this address the original requirements?",
            "factors": [
                "All stated requirements are addressed",
                "Integration challenge is fully resolved",
                "Charter objectives are met",
                "Success criteria are defined",
                "Edge cases are considered",
            ],
        },
        "stakeholder_balance": {
            "weight": 0.2,
            "description": "Are all stakeholder concerns adequately addressed?",
            "factors": [
                "All stakeholder domains are represented",
                "No domain is significantly underrepresented",
                "Conflicts between domains are resolved",
                "Trade-offs are clearly explained",
                "Consensus is achievable",
            ],
        },
        "technical_feasibility": {
            "weight": 0.15,
            "description": "Is this technically sound and achievable?",
            "factors": [
                "Technical approach is sound",
                "Performance requirements are realistic",
                "Scalability is considered",
                "Security implications are addressed",
                "Integration patterns are proven",
            ],
        },
        "clarity_completeness": {
            "weight": 0.1,
            "description": "Is the description clear and comprehensive?",
            "factors": [
                "Writing is clear and well-organized",
                "Technical concepts are well-explained",
                "Examples are provided where helpful",
                "Documentation is comprehensive",
                "Next steps are clear",
            ],
        },
    }

    def __init__(self, llm: ChatOpenAI | None = None, prompt_manager: PromptManager | None = None):
        self.logger = logging.getLogger(__name__)

        # LLM setup
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0)

        # Prompt management
        self.prompt_manager = prompt_manager or PromptManager()

        self.logger.info("QualityGates initialized")

    def evaluate(
        self, synthesis_result: Any, integration_challenge: str, stakeholder_contributions: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Comprehensive quality evaluation of a synthesis result.

        Args:
            synthesis_result: The synthesis to evaluate
            integration_challenge: Original integration challenge
            stakeholder_contributions: Original stakeholder contributions

        Returns:
            Quality evaluation results with scores and recommendations
        """

        self.logger.info("Starting comprehensive quality evaluation")

        try:
            # Build evaluation prompt
            evaluation_prompt = self._build_evaluation_prompt(
                synthesis_result, integration_challenge, stakeholder_contributions
            )

            # Get LLM evaluation with structured output
            messages = [
                SystemMessage(content=evaluation_prompt),
                HumanMessage(
                    content="Please provide a comprehensive quality evaluation with specific scores and detailed feedback."
                ),
            ]

            try:
                # Try structured output first
                structured_llm = self.llm.with_structured_output(QualityAssessment)
                response = structured_llm.invoke(messages)

                # Convert Pydantic model to dict
                evaluation_result = response.model_dump()

                self.logger.info(
                    f"Quality evaluation completed with structured output - Overall score: {evaluation_result.get('overall_score', 'N/A')}"
                )

                return evaluation_result

            except Exception as structured_error:
                self.logger.warning(f"Structured output failed, falling back to regex parsing: {structured_error}")

                # Fallback to regex parsing
                response = self.llm.invoke(messages)
                evaluation_result = self._parse_evaluation_response(response.content)

                self.logger.info(
                    f"Quality evaluation completed with fallback parsing - Overall score: {evaluation_result.get('overall_score', 'N/A')}"
                )

                return evaluation_result

        except Exception as e:
            self.logger.error(f"Error in quality evaluation: {e}")
            # Return a basic error result
            return {
                "overall_score": 0.0,
                "implementation_readiness": 0.0,
                "ticket_coverage": 0.0,
                "stakeholder_balance": 0.0,
                "technical_feasibility": 0.0,
                "clarity_completeness": 0.0,
                "details": f"Evaluation failed: {str(e)}",
                "recommendations": ["Fix evaluation system error"],
                "pass_threshold": False,
            }

    def _build_evaluation_prompt(
        self, synthesis_result: Any, integration_challenge: str, stakeholder_contributions: dict[str, Any]
    ) -> str:
        """Build the quality evaluation prompt"""

        # Get base quality gates prompt
        base_prompt = self.prompt_manager.get_quality_gates_prompt()

        # Format criteria
        criteria_description = self._format_criteria_description()

        # Format stakeholder summary
        stakeholder_summary = self._format_stakeholder_summary(stakeholder_contributions)

        context = f"""
## Evaluation Context

### Original Integration Challenge
{integration_challenge}

### Stakeholder Contributions Summary
{stakeholder_summary}

### Synthesis to Evaluate
{self._format_synthesis_result(synthesis_result)}

## Quality Criteria

{criteria_description}

## Evaluation Requirements

Provide a structured evaluation with:

1. **Individual Scores** (0.0-1.0) for each criterion:
   - implementation_readiness: {self.QUALITY_CRITERIA["implementation_readiness"]["description"]}
   - ticket_coverage: {self.QUALITY_CRITERIA["ticket_coverage"]["description"]}
   - stakeholder_balance: {self.QUALITY_CRITERIA["stakeholder_balance"]["description"]}
   - technical_feasibility: {self.QUALITY_CRITERIA["technical_feasibility"]["description"]}
   - clarity_completeness: {self.QUALITY_CRITERIA["clarity_completeness"]["description"]}

2. **Overall Score**: Weighted average of individual scores

3. **Detailed Feedback**: Specific strengths and weaknesses for each criterion

4. **Recommendations**: Concrete suggestions for improvement

5. **Pass/Fail Decision**: Whether this meets minimum quality standards (>0.7 overall)

## Response Format

Please structure your response as follows:

### Scores
- Implementation Readiness: X.X/1.0
- Ticket Coverage: X.X/1.0  
- Stakeholder Balance: X.X/1.0
- Technical Feasibility: X.X/1.0
- Clarity & Completeness: X.X/1.0
- **Overall Score: X.X/1.0**

### Detailed Analysis
[Provide detailed analysis for each criterion]

### Recommendations
[List specific improvement recommendations]

### Decision
[PASS/FAIL with rationale]
"""

        return f"{base_prompt}\n\n{context}"

    def _format_criteria_description(self) -> str:
        """Format the quality criteria for the prompt"""
        formatted = []

        for criterion, config in self.QUALITY_CRITERIA.items():
            formatted.append(f"\n**{criterion.replace('_', ' ').title()}** (Weight: {config['weight']}):")
            formatted.append(f"  {config['description']}")
            formatted.append("  Key factors:")
            for factor in config["factors"]:
                formatted.append(f"    - {factor}")

        return "\n".join(formatted)

    def _format_stakeholder_summary(self, contributions: dict[str, Any]) -> str:
        """Format stakeholder contributions summary"""
        if not contributions:
            return "No stakeholder contributions available."

        summary = []
        for stakeholder, contribution in contributions.items():
            if hasattr(contribution, "analysis"):
                # It's a StakeholderAnalysis object
                analysis_length = len(contribution.analysis)
                summary.append(
                    f"- **{stakeholder.replace('_', ' ').title()}**: {contribution.perspective} ({analysis_length} chars)"
                )
            else:
                # Fallback for other formats
                summary.append(f"- **{stakeholder.replace('_', ' ').title()}**: {str(contribution)[:100]}...")

        return "\n".join(summary)

    def _format_synthesis_result(self, synthesis_result: Any) -> str:
        """Format synthesis result for evaluation"""
        if hasattr(synthesis_result, "introduction"):
            # It's a SynthesisResult object
            formatted = f"**Introduction**: {synthesis_result.introduction}\n\n"
            formatted += f"**Architecture Views**: {len(synthesis_result.architecture_views)} views\n"
            formatted += f"**Decisions**: {len(synthesis_result.decisions)} decisions\n"
            formatted += f"**Considerations**: {len(synthesis_result.architecture_considerations)} considerations\n"
            return formatted
        else:
            # Fallback for string or other formats
            return str(synthesis_result)

    def _parse_evaluation_response(self, response_content: str) -> dict[str, Any]:
        """Parse the LLM evaluation response into structured data"""

        # Initialize result structure
        result = {
            "overall_score": 0.0,
            "implementation_readiness": 0.0,
            "ticket_coverage": 0.0,
            "stakeholder_balance": 0.0,
            "technical_feasibility": 0.0,
            "clarity_completeness": 0.0,
            "details": response_content,
            "recommendations": [],
            "pass_threshold": False,
        }

        try:
            # Extract scores using regex patterns
            import re

            # Score patterns
            patterns = {
                "implementation_readiness": r"Implementation Readiness:\s*(\d+\.?\d*)",
                "ticket_coverage": r"Ticket Coverage:\s*(\d+\.?\d*)",
                "stakeholder_balance": r"Stakeholder Balance:\s*(\d+\.?\d*)",
                "technical_feasibility": r"Technical Feasibility:\s*(\d+\.?\d*)",
                "clarity_completeness": r"Clarity.*?Completeness:\s*(\d+\.?\d*)",
                "overall_score": r"Overall Score:\s*(\d+\.?\d*)",
            }

            for key, pattern in patterns.items():
                match = re.search(pattern, response_content, re.IGNORECASE)
                if match:
                    score = float(match.group(1))
                    # Normalize to 0-1 range if needed
                    if score > 1.0:
                        score = score / 10.0 if score <= 10.0 else 1.0
                    result[key] = score

            # Calculate overall score if not found
            if result["overall_score"] == 0.0:
                weights = [
                    result["implementation_readiness"] * self.QUALITY_CRITERIA["implementation_readiness"]["weight"],
                    result["ticket_coverage"] * self.QUALITY_CRITERIA["ticket_coverage"]["weight"],
                    result["stakeholder_balance"] * self.QUALITY_CRITERIA["stakeholder_balance"]["weight"],
                    result["technical_feasibility"] * self.QUALITY_CRITERIA["technical_feasibility"]["weight"],
                    result["clarity_completeness"] * self.QUALITY_CRITERIA["clarity_completeness"]["weight"],
                ]
                result["overall_score"] = sum(weights)

            # Extract recommendations
            recommendations_section = re.search(
                r"### Recommendations\s*(.*?)(?:###|$)", response_content, re.DOTALL | re.IGNORECASE
            )
            if recommendations_section:
                recommendations_text = recommendations_section.group(1)
                # Extract bullet points or numbered items
                recommendations = re.findall(r"[-*]\s*(.+?)(?=\n|$)", recommendations_text)
                result["recommendations"] = [rec.strip() for rec in recommendations if rec.strip()]
            else:
                # Fallback: try to extract any list-like content
                list_patterns = [
                    r"recommendations?:\s*\[(.*?)\]",  # JSON-like format
                    r"recommendations?:\s*(.*?)(?:\n\n|\n###|$)",  # Plain text format
                ]

                for pattern in list_patterns:
                    match = re.search(pattern, response_content, re.DOTALL | re.IGNORECASE)
                    if match:
                        content = match.group(1)
                        # Try to parse as JSON array
                        try:
                            import json

                            parsed = json.loads(f"[{content}]")
                            if isinstance(parsed, list):
                                result["recommendations"] = [str(item).strip() for item in parsed if str(item).strip()]
                                break
                        except:
                            pass

                        # Fallback to splitting by common delimiters
                        if "," in content:
                            items = [item.strip().strip("\"'") for item in content.split(",")]
                        elif "\n" in content:
                            items = [item.strip() for item in content.split("\n") if item.strip()]
                        else:
                            items = [content.strip()]

                        result["recommendations"] = [item for item in items if item and len(item) > 3]
                        break

                # Final fallback if nothing worked
                if "recommendations" not in result:
                    result["recommendations"] = ["Review implementation for completeness and quality"]

            # Determine pass/fail
            result["pass_threshold"] = result["overall_score"] >= 0.7

            self.logger.debug(f"Parsed evaluation scores: {result['overall_score']:.2f} overall")

        except Exception as e:
            self.logger.warning(f"Error parsing evaluation response: {e}")
            # Keep the raw response in details
            result["details"] = f"Parsing error: {str(e)}\n\nRaw response:\n{response_content}"

        return result

    def quick_assessment(self, synthesis_result: str, integration_challenge: str) -> dict[str, Any]:
        """
        Perform a quick quality assessment without full stakeholder context.

        Args:
            synthesis_result: The synthesis to assess
            integration_challenge: Original integration challenge

        Returns:
            Quick assessment results
        """

        self.logger.info("Performing quick quality assessment")

        try:
            quick_prompt = f"""
Perform a quick quality assessment of this architecture synthesis:

## Integration Challenge
{integration_challenge}

## Synthesis
{synthesis_result}

Rate on a scale of 0.0-1.0:
1. Implementation Readiness: How implementable is this?
2. Challenge Coverage: How well does this address the integration challenge?
3. Technical Soundness: Is this technically feasible?

Provide brief feedback and a pass/fail recommendation (pass threshold: 0.7).

Format:
Implementation Readiness: X.X
Challenge Coverage: X.X  
Technical Soundness: X.X
Overall: X.X
Feedback: [brief feedback]
Decision: PASS/FAIL
"""

            messages = [
                SystemMessage(content=quick_prompt),
                HumanMessage(content="Please provide the quick assessment."),
            ]

            # Use structured output with the LLM
            structured_llm = self.llm.with_structured_output(QuickAssessmentResult, method="function_calling")

            response = structured_llm.invoke(messages)

            # Convert Pydantic model to dict format
            result = response.model_dump()

            self.logger.info(f"Quick assessment completed - Overall: {result.get('overall_score', 'N/A')}")

            return result

        except Exception as e:
            self.logger.error(f"Error in quick assessment: {e}")
            return {
                "overall_score": 0.0,
                "implementation_readiness": 0.0,
                "challenge_coverage": 0.0,
                "technical_soundness": 0.0,
                "feedback": f"Assessment failed: {str(e)}",
                "pass_threshold": False,
            }

    def _parse_quick_response(self, response_content: str) -> dict[str, Any]:
        """Parse quick assessment response"""

        result = {
            "overall_score": 0.0,
            "implementation_readiness": 0.0,
            "challenge_coverage": 0.0,
            "technical_soundness": 0.0,
            "feedback": response_content,
            "pass_threshold": False,
        }

        try:
            import re

            # Extract scores
            patterns = {
                "implementation_readiness": r"Implementation Readiness:\s*(\d+\.?\d*)",
                "challenge_coverage": r"Challenge Coverage:\s*(\d+\.?\d*)",
                "technical_soundness": r"Technical Soundness:\s*(\d+\.?\d*)",
                "overall_score": r"Overall:\s*(\d+\.?\d*)",
            }

            for key, pattern in patterns.items():
                match = re.search(pattern, response_content, re.IGNORECASE)
                if match:
                    score = float(match.group(1))
                    if score > 1.0:
                        score = score / 10.0 if score <= 10.0 else 1.0
                    result[key] = score

            # Calculate overall if not found
            if result["overall_score"] == 0.0:
                result["overall_score"] = (
                    result["implementation_readiness"] + result["challenge_coverage"] + result["technical_soundness"]
                ) / 3.0

            result["pass_threshold"] = result["overall_score"] >= 0.7

        except Exception as e:
            self.logger.warning(f"Error parsing quick response: {e}")

        return result
