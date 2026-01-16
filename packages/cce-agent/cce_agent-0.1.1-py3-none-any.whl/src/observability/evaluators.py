"""
Advanced Observability - Custom Evaluators

CCE-specific evaluators for LangSmith integration providing detailed
metrics on architecture generation quality and stakeholder coordination.
"""

import logging
import time
from dataclasses import dataclass
from typing import Any

try:
    from langsmith import Client
    from langsmith.evaluation import StringEvaluator, evaluate

    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    logging.warning("LangSmith not available. Install langsmith package for advanced evaluators.")


@dataclass
class EvaluationResult:
    """Result of an evaluation"""

    score: float
    details: str
    metadata: dict[str, Any]
    timestamp: float


class ImplementationReadinessEvaluator:
    """Evaluates how ready an architecture description is for implementation"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def evaluate(self, synthesis: str, context: dict[str, Any]) -> EvaluationResult:
        """
        Evaluate implementation readiness of a synthesis.

        Args:
            synthesis: The architecture synthesis to evaluate
            context: Additional context for evaluation

        Returns:
            Evaluation result with score and details
        """

        score = 0.0
        details = []
        metadata = {}

        # Check for concrete implementation steps
        if "implementation" in synthesis.lower() and "step" in synthesis.lower():
            score += 0.2
            details.append("✓ Contains implementation steps")
        else:
            details.append("✗ Missing concrete implementation steps")

        # Check for technical details
        technical_keywords = ["api", "interface", "class", "function", "method", "module", "component"]
        technical_count = sum(1 for keyword in technical_keywords if keyword in synthesis.lower())
        if technical_count >= 3:
            score += 0.2
            details.append(f"✓ Contains technical details ({technical_count} keywords)")
        else:
            details.append(f"✗ Insufficient technical details ({technical_count} keywords)")

        # Check for dependencies
        if "depend" in synthesis.lower() or "require" in synthesis.lower():
            score += 0.2
            details.append("✓ Identifies dependencies")
        else:
            details.append("✗ Dependencies not clearly identified")

        # Check for resource requirements
        resource_keywords = ["time", "resource", "team", "skill", "infrastructure"]
        resource_count = sum(1 for keyword in resource_keywords if keyword in synthesis.lower())
        if resource_count >= 2:
            score += 0.2
            details.append(f"✓ Addresses resource requirements ({resource_count} aspects)")
        else:
            details.append(f"✗ Resource requirements unclear ({resource_count} aspects)")

        # Check for timeline/phases
        if "phase" in synthesis.lower() or "timeline" in synthesis.lower() or "milestone" in synthesis.lower():
            score += 0.2
            details.append("✓ Includes timeline or phases")
        else:
            details.append("✗ No timeline or phasing provided")

        metadata = {
            "technical_keyword_count": technical_count,
            "resource_keyword_count": resource_count,
            "synthesis_length": len(synthesis),
            "word_count": len(synthesis.split()),
        }

        return EvaluationResult(score=score, details="\n".join(details), metadata=metadata, timestamp=time.time())


class TicketCoverageEvaluator:
    """Evaluates how well the synthesis covers the original ticket requirements"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def evaluate(self, synthesis: str, context: dict[str, Any]) -> EvaluationResult:
        """
        Evaluate ticket coverage of a synthesis.

        Args:
            synthesis: The architecture synthesis to evaluate
            context: Must include 'integration_challenge' and optionally 'charter'

        Returns:
            Evaluation result with score and details
        """

        score = 0.0
        details = []
        metadata = {}

        integration_challenge = context.get("integration_challenge", "")
        charter = context.get("charter", "")

        if not integration_challenge:
            return EvaluationResult(
                score=0.0,
                details="No integration challenge provided for comparison",
                metadata={"error": "missing_integration_challenge"},
                timestamp=time.time(),
            )

        # Extract key terms from the challenge
        challenge_words = set(integration_challenge.lower().split())
        synthesis_words = set(synthesis.lower().split())

        # Remove common words
        common_words = {
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "can",
            "this",
            "that",
            "these",
            "those",
        }
        challenge_keywords = challenge_words - common_words
        synthesis_keywords = synthesis_words - common_words

        # Calculate keyword overlap
        overlap = challenge_keywords.intersection(synthesis_keywords)
        coverage_ratio = len(overlap) / len(challenge_keywords) if challenge_keywords else 0

        if coverage_ratio >= 0.7:
            score += 0.4
            details.append(f"✓ High keyword coverage ({coverage_ratio:.2f})")
        elif coverage_ratio >= 0.4:
            score += 0.2
            details.append(f"◐ Moderate keyword coverage ({coverage_ratio:.2f})")
        else:
            details.append(f"✗ Low keyword coverage ({coverage_ratio:.2f})")

        # Check for explicit requirement addressing
        requirement_indicators = ["requirement", "must", "shall", "need", "objective", "goal"]
        requirement_count = sum(1 for indicator in requirement_indicators if indicator in synthesis.lower())
        if requirement_count >= 2:
            score += 0.3
            details.append(f"✓ Addresses requirements explicitly ({requirement_count} indicators)")
        else:
            details.append(f"✗ Requirements not explicitly addressed ({requirement_count} indicators)")

        # Check for success criteria
        if "success" in synthesis.lower() or "criteria" in synthesis.lower() or "metric" in synthesis.lower():
            score += 0.3
            details.append("✓ Includes success criteria or metrics")
        else:
            details.append("✗ Missing success criteria or metrics")

        metadata = {
            "keyword_coverage_ratio": coverage_ratio,
            "overlapping_keywords": len(overlap),
            "total_challenge_keywords": len(challenge_keywords),
            "requirement_indicators": requirement_count,
            "challenge_length": len(integration_challenge),
            "synthesis_length": len(synthesis),
        }

        return EvaluationResult(score=score, details="\n".join(details), metadata=metadata, timestamp=time.time())


