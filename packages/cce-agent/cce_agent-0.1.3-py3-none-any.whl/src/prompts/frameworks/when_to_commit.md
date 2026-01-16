<objective>
Decide when to commit changes during an implementation cycle.
</objective>

<behavioral_calibration>
<!-- Tone: Disciplined, cautious -->
<!-- Verbosity: Brief decision with rationale -->
<!-- Proactiveness: Moderate - commit when stable -->
</behavioral_calibration>

<quick_start>
- Commit after a coherent, tested change set.
- Avoid committing partial or unvalidated work.
- Keep commits focused and reversible.
</quick_start>

<success_criteria>
- Commits are small, tested, and aligned with plan items.
</success_criteria>

<decision_criteria>
Commit when:
- A plan item is fully complete.
- Linting and relevant tests pass.
- The change set is cohesive and reviewable.

Do not commit when:
- Tests are failing or unrun.
- The change set mixes unrelated concerns.
- The plan item is still in progress.
</decision_criteria>

<examples>
<example>
<input>Completed lint fixes and tests are green</input>
<output>Commit with a focused message referencing the ticket</output>
</example>
<example>
<input>Halfway through a refactor</input>
<output>Do not commit yet</output>
</example>
</examples>

<power_phrases>
- "This change is complete and validated, so I can commit."
- "This is still in progress, so I should hold the commit."
</power_phrases>
