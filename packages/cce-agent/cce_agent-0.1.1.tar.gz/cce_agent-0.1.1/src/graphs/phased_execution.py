"""
Phased Execution with Structured Outputs for LangGraph

This module provides structured phase parsing and execution with proper
LangGraph state management and structured outputs.
"""

import re
from typing import Any

from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class PlanPhase(BaseModel):
    """Structured representation of a plan phase."""

    phase_number: int = Field(description="The phase number (1, 2, 3, etc.)")
    phase_name: str = Field(description="The name/title of the phase")
    description: str = Field(description="Description of what this phase accomplishes")
    tasks: list[str] = Field(description="List of tasks to be completed in this phase")
    deliverables: list[str] = Field(description="Expected deliverables from this phase")
    acceptance_criteria: list[str] = Field(description="Criteria to validate phase completion")


class PhaseExecutionResult(BaseModel):
    """Structured result of executing a single phase."""

    phase_number: int
    phase_name: str
    success: bool
    execution_summary: str = Field(description="Summary of what was accomplished")
    files_modified: list[str] = Field(description="List of files that were modified")
    deliverables_created: list[str] = Field(description="Deliverables that were actually created")
    issues_encountered: list[str] = Field(default_factory=list, description="Any issues or blockers")
    next_phase_notes: str = Field(default="", description="Important notes for the next phase")


class PhasedExecutionState(TypedDict):
    """Extended state for phased execution."""

    # Original state fields
    instruction: str
    target_files: list[str]

    # Phased execution fields
    use_phased_execution: bool
    plan_content: str
    parsed_phases: list[dict[str, Any]]  # Will contain PlanPhase.dict() representations
    current_phase_index: int
    completed_phases: list[dict[str, Any]]  # Will contain PhaseExecutionResult.dict() representations
    phase_execution_summary: str

    # Standard state fields
    error_message: str | None
    patch_preview_path: str | None


def parse_plan_to_phases(plan_content: str) -> list[PlanPhase]:
    """
    Parse a plan document into structured PlanPhase objects.

    Returns:
        List of PlanPhase objects with structured data
    """
    phases = []
    lines = plan_content.split("\n")

    current_phase_data = None
    current_section = None
    phase_number = 0

    for line in lines:
        line = line.strip()

        # Match phase headers like "### Phase 1: Core Mode Infrastructure"
        phase_match = re.match(r"^### Phase \d+: (.+)", line)
        if phase_match:
            # Save previous phase if exists
            if current_phase_data:
                phases.append(PlanPhase(**current_phase_data))

            # Start new phase
            phase_number += 1
            phase_name = phase_match.group(1)
            current_phase_data = {
                "phase_number": phase_number,
                "phase_name": phase_name,
                "description": "",
                "tasks": [],
                "deliverables": [],
                "acceptance_criteria": [],
            }
            current_section = None
            continue

        # Skip if no current phase
        if not current_phase_data:
            continue

        # Match section headers
        if line.startswith("**Description**:"):
            current_section = "description"
            continue
        elif line.startswith("**Tasks**:"):
            current_section = "tasks"
            continue
        elif line.startswith("**Deliverables**:"):
            current_section = "deliverables"
            continue
        elif line.startswith("**Acceptance Criteria**:"):
            current_section = "acceptance_criteria"
            continue

        # Parse content based on current section
        if current_section == "description" and line and not line.startswith("**"):
            current_phase_data["description"] = line

        elif current_section == "tasks":
            # Match task items like "- [ ] Task description"
            task_match = re.match(r"^- \[([ x])\] (.+)", line)
            if task_match:
                description = task_match.group(2)
                current_phase_data["tasks"].append(description)

        elif current_section == "deliverables":
            # Match deliverable items like "- Deliverable description"
            if line.startswith("- ") and not line.startswith("- [ ]"):
                deliverable = line[2:]  # Remove "- " prefix
                current_phase_data["deliverables"].append(deliverable)

        elif current_section == "acceptance_criteria":
            # Match criteria items like "- [ ] Criteria description"
            criteria_match = re.match(r"^- \[([ x])\] (.+)", line)
            if criteria_match:
                criteria = criteria_match.group(2)
                current_phase_data["acceptance_criteria"].append(criteria)

    # Don't forget the last phase
    if current_phase_data:
        phases.append(PlanPhase(**current_phase_data))

    return phases


