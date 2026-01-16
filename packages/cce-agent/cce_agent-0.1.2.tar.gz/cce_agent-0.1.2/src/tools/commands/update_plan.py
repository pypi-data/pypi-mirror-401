"""
Update Plan Command Implementation

This module provides programmatic access to the update_plan command
functionality as a LangChain tool, implementing the actual logic from
.cursor/commands/update_plan.md
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
async def update_plan(plan_file_path: str, update_type: str, additional_context: str | None = None) -> str:
    """
    Update existing implementation plans with new requirements, feedback,
    scope changes, or additional phases. This implements the actual update_plan
    command logic from .cursor/commands/update_plan.md

    Args:
        plan_file_path: Path to the plan file to update
        update_type: Type of update (requirements, feedback, scope, phases)
        additional_context: Additional context for the update

    Returns:
        Updated plan content or status message
    """
    try:
        # Import here to avoid circular imports
        from ..code_analyzer import CodeAnalyzer
        from ..shell_runner import ShellRunner
        from src.workspace_context import get_workspace_root

        # Initialize required services
        workspace_root = get_workspace_root() or "."
        shell_runner = ShellRunner(workspace_root)
        code_analyzer = CodeAnalyzer(shell_runner)

        # Phase 1: Plan Analysis
        plan_analysis = await _analyze_existing_plan(plan_file_path)
        if not plan_analysis["valid"]:
            return f"Plan analysis failed: {plan_analysis['error']}"

        # Phase 2: Update Processing
        update_result = await _process_plan_update(
            plan_analysis, update_type, additional_context, shell_runner, code_analyzer
        )

        # Phase 3: Plan Modification
        modification_result = await _modify_plan_content(plan_analysis, update_result)

        # Phase 4: Validation and Documentation
        validation_result = await _validate_updated_plan(modification_result, shell_runner)

        return f"""
Plan Update Results

Plan: {plan_file_path}
Update Type: {update_type}
Status: {modification_result["status"]}
Validation: {validation_result["status"]}

Details:
{modification_result.get("details", "")}
"""

    except Exception as e:
        logger.error(f"Update plan command failed: {e}")
        return f"Plan update failed: {str(e)}"


async def _analyze_existing_plan(plan_file_path: str) -> dict[str, Any]:
    """Analyze the existing plan file."""
    try:
        plan_file = Path(plan_file_path)
        if not plan_file.exists():
            return {"valid": False, "error": f"Plan file not found: {plan_file_path}"}

        # Read plan content
        with open(plan_file) as f:
            content = f.read()

        # Extract plan structure
        phases = []
        phase_pattern = r"### Phase (\d+): ([^\n]+)"
        for match in re.finditer(phase_pattern, content):
            phase_num = match.group(1)
            phase_name = match.group(2)
            phases.append({"number": phase_num, "name": phase_name})

        # Extract success criteria
        success_criteria = []
        criteria_pattern = r"- \[ \] ([^\n]+)"
        for match in re.finditer(criteria_pattern, content):
            success_criteria.append(match.group(1))

        # Extract completed items
        completed_items = []
        completed_pattern = r"- \[x\] ([^\n]+)"
        for match in re.finditer(completed_pattern, content):
            completed_items.append(match.group(1))

        return {
            "valid": True,
            "file_path": plan_file_path,
            "content": content,
            "phases": phases,
            "success_criteria": success_criteria,
            "completed_items": completed_items,
        }
    except Exception as e:
        return {"valid": False, "error": f"Plan analysis failed: {str(e)}"}


async def _process_plan_update(
    plan_analysis: dict[str, Any], update_type: str, additional_context: str | None, shell_runner, code_analyzer
) -> dict[str, Any]:
    """Process the plan update based on type."""
    try:
        update_result = {"type": update_type, "context": additional_context, "changes": []}

        if update_type == "requirements":
            # Add new requirements
            update_result["changes"].append("Added new requirements based on feedback")
            update_result["new_requirements"] = additional_context or "No specific requirements provided"

        elif update_type == "feedback":
            # Incorporate feedback
            update_result["changes"].append("Incorporated feedback into plan")
            update_result["feedback"] = additional_context or "No specific feedback provided"

        elif update_type == "scope":
            # Update scope
            update_result["changes"].append("Updated project scope")
            update_result["scope_changes"] = additional_context or "No specific scope changes provided"

        elif update_type == "phases":
            # Add or modify phases
            update_result["changes"].append("Updated implementation phases")
            update_result["phase_changes"] = additional_context or "No specific phase changes provided"

        else:
            # Generic update
            update_result["changes"].append(f"Applied {update_type} update")
            update_result["generic_update"] = additional_context or "No specific update details provided"

        return update_result
    except Exception as e:
        return {"error": f"Update processing failed: {str(e)}"}


async def _modify_plan_content(plan_analysis: dict[str, Any], update_result: dict[str, Any]) -> dict[str, Any]:
    """Modify the plan content based on the update."""
    try:
        original_content = plan_analysis["content"]
        update_type = update_result["type"]

        # Create updated content
        updated_content = original_content

        # Add update section
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_section = f"""

## Plan Updates

### Update: {update_type.title()} - {timestamp}

**Update Type**: {update_type}
**Context**: {update_result.get("context", "No additional context provided")}

**Changes Made**:
{chr(10).join(f"- {change}" for change in update_result.get("changes", []))}

**Details**:
"""

        # Add specific details based on update type
        if update_type == "requirements" and "new_requirements" in update_result:
            update_section += f"\n**New Requirements**:\n{update_result['new_requirements']}\n"
        elif update_type == "feedback" and "feedback" in update_result:
            update_section += f"\n**Feedback Incorporated**:\n{update_result['feedback']}\n"
        elif update_type == "scope" and "scope_changes" in update_result:
            update_section += f"\n**Scope Changes**:\n{update_result['scope_changes']}\n"
        elif update_type == "phases" and "phase_changes" in update_result:
            update_section += f"\n**Phase Changes**:\n{update_result['phase_changes']}\n"
        else:
            update_section += (
                f"\n**Update Details**:\n{update_result.get('generic_update', 'No specific details provided')}\n"
            )

        # Insert update section before the last section
        if "## References" in updated_content:
            updated_content = updated_content.replace("## References", update_section + "\n## References")
        else:
            updated_content += update_section

        # Write updated content back to file
        with open(plan_analysis["file_path"], "w") as f:
            f.write(updated_content)

        return {
            "status": "Plan updated successfully",
            "details": f"Updated {update_type} in plan file",
            "updated_content": updated_content,
        }
    except Exception as e:
        return {"status": f"Plan modification failed: {str(e)}"}


async def _validate_updated_plan(modification_result: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Validate the updated plan."""
    try:
        # Check if file was written successfully
        if "updated_content" in modification_result:
            # Basic validation - check if content is not empty
            content = modification_result["updated_content"]
            if len(content.strip()) < 100:
                return {"status": "Warning: Updated plan content seems too short"}

            # Check for required sections
            required_sections = ["## Overview", "## Implementation Phases"]
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)

            if missing_sections:
                return {"status": f"Warning: Missing required sections: {', '.join(missing_sections)}"}

            return {"status": "Plan validation passed"}
        else:
            return {"status": "Plan validation failed - no updated content"}
    except Exception as e:
        return {"status": f"Plan validation failed: {str(e)}"}
