<objective>
Document the prompt library structure and required tag conventions.
</objective>

<quick_start>
- Review the folder structure and prompt categories.
- Ensure prompt files include the required XML tags.
</quick_start>

<success_criteria>
- Prompt structure and legacy mapping are clear.
- Required tags for prompt files are listed.
</success_criteria>

<context>
# Prompt Library

This directory contains all CCE prompt content and the prompt manager that loads and composes templates.

## Structure

- `identity/` - core identity prompts that define the agent's role and baseline behavior
- `phases/` - phase prompts (orient/execute/reconcile/decide) plus quality, synthesis, and supervisor subfolders
- `frameworks/` - reusable analysis frameworks, stakeholder prompts, and decision guides
- `tools/` - tool usage guidance and examples
- `guardrails/` - safety constraints and error-handling guidance
- `manager.py` - prompt loading/composition utility

## Legacy Mapping

Legacy prompt locations were consolidated into this hierarchy:
- `supervisor/` -> `phases/supervisor/`
- `synthesis/` -> `phases/synthesis/`
- `quality/` -> `phases/quality/`
- `stakeholders/` -> `frameworks/stakeholders/`
- `knowledge/` -> `frameworks/knowledge/`

All prompt files should use XML tags for structure, including:
- `&lt;objective&gt;`
- `&lt;quick_start&gt;`
- `&lt;success_criteria&gt;`
</context>