class StakeholderBalanceEvaluator:
    """Evaluates how well the synthesis balances different stakeholder perspectives"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def evaluate(self, synthesis: str, context: dict[str, Any]) -> EvaluationResult:
        """
        Evaluate stakeholder balance in a synthesis.

        Args:
            synthesis: The architecture synthesis to evaluate
            context: Must include 'stakeholder_contributions'

        Returns:
            Evaluation result with score and details
        """

        score = 0.0
        details = []
        metadata = {}

        stakeholder_contributions = context.get("stakeholder_contributions", {})

        if not stakeholder_contributions:
            return EvaluationResult(
                score=0.0,
                details="No stakeholder contributions provided for comparison",
                metadata={"error": "missing_stakeholder_contributions"},
                timestamp=time.time(),
            )

        stakeholder_names = list(stakeholder_contributions.keys())
        synthesis_lower = synthesis.lower()

        # Check for explicit stakeholder mentions
        mentioned_stakeholders = []
        for stakeholder in stakeholder_names:
            stakeholder_terms = stakeholder.replace("_", " ").split()
            if any(term in synthesis_lower for term in stakeholder_terms):
                mentioned_stakeholders.append(stakeholder)

        mention_ratio = len(mentioned_stakeholders) / len(stakeholder_names)

        if mention_ratio >= 0.8:
            score += 0.3
            details.append(f"✓ Most stakeholders mentioned ({mention_ratio:.2f})")
        elif mention_ratio >= 0.5:
            score += 0.15
            details.append(f"◐ Some stakeholders mentioned ({mention_ratio:.2f})")
        else:
            details.append(f"✗ Few stakeholders mentioned ({mention_ratio:.2f})")

        # Check for domain-specific keywords from each stakeholder
        domain_keywords = {
            "aider_integration": ["repomap", "editing", "validation", "git", "tool"],
            "context_engineering": ["memory", "context", "token", "cache", "optimization"],
            "langgraph_architecture": ["graph", "state", "orchestration", "coordination", "flow"],
            "production_stability": ["performance", "reliability", "monitoring", "error", "stability"],
            "developer_experience": ["api", "interface", "debugging", "documentation", "usability"],
        }

        domain_coverage = {}
        for stakeholder, keywords in domain_keywords.items():
            if stakeholder in stakeholder_names:
                covered_keywords = sum(1 for keyword in keywords if keyword in synthesis_lower)
                domain_coverage[stakeholder] = covered_keywords / len(keywords)

        avg_domain_coverage = sum(domain_coverage.values()) / len(domain_coverage) if domain_coverage else 0

        if avg_domain_coverage >= 0.6:
            score += 0.4
            details.append(f"✓ Good domain coverage ({avg_domain_coverage:.2f})")
        elif avg_domain_coverage >= 0.3:
            score += 0.2
            details.append(f"◐ Moderate domain coverage ({avg_domain_coverage:.2f})")
        else:
            details.append(f"✗ Poor domain coverage ({avg_domain_coverage:.2f})")

        # Check for conflict resolution
        conflict_indicators = ["trade-off", "balance", "compromise", "resolve", "integrate"]
        conflict_count = sum(1 for indicator in conflict_indicators if indicator in synthesis_lower)

        if conflict_count >= 2:
            score += 0.3
            details.append(f"✓ Addresses conflicts/trade-offs ({conflict_count} indicators)")
        else:
            details.append(f"✗ Limited conflict resolution ({conflict_count} indicators)")

        metadata = {
            "stakeholder_mention_ratio": mention_ratio,
            "mentioned_stakeholders": mentioned_stakeholders,
            "domain_coverage": domain_coverage,
            "avg_domain_coverage": avg_domain_coverage,
            "conflict_indicators": conflict_count,
            "total_stakeholders": len(stakeholder_names),
        }

        return EvaluationResult(score=score, details="\n".join(details), metadata=metadata, timestamp=time.time())


class CCEEvaluatorSuite:
    """Suite of CCE-specific evaluators for comprehensive assessment"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Initialize evaluators
        self.implementation_evaluator = ImplementationReadinessEvaluator()
        self.coverage_evaluator = TicketCoverageEvaluator()
        self.balance_evaluator = StakeholderBalanceEvaluator()

        # Initialize tool call validation evaluators
        try:
            from ..deep_agents.tool_call_evaluators import ToolCallValidationSuite

            self.tool_call_validation_suite = ToolCallValidationSuite()
            self.logger.info("Tool call validation evaluators initialized")
        except ImportError as e:
            self.logger.warning(f"Could not import tool call validation evaluators: {e}")
            self.tool_call_validation_suite = None

        self.logger.info("CCE Evaluator Suite initialized")

    def evaluate_synthesis(
        self,
        synthesis: str,
        integration_challenge: str,
        stakeholder_contributions: dict[str, list[str]],
        charter: str | None = None,
    ) -> dict[str, Any]:
        """
        Run complete evaluation suite on a synthesis.

        Args:
            synthesis: The synthesis to evaluate
            integration_challenge: Original integration challenge
            stakeholder_contributions: Stakeholder contributions
            charter: Optional charter

        Returns:
            Complete evaluation results
        """

        self.logger.info("Running complete evaluation suite")

        context = {
            "integration_challenge": integration_challenge,
            "stakeholder_contributions": stakeholder_contributions,
            "charter": charter,
        }

        # Run all evaluators
        implementation_result = self.implementation_evaluator.evaluate(synthesis, context)
        coverage_result = self.coverage_evaluator.evaluate(synthesis, context)
        balance_result = self.balance_evaluator.evaluate(synthesis, context)

        # Calculate weighted overall score
        weights = {"implementation_readiness": 0.4, "ticket_coverage": 0.35, "stakeholder_balance": 0.25}

        overall_score = (
            implementation_result.score * weights["implementation_readiness"]
            + coverage_result.score * weights["ticket_coverage"]
            + balance_result.score * weights["stakeholder_balance"]
        )

        # Compile results
        results = {
            "overall_score": overall_score,
            "implementation_readiness": {
                "score": implementation_result.score,
                "details": implementation_result.details,
                "metadata": implementation_result.metadata,
            },
            "ticket_coverage": {
                "score": coverage_result.score,
                "details": coverage_result.details,
                "metadata": coverage_result.metadata,
            },
            "stakeholder_balance": {
                "score": balance_result.score,
                "details": balance_result.details,
                "metadata": balance_result.metadata,
            },
            "evaluation_timestamp": time.time(),
            "synthesis_length": len(synthesis),
            "synthesis_word_count": len(synthesis.split()),
        }

        self.logger.info(f"Evaluation suite completed - Overall score: {overall_score:.3f}")

        return results

    def evaluate_tool_calls(
        self, tool_calls: list[dict[str, Any]], inputs: dict[str, Any] = None, outputs: dict[str, Any] = None
    ) -> dict[str, Any]:
        """
        Evaluate tool calls using the tool call validation suite.

        Args:
            tool_calls: List of tool call dictionaries
            inputs: Input context for evaluation
            outputs: System outputs for generation evaluation

        Returns:
            Tool call validation results
        """
        if not self.tool_call_validation_suite:
            return {
                "error": "Tool call validation suite not available",
                "score": 0.0,
                "details": "Tool call validation evaluators could not be initialized",
            }

        return self.tool_call_validation_suite.evaluate_tool_calls(tool_calls, inputs, outputs)

    def create_langsmith_evaluators(self) -> list[Any]:
        """
        Create LangSmith-compatible evaluators if LangSmith is available.

        Returns:
            List of LangSmith evaluators
        """

        if not LANGSMITH_AVAILABLE:
            self.logger.warning("LangSmith not available, cannot create LangSmith evaluators")
            return []

        evaluators = []

        # Implementation readiness evaluator
        def implementation_readiness_evaluator(run, example):
            outputs = run.outputs or {}
            synthesis = outputs.get("synthesis", "")
            context = outputs.get("context", {})
            result = self.implementation_evaluator.evaluate(synthesis, context)
            return {"key": "implementation_readiness", "score": result.score, "comment": result.details}

        # Ticket coverage evaluator
        def ticket_coverage_evaluator(run, example):
            outputs = run.outputs or {}
            synthesis = outputs.get("synthesis", "")
            context = outputs.get("context", {})
            result = self.coverage_evaluator.evaluate(synthesis, context)
            return {"key": "ticket_coverage", "score": result.score, "comment": result.details}

        # Stakeholder balance evaluator
        def stakeholder_balance_evaluator(run, example):
            outputs = run.outputs or {}
            synthesis = outputs.get("synthesis", "")
            context = outputs.get("context", {})
            result = self.balance_evaluator.evaluate(synthesis, context)
            return {"key": "stakeholder_balance", "score": result.score, "comment": result.details}

        try:
            # Create evaluator functions compatible with LangSmith
            evaluators = [implementation_readiness_evaluator, ticket_coverage_evaluator, stakeholder_balance_evaluator]
            self.logger.info(f"Created {len(evaluators)} LangSmith evaluators")
        except Exception as e:
            self.logger.error(f"Error creating LangSmith evaluators: {e}")

        return evaluators

    def run_langsmith_evaluation(self, dataset_name: str, experiment_name: str) -> dict[str, Any] | None:
        """
        Run evaluation using LangSmith dataset.

        Args:
            dataset_name: Name of the LangSmith dataset
            experiment_name: Name for the evaluation experiment

        Returns:
            Evaluation results if successful
        """

        if not LANGSMITH_AVAILABLE:
            self.logger.warning("LangSmith not available for dataset evaluation")
            return None

        try:
            # Get evaluators
            evaluators = self.create_langsmith_evaluators()

            if not evaluators:
                self.logger.error("No evaluators available for LangSmith evaluation")
                return None

            # Run evaluation against dataset
            results = evaluate(
                lambda inputs: {"synthesis": inputs.get("synthesis", ""), "context": inputs.get("context", {})},
                data=dataset_name,
                evaluators=evaluators,
                experiment_prefix=experiment_name,
            )

            self.logger.info(f"LangSmith evaluation completed: {experiment_name}")
            return results

        except Exception as e:
            self.logger.error(f"LangSmith evaluation failed: {e}")
            return None