def create_phase_instruction(phase: PlanPhase, target_files: list[str]) -> str:
    """Create a structured aider instruction for a single phase."""

    instruction = f"""
PHASE {phase.phase_number}: {phase.phase_name.upper()}

DESCRIPTION: {phase.description}

TARGET FILES: {", ".join(target_files)}

TASKS TO IMPLEMENT:
"""

    for task in phase.tasks:
        instruction += f"🔲 {task}\n"

    if phase.deliverables:
        instruction += f"""
DELIVERABLES EXPECTED:
"""
        for deliverable in phase.deliverables:
            instruction += f"• {deliverable}\n"

    if phase.acceptance_criteria:
        instruction += f"""
ACCEPTANCE CRITERIA:
"""
        for criteria in phase.acceptance_criteria:
            instruction += f"✓ {criteria}\n"

    instruction += f"""
IMPLEMENTATION FOCUS:
- Focus ONLY on the tasks for this phase
- Ensure all deliverables are created/implemented  
- Meet all acceptance criteria before considering phase complete
- Follow existing code patterns and architecture
- Add necessary imports and dependencies
- Create clean, testable, and maintainable code

STRUCTURED OUTPUT REQUIRED:
After implementing this phase, provide a structured summary including:
1. What was accomplished in this phase
2. Which files were modified
3. Which deliverables were actually created
4. Any issues or blockers encountered
5. Important notes for the next phase
"""

    return instruction.strip()


class PhaseExecutionPrompt(BaseModel):
    """Structured prompt for phase execution with aider."""

    phase: PlanPhase
    target_files: list[str]
    previous_phase_notes: str = ""

    def to_instruction(self) -> str:
        """Convert to aider instruction string."""
        base_instruction = create_phase_instruction(self.phase, self.target_files)

        if self.previous_phase_notes:
            base_instruction += f"""

CONTEXT FROM PREVIOUS PHASE:
{self.previous_phase_notes}
"""

        return base_instruction


def create_phased_execution_state(instruction: str, target_files: list[str], plan_content: str) -> PhasedExecutionState:
    """
    Create initial state for phased execution.

    Args:
        instruction: The main implementation instruction
        target_files: Files to be modified
        plan_content: The plan document content

    Returns:
        Structured state ready for phased execution
    """

    # Parse phases from plan
    phases = parse_plan_to_phases(plan_content)

    return PhasedExecutionState(
        instruction=instruction,
        target_files=target_files,
        use_phased_execution=True,
        plan_content=plan_content,
        parsed_phases=[phase.model_dump() for phase in phases],
        current_phase_index=0,
        completed_phases=[],
        phase_execution_summary="",
        error_message=None,
        patch_preview_path=None,
    )


def get_current_phase(state: PhasedExecutionState) -> PlanPhase | None:
    """Get the current phase to execute."""
    if state["current_phase_index"] >= len(state["parsed_phases"]):
        return None

    phase_dict = state["parsed_phases"][state["current_phase_index"]]
    return PlanPhase(**phase_dict)


def get_previous_phase_notes(state: PhasedExecutionState) -> str:
    """Get notes from the previous phase for context."""
    if not state["completed_phases"]:
        return ""

    last_phase = state["completed_phases"][-1]
    return last_phase.get("next_phase_notes", "")


# Example usage for testing
if __name__ == "__main__":
    # Test with the actual plan file
    with open(
        "docs/context_engineering/plans/2025-09-13_124915_plan_add_configurable_run_modes__demo_guided_expert_.md"
    ) as f:
        plan_content = f.read()

    # Parse phases
    phases = parse_plan_to_phases(plan_content)

    print(f"📋 Parsed {len(phases)} structured phases:")
    for phase in phases:
        print(f"  Phase {phase.phase_number}: {phase.phase_name}")
        print(f"    Description: {phase.description}")
        print(f"    Tasks: {len(phase.tasks)}")
        print(f"    Deliverables: {len(phase.deliverables)}")
        print(f"    Acceptance Criteria: {len(phase.acceptance_criteria)}")

    # Create structured state
    target_files = ["src/config.py", "src/agent.py", "src/run_modes.py"]
    state = create_phased_execution_state("Implement configurable run modes", target_files, plan_content)

    print(f"\n🏗️  Created structured state:")
    print(f"  Total phases: {len(state['parsed_phases'])}")
    print(f"  Current phase index: {state['current_phase_index']}")
    print(f"  Use phased execution: {state['use_phased_execution']}")

    # Get current phase
    current_phase = get_current_phase(state)
    if current_phase:
        print(f"\n🎯 Current phase: {current_phase.phase_name}")

        # Create structured prompt
        prompt = PhaseExecutionPrompt(phase=current_phase, target_files=target_files)

        print(f"\n📝 Structured instruction preview:")
        print("=" * 60)
        print(prompt.to_instruction()[:500] + "...")
        print("=" * 60)
