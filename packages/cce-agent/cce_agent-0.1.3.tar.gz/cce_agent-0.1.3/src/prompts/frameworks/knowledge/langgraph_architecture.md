<objective>
Provide reference guidance on LangGraph architecture patterns and capabilities.
</objective>

<behavioral_calibration>
<!-- Tone: Architectural, precise -->
<!-- Verbosity: Detailed but structured -->
<!-- Proactiveness: Moderate - highlight constraints -->
</behavioral_calibration>

<quick_start>
- Use this when designing or reviewing LangGraph integration work.
- Focus on state management, orchestration, and tool integration.
</quick_start>

<success_criteria>
- Architectural guidance aligns with LangGraph best practices.
</success_criteria>

<context>
# LangGraph Architecture Knowledge Base

## LangGraph Overview

LangGraph provides stateful workflows for LLM agents, enabling deterministic orchestration, tool integration, and checkpointing.

## Core Patterns

### State Management
- Use TypedDict state schemas for clarity and validation.
- Track messages and outputs explicitly.
- Keep state changes incremental and auditable.

### Graph Structure
- Separate planning and execution graphs where possible.
- Use clear node boundaries for tool orchestration.
- Prefer small, composable nodes.

### Tool Integration
- Expose tools through adapters that validate inputs and outputs.
- Separate planning tools from execution tools to reduce risk.
- Include validation nodes after significant actions.

### Checkpointing
- Use checkpointers to persist state across long runs.
- Ensure resumability and replayability where possible.
</context>

<decision_framework>
If a workflow step is ambiguous:
- Prefer explicit state transitions.
- Add validation nodes before irreversible actions.
- Keep node responsibilities narrow and testable.
</decision_framework>

<power_phrases>
- "This node should do one thing and emit a clear state update."
- "We need a validation step before proceeding."
</power_phrases>
