<objective>
Decide what tests to run and when.
</objective>

<behavioral_calibration>
<!-- Tone: Careful, quality-focused -->
<!-- Verbosity: Concise but explicit -->
<!-- Proactiveness: High for validation -->
</behavioral_calibration>

<quick_start>
- Run the smallest test set that validates the change.
- Expand scope when changes affect shared behavior.
- Always run full tests before final submission.
</quick_start>

<success_criteria>
- Tests provide confidence in the change without excessive runtime.
</success_criteria>

<decision_criteria>
Run targeted tests when:
- Changes are localized to a single file or module.
- There is a clear test covering the change.

Run broader tests when:
- Changes affect shared utilities or core workflows.
- Multiple modules or subsystems are touched.

Run full suite when:
- Preparing final submission.
- There were previous failures or regressions.
</decision_criteria>

<examples>
<example>
<input>Change in src/tools/git_ops.py</input>
<output>run_tests(test_pattern="git_ops")</output>
</example>
<example>
<input>Refactor across multiple modules</input>
<output>run_tests()</output>
</example>
</examples>

<power_phrases>
- "This change is localized, so targeted tests are sufficient."
- "Because this touches shared code, I should expand coverage."
</power_phrases>
