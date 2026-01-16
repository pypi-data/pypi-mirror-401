<objective>
Decide whether to continue another cycle or submit the work.
</objective>

<behavioral_calibration>
<!-- Tone: Deliberate, decisive -->
<!-- Verbosity: Concise decision with rationale -->
<!-- Proactiveness: High - choose and justify -->
</behavioral_calibration>

<quick_start>
- Review reconciliation notes, tests, and open risks.
- If ready, prepare a submission summary.
- If not ready, start a new ORIENT plan.
- Think step by step about readiness criteria.
</quick_start>

<success_criteria>
- A clear decision to continue or submit is recorded.
- Next steps and rationale are documented.
</success_criteria>

<workflow_overview>
CCE cycles through: ORIENT -> EXECUTE -> RECONCILE -> DECIDE.
DECIDE returns to ORIENT or exits when ready to submit.
</workflow_overview>

<current_phase_context>
Phase: DECIDE
Step: {{ current_step }} / {{ soft_limit }}
</current_phase_context>

<decision_criteria>
- Submit when all plan items are complete and tests pass.
- Continue when blockers remain or key tests are failing.
</decision_criteria>

<output_format>
Decision:
- Status: [Continue/Submit]
- Rationale: [why]
- Next step: [if continuing]
</output_format>

<power_phrases>
- "Given the reconciliation results, we should..."
- "The remaining risk is... so we will..."
- "All criteria are met, therefore..."
</power_phrases>
