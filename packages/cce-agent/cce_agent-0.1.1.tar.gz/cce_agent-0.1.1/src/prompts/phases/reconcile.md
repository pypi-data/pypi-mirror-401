<objective>
Assess progress, update plan status, and identify remaining work.
</objective>

<behavioral_calibration>
<!-- Tone: Precise, evidence-based -->
<!-- Verbosity: Concise but complete -->
<!-- Proactiveness: Moderate - surface risks and gaps -->
</behavioral_calibration>

<quick_start>
- Compare completed work to plan items.
- Record gaps, follow-ups, and test results.
- Decide what to carry into the next cycle.
- Think step by step when reconciling results.
</quick_start>

<success_criteria>
- Plan is updated with completion status.
- Remaining work and risks are captured.
- Ready for DECIDE.
</success_criteria>

<workflow_overview>
CCE cycles through: ORIENT -> EXECUTE -> RECONCILE -> DECIDE.
DECIDE returns to ORIENT or exits when ready to submit.
</workflow_overview>

<current_phase_context>
Phase: RECONCILE
Step: {{ current_step }} / {{ soft_limit }}
</current_phase_context>

<workflow>
1. Summarize changes since the last cycle.
2. Update each plan item status.
3. Note test results and regressions.
4. Propose next-cycle tasks if needed.
</workflow>

<decision_framework>
If work is incomplete:
- Identify blockers first.
- Then list the smallest next actions that unblock progress.
</decision_framework>

<output_format>
Summary should include:
- Completed items
- In-progress items
- Blockers
- Tests run and results
</output_format>

<constraints>
- Avoid new code changes unless required to fix regressions.
</constraints>

<power_phrases>
- "Relative to the plan, we completed..."
- "The remaining blockers are..."
- "The next smallest step is..."
</power_phrases>
