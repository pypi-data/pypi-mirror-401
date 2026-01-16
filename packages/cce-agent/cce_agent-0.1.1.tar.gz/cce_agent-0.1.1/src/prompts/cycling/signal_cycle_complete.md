<objective>
Emit a cycle-complete signal with a concise summary and next-step guidance.
</objective>

<behavioral_calibration>
<!-- Tone: Clear, concise -->
<!-- Verbosity: Brief but complete -->
<!-- Proactiveness: High - give explicit next steps -->
</behavioral_calibration>

<quick_start>
- Call signal_cycle_complete when stopping or the soft limit triggers.
- Provide all required fields with concise, actionable content.
- List changed artifacts and any tests or issues.
</quick_start>

<success_criteria>
- signal_cycle_complete is called with all required fields.
- Summary and next focus are specific and actionable.
</success_criteria>

<workflow>
When you reach a natural stopping point or the soft limit is triggered, call
signal_cycle_complete with:
- summary: {{ summary }}
- work_remaining: {{ work_remaining }}
- next_focus: {{ next_focus }}
- tests_run: {{ tests_run }}
- issues_found: {{ issues_found }}
- artifacts: {{ artifacts }}
</workflow>

<output_format>
Example call payload:
summary: "Completed prompt updates for cycling and guardrail phases."
work_remaining: "Update stakeholder prompts and add prompt checklist."
next_focus: "Apply calibration to stakeholder prompts, then add test report doc."
tests_run: "Not run"
issues_found: "None"
artifacts: "src/prompts/cycling/orientation.md, src/prompts/cycling/wrap_up.md"
</output_format>

<power_phrases>
- "This cycle is complete because..."
- "The next focus should be..."
</power_phrases>
