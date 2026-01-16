<objective>
Summarize work completed in the cycle and provide actionable recommendations for next steps.
</objective>

<behavioral_calibration>
<!-- Tone: Reflective, forward-looking -->
<!-- Verbosity: Comprehensive summary, specific recommendations -->
<!-- Proactiveness: High - provide clear next steps -->
</behavioral_calibration>

<quick_start>
- List ALL completed work, artifacts, tests, and issues.
- State what remains with clear priority order.
- Provide an explicit, actionable next focus recommendation.
- Be honest about blockers and risks.
</quick_start>

<success_criteria>
- Summary completely covers work done this cycle.
- Remaining work is clear and prioritized.
- Next focus is specific and immediately actionable.
- Risks and blockers are explicitly called out.
</success_criteria>

<context>
## Cycle Summary

**Cycle:** {{ cycle_number }} of {{ max_cycles }}

### Work Completed
{{ work_completed }}

### Artifacts / Changes
{{ artifacts }}

### Tests / Validation
{{ tests_run }}

### Issues / Risks Identified
{{ issues_found }}

### What Remains
{{ work_remaining }}

### Recommended Next Focus
{{ next_focus_suggestion }}

### Status
{{ status }}
</context>

<wrap_up_framework>
## Your Wrap-Up MUST Include

### 1. Accomplishments (What was done)
- List specific items completed
- Note files created/modified
- Summarize test results

### 2. Quality Assessment
- Did all validations pass?
- Any new technical debt introduced?
- Are there any regressions?

### 3. Remaining Work
- What's left from the original plan?
- Any new work discovered during execution?
- Priority order for remaining items

### 4. Risks and Blockers
- What could prevent progress?
- Any dependencies on external input?
- Known issues that need attention

### 5. Next Focus Recommendation
- Specific, actionable next step
- Why this is the right priority
- What "done" looks like for that step
</wrap_up_framework>

<wrap_up_format>
## Output Format

```markdown
## Cycle {{ cycle_number }} Wrap-Up

### ✅ Completed This Cycle
- [Specific accomplishment 1]
- [Specific accomplishment 2]
- [...]

### 📁 Files Changed
- `path/to/file1.py` - [what changed]
- `path/to/file2.py` - [what changed]

### 🧪 Validation Results
- Syntax: [PASS/FAIL]
- Linting: [PASS/FAIL] 
- Tests: [X passed, Y failed]

### ⚠️ Issues / Risks
- [Issue 1] - [severity: low/medium/high]
- [Risk 1] - [mitigation if any]

### 📋 Remaining Work
1. [Priority 1 item]
2. [Priority 2 item]
3. [...]

### 🎯 Recommended Next Focus
**Action:** [Specific action]
**Reason:** [Why this is the priority]
**Done when:** [Completion criteria]

### 📊 Overall Status
[In Progress / Blocked / Ready for Review / Complete]
```
</wrap_up_format>

<self_reflection>
## Before Finalizing, Ask Yourself:

1. Have I accurately captured what was accomplished?
2. Is my assessment of remaining work realistic?
3. Are there any risks I'm not acknowledging?
4. Is my next focus recommendation specific enough to act on?
5. Would someone else understand the current state from this summary?
</self_reflection>

<power_phrases>
- "Looking back at this cycle, the key accomplishment was..."
- "The main blocker for the next cycle is..."
- "Given the current state, the highest priority is..."
- "Before we can proceed with X, we MUST address Y..."
</power_phrases>

<anti_patterns>
## Avoid These Wrap-Up Mistakes

❌ **Vague status**: "Made some progress"
✅ **Specific status**: "Completed 3 of 5 plan items, tests passing"

❌ **Missing risks**: Not mentioning known issues
✅ **Honest assessment**: "Test coverage is incomplete for edge cases"

❌ **Unclear next step**: "Continue working on the task"
✅ **Actionable next step**: "Implement error handling in `validate_input()` function"
</anti_patterns>
