<objective>
Provide reference guidance on Aider integration patterns and capabilities.
</objective>

<behavioral_calibration>
<!-- Tone: Technical, reference-oriented -->
<!-- Verbosity: Detailed but focused -->
<!-- Proactiveness: Moderate - emphasize safe defaults -->
</behavioral_calibration>

<quick_start>
- Use this when designing or reviewing Aider integration work.
- Focus on editing strategies, validation, and safety mechanisms.
</quick_start>

<success_criteria>
- Integration decisions align with Aider capabilities and guardrails.
</success_criteria>

<context>
# AIDER Integration Knowledge Base

## AIDER Platform Overview

AIDER is an AI-powered coding assistant that provides sophisticated code understanding and editing capabilities. It serves as the bar setter for AI coding agents with its advanced features.

## Core Capabilities

### 1. RepoMap System
- Tree-sitter parsing: advanced code understanding using Tree-sitter parsers
- Semantic codebase understanding: deep comprehension of code structure and relationships
- Context-aware editing: maintains understanding of code context across edits

### 2. Multi-Strategy Editing
- UnifiedDiff strategy: generates precise, minimal diffs for targeted changes
- EditBlock strategy: creates focused edit blocks for specific code sections
- WholeFile strategy: complete file rewrites when necessary for major changes

### 3. Validation Pipeline
- Automatic linting: post-edit validation with linting tools
- Automated testing: integration with test suites for validation
- Rollback capabilities: automatic rollback on test failures

### 4. Git Integration
- Auto-commit workflows: intelligent commit message generation
- Safety mechanisms: rollback and recovery capabilities
- Branch management: clean branch creation and management

## Integration Patterns

### Code Understanding
```python
# AIDER excels at understanding complex code relationships
class ExampleClass:
    def __init__(self, config):
        self.config = config
        self.dependencies = self._load_dependencies()

    def _load_dependencies(self):
        # AIDER understands this method's role in the class
        return DependencyManager(self.config)
```

### Editing Strategies
- Minimal changes: prefer UnifiedDiff for small, targeted modifications
- Structural changes: use EditBlock for medium-scale refactoring
- Major refactoring: apply WholeFile strategy for complete rewrites

### Validation Integration
- Always run linting after edits
- Execute relevant tests to validate changes
- Implement rollback mechanisms for failed validations

## Best Practices

1. Maintain context: AIDER's strength is understanding code relationships
2. Use appropriate strategy: match editing strategy to change scope
3. Validate changes: always run tests and linting after edits
4. Preserve robustness: maintain AIDER's proven reliability patterns
5. Git safety: use auto-commit with rollback capabilities

## Integration with LangGraph

When integrating AIDER with LangGraph:
- Preserve AIDER's sophisticated code understanding capabilities
- Maintain multi-strategy editing approach
- Keep validation pipeline intact
- Ensure git operations remain safe and reliable
- Adapt AIDER patterns to LangGraph's state management system
</context>

<decision_framework>
If unsure which editing strategy to use:
- Prefer UnifiedDiff for small, targeted edits.
- Use EditBlock for localized refactors.
- Use WholeFile only when structural changes require it.
</decision_framework>

<power_phrases>
- "This change is small; UnifiedDiff is appropriate."
- "This refactor spans multiple blocks; EditBlock is safer."
</power_phrases>
