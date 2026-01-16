<objective>
Orient the agent at the start of an execution cycle with a focused objective and actionable context.
</objective>

<behavioral_calibration>
<!-- Tone: Focused, action-oriented -->
<!-- Verbosity: Concise orientation (1-3 sentences) -->
<!-- Proactiveness: High - provide clear direction -->
</behavioral_calibration>

<quick_start>
- Focus on {{ focus }} and {{ focus_description }}.
- Think step by step about the best approach for this cycle.
- Use plan context and relevant items/files to guide actions.
- Honor constraints and success criteria for this cycle.
</quick_start>

<success_criteria>
- Orientation states a clear, actionable focus for the cycle.
- Provided context is sufficient to act without ambiguity.
- Agent understands what "done" looks like for this cycle.
</success_criteria>

<workflow>
## Orientation Process

1. **Review** the context below carefully
2. **Identify** the most important focus if not already specified
3. **Think** step by step about the approach
4. **Respond** with a concise orientation statement (1-3 sentences)

Your orientation MUST include:
- What you will focus on this cycle
- Why this focus is the right priority
- How you will know when you're done
</workflow>

<context>
## Cycle Information

**Cycle:** {{ cycle_number }} of {{ max_cycles }}

## Current Objective

**Focus:** {{ focus }}
**Description:** {{ focus_description }}

## Plan Context

{{ plan_summary }}

## Relevant Plan Items

{{ relevant_plan_items }}

## Relevant Files

{{ relevant_files }}

## Recent Changes

{{ recent_changes }}

## Previous Cycle Summary

{{ previous_cycle_summary }}

## Previous Suggestion

{{ previous_suggestion }}

## Constraints / Risks

{{ constraints }}

## Success Criteria for This Cycle

{{ cycle_success_criteria }}

## Suggested Approach

{{ suggested_approach }}

## Memory-Driven Context

{{ memory_context }}

## Intelligent Context

{{ intelligent_context }}
</context>

<decision_framework>
## Choosing Your Focus

If the focus is unclear, prioritize:

```
1. Unresolved blockers from previous cycle
2. Critical path items from the plan
3. Items with dependencies on them
4. Items that validate previous work
5. Items that reduce risk/uncertainty
```
</decision_framework>

<orientation_format>
## Your Orientation Should Follow This Pattern

```
This cycle, I will [SPECIFIC ACTION] because [REASON].

My approach:
1. [First step]
2. [Second step]  
3. [Validation step]

Done when: [CONCRETE COMPLETION CRITERIA]
```
</orientation_format>

<power_phrases>
Use these reasoning triggers:
- "Given the previous cycle's outcome, I should prioritize..."
- "The critical path requires me to focus on..."
- "Before I can proceed with X, I must first..."
- "The biggest risk right now is... so I will address..."
</power_phrases>

<anti_patterns>
## Avoid These Orientation Mistakes

❌ **Vague**: "I will work on the code."
✅ **Specific**: "I will implement the `validate_input` function in `src/utils.py`."

❌ **No completion criteria**: "I will fix the bug."
✅ **Clear done state**: "I will fix the bug and verify with `pytest test_module.py`."

❌ **Ignoring context**: Starting fresh without reading previous cycle.
✅ **Building on context**: "Building on the previous cycle's foundation..."
</anti_patterns>
