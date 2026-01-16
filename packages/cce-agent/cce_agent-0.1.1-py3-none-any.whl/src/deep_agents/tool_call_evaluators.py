"""
Tool Call Validation Evaluators

Heuristic evaluators for validating tool calls in the CCE Deep Agent system.
These evaluators provide fast, deterministic validation of tool call parameters
and generation quality, following LangSmith evaluation patterns.
"""

import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

try:
    from langsmith import Client
    from langsmith.evaluation import StringEvaluator, evaluate

    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    logging.warning("LangSmith not available. Install langsmith package for advanced evaluators.")


@dataclass
class ToolCallValidationResult:
    """Result of a tool call validation evaluation"""

    score: float
    details: str
    metadata: dict[str, Any]
    timestamp: float
    validation_errors: list[str]
    passed_checks: list[str]


class ToolCallParameterEvaluator:
    """Heuristic evaluator for tool call parameter validation"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Define required parameters for each tool
        self.tool_requirements = {
            "write_file": {
                "required": ["file_path", "content"],
                "optional": ["state", "tool_call_id"],
                "validation_rules": {"content": lambda x: x is not None and isinstance(x, str) and x.strip() != ""},
            },
            "hybrid_write_file": {
                "required": ["file_path", "content"],
                "optional": ["state", "tool_call_id"],
                "validation_rules": {"content": lambda x: x is not None and isinstance(x, str) and x.strip() != ""},
            },
            "edit_file": {
                "required": ["file_path", "old_string", "new_string"],
                "optional": ["state", "tool_call_id", "replace_all"],
                "validation_rules": {
                    "old_string": lambda x: x is not None and isinstance(x, str),
                    "new_string": lambda x: x is not None and isinstance(x, str),
                },
            },
            "hybrid_edit_file": {
                "required": ["file_path", "old_string", "new_string"],
                "optional": ["state", "tool_call_id", "replace_all"],
                "validation_rules": {
                    "old_string": lambda x: x is not None and isinstance(x, str),
                    "new_string": lambda x: x is not None and isinstance(x, str),
                },
            },
            "execute_bash_command": {
                "required": ["command"],
                "optional": ["timeout"],
                "validation_rules": {"command": lambda x: x is not None and isinstance(x, str) and x.strip() != ""},
            },
        }

    def evaluate(self, tool_calls: list[dict[str, Any]], context: dict[str, Any] = None) -> ToolCallValidationResult:
        """
        Evaluate tool call parameters using heuristic rules.

        Args:
            tool_calls: List of tool call dictionaries
            context: Additional context for evaluation

        Returns:
            Tool call validation result with score and details
        """
        validation_errors = []
        passed_checks = []
        total_score = 0.0
        total_checks = 0

        if not tool_calls:
            return ToolCallValidationResult(
                score=0.0,
                details="No tool calls provided for validation",
                metadata={"error": "no_tool_calls"},
                timestamp=time.time(),
                validation_errors=["No tool calls provided"],
                passed_checks=[],
            )

        for i, tool_call in enumerate(tool_calls):
            tool_name = tool_call.get("name", f"unknown_tool_{i}")
            tool_args = tool_call.get("args", {})

            if tool_name not in self.tool_requirements:
                validation_errors.append(f"Unknown tool: {tool_name}")
                continue

            requirements = self.tool_requirements[tool_name]

            # Check required parameters
            for param in requirements["required"]:
                total_checks += 1
                if param not in tool_args:
                    validation_errors.append(f"Tool {tool_name} missing required parameter: {param}")
                else:
                    passed_checks.append(f"Tool {tool_name} has required parameter: {param}")
                    total_score += 1.0

                    # Apply validation rules if they exist
                    if param in requirements["validation_rules"]:
                        validation_rule = requirements["validation_rules"][param]
                        try:
                            if not validation_rule(tool_args[param]):
                                validation_errors.append(f"Tool {tool_name} parameter {param} failed validation rule")
                            else:
                                passed_checks.append(f"Tool {tool_name} parameter {param} passed validation rule")
                        except Exception as e:
                            validation_errors.append(f"Tool {tool_name} parameter {param} validation error: {str(e)}")

            # Check for unexpected parameters (warn but don't fail)
            for param in tool_args:
                if param not in requirements["required"] and param not in requirements["optional"]:
                    validation_errors.append(f"Tool {tool_name} has unexpected parameter: {param}")

        # Calculate final score
        final_score = total_score / total_checks if total_checks > 0 else 0.0

        # Generate details
        details_parts = []
        if validation_errors:
            details_parts.append(f"Validation Errors ({len(validation_errors)}):")
            for error in validation_errors:
                details_parts.append(f"  - {error}")

        if passed_checks:
            details_parts.append(f"Passed Checks ({len(passed_checks)}):")
            for check in passed_checks:
                details_parts.append(f"  ✓ {check}")

        details = "\n".join(details_parts) if details_parts else "No validation performed"

        return ToolCallValidationResult(
            score=final_score,
            details=details,
            metadata={
                "total_tool_calls": len(tool_calls),
                "total_checks": total_checks,
                "validation_errors_count": len(validation_errors),
                "passed_checks_count": len(passed_checks),
            },
            timestamp=time.time(),
            validation_errors=validation_errors,
            passed_checks=passed_checks,
        )


class ToolCallGenerationEvaluator:
    """Evaluator for testing tool call generation from prompts"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.parameter_evaluator = ToolCallParameterEvaluator()

    def evaluate(
        self, inputs: dict[str, Any], outputs: dict[str, Any], reference_outputs: dict[str, Any] = None
    ) -> ToolCallValidationResult:
        """
        Evaluate tool call generation from prompt outputs.

        Args:
            inputs: Input to the system (e.g., user prompt)
            outputs: System outputs (should contain tool_calls)
            reference_outputs: Reference outputs for comparison

        Returns:
            Tool call generation validation result
        """
        # Extract tool calls from outputs
        tool_calls = []

        # Handle different output formats
        if "tool_calls" in outputs:
            tool_calls = outputs["tool_calls"]
        elif "messages" in outputs and isinstance(outputs["messages"], list):
            # Extract tool calls from messages
            for message in outputs["messages"]:
                if isinstance(message, dict) and "tool_calls" in message:
                    tool_calls.extend(message["tool_calls"])
                elif hasattr(message, "tool_calls") and message.tool_calls:
                    tool_calls.extend(message.tool_calls)

        # Use parameter evaluator to validate tool calls
        parameter_result = self.parameter_evaluator.evaluate(tool_calls, inputs)

        # Add generation-specific validation
        generation_errors = []
        generation_passed = []

        # Check if tool calls were generated when expected
        user_input = inputs.get("question", inputs.get("prompt", str(inputs)))
        if any(keyword in user_input.lower() for keyword in ["create", "write", "edit", "modify", "add", "remove"]):
            if not tool_calls:
                generation_errors.append("Expected tool calls for file operation request but none were generated")
            else:
                generation_passed.append("Tool calls generated for file operation request")

        # Check tool call appropriateness
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.get("name", "unknown")
                if tool_name in ["write_file", "edit_file", "hybrid_write_file", "hybrid_edit_file"]:
                    if "file" not in user_input.lower() and "code" not in user_input.lower():
                        generation_errors.append(f"Tool {tool_name} used but no file operation mentioned in input")
                    else:
                        generation_passed.append(f"Tool {tool_name} appropriately used for file operation")

        # Combine results
        all_errors = parameter_result.validation_errors + generation_errors
        all_passed = parameter_result.passed_checks + generation_passed

        # Adjust score based on generation quality
        generation_score = 1.0 if not generation_errors else 0.5
        final_score = (parameter_result.score + generation_score) / 2.0

        # Generate combined details
        details_parts = []
        if all_errors:
            details_parts.append(f"Validation Errors ({len(all_errors)}):")
            for error in all_errors:
                details_parts.append(f"  - {error}")

        if all_passed:
            details_parts.append(f"Passed Checks ({len(all_passed)}):")
            for check in all_passed:
                details_parts.append(f"  ✓ {check}")

        details = "\n".join(details_parts) if details_parts else "No validation performed"

        return ToolCallValidationResult(
            score=final_score,
            details=details,
            metadata={
                **parameter_result.metadata,
                "generation_errors_count": len(generation_errors),
                "generation_passed_count": len(generation_passed),
                "user_input": user_input,
            },
            timestamp=time.time(),
            validation_errors=all_errors,
            passed_checks=all_passed,
        )


class ToolCallValidationSuite:
    """Suite of tool call validation evaluators for comprehensive assessment"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Initialize evaluators
        self.parameter_evaluator = ToolCallParameterEvaluator()
        self.generation_evaluator = ToolCallGenerationEvaluator()

        self.logger.info("Tool Call Validation Suite initialized")

    def evaluate_tool_calls(
        self, tool_calls: list[dict[str, Any]], inputs: dict[str, Any] = None, outputs: dict[str, Any] = None
    ) -> dict[str, Any]:
        """
        Run complete tool call validation suite.

        Args:
            tool_calls: List of tool call dictionaries
            inputs: Input context for evaluation
            outputs: System outputs for generation evaluation

        Returns:
            Complete validation results
        """

        self.logger.info("Running complete tool call validation suite")

        # Run parameter validation
        parameter_result = self.parameter_evaluator.evaluate(tool_calls, inputs or {})

        # Run generation validation if outputs provided
        generation_result = None
        if outputs:
            generation_result = self.generation_evaluator.evaluate(inputs or {}, outputs)

        # Calculate weighted overall score
        if generation_result:
            weights = {"parameter_validation": 0.6, "generation_validation": 0.4}

            overall_score = (
                parameter_result.score * weights["parameter_validation"]
                + generation_result.score * weights["generation_validation"]
            )
        else:
            overall_score = parameter_result.score

        # Compile results
        results = {
            "overall_score": overall_score,
            "parameter_validation": {
                "score": parameter_result.score,
                "details": parameter_result.details,
                "metadata": parameter_result.metadata,
                "errors": parameter_result.validation_errors,
                "passed": parameter_result.passed_checks,
            },
        }

        if generation_result:
            results["generation_validation"] = {
                "score": generation_result.score,
                "details": generation_result.details,
                "metadata": generation_result.metadata,
                "errors": generation_result.validation_errors,
                "passed": generation_result.passed_checks,
            }

        self.logger.info(f"Tool call validation completed. Overall score: {overall_score:.3f}")

        return results

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

        # Parameter validation evaluator
        def parameter_validation_evaluator(run, example):
            outputs = run.outputs or {}
            tool_calls = outputs.get("tool_calls", [])
            result = self.parameter_evaluator.evaluate(tool_calls, example.inputs)
            return {"key": "tool_call_parameter_validation", "score": result.score, "comment": result.details}

        # Generation validation evaluator
        def generation_validation_evaluator(run, example):
            outputs = run.outputs or {}
            result = self.generation_evaluator.evaluate(example.inputs, outputs)
            return {"key": "tool_call_generation_validation", "score": result.score, "comment": result.details}

        try:
            # Create evaluator functions compatible with LangSmith
            evaluators.extend([parameter_validation_evaluator, generation_validation_evaluator])

            self.logger.info(f"Created {len(evaluators)} LangSmith-compatible evaluators")

        except Exception as e:
            self.logger.error(f"Error creating LangSmith evaluators: {e}")

        return evaluators


# Global instance for easy access
_tool_call_validation_suite: ToolCallValidationSuite | None = None


def get_tool_call_validation_suite() -> ToolCallValidationSuite:
    """Get the global tool call validation suite instance."""
    global _tool_call_validation_suite
    if _tool_call_validation_suite is None:
        _tool_call_validation_suite = ToolCallValidationSuite()
    return _tool_call_validation_suite
