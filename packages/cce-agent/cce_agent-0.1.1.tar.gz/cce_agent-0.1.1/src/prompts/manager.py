"""
Centralized Prompt Management System

Migrated from the notebook prototype to provide centralized, observable,
and maintainable prompt management for the CCE agent.

Features:
- Single source of truth for all prompts
- Template composition and variable substitution
- LangSmith observability integration
- A/B testing support (future)
"""

import logging
import os
from pathlib import Path
from typing import Any

try:
    from langsmith import Client as LangSmithClient

    LANGSMITH_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    LangSmithClient = None
    LANGSMITH_AVAILABLE = False


DEFAULT_PROMPT_HUB_ALLOWLIST = {
    "identity/cce_identity.md",
    "tools/tool_descriptions.md",
    "frameworks/when_to_search.md",
    "frameworks/when_to_test.md",
    "frameworks/when_to_commit.md",
    "guardrails/approval_required.md",
    "guardrails/banned_commands.md",
}


class PromptManager:
    """
    Centralized prompt management system for the CCE agent.

    Provides template loading, composition, and variable substitution
    with observability and caching support.
    """

    def __init__(self, base_path: str | None = None):
        """
        Initialize the PromptManager.

        Args:
            base_path: Base path for prompt templates (defaults to src/prompts)
        """
        self.logger = logging.getLogger(__name__)

        # Set up paths
        if base_path:
            self.base_path = Path(base_path)
        else:
            # Default to src/prompts relative to this file
            self.base_path = Path(__file__).parent

        self.identity_path = self.base_path / "identity"
        self.phases_path = self.base_path / "phases"
        self.frameworks_path = self.base_path / "frameworks"
        self.tools_path = self.base_path / "tools"
        self.guardrails_path = self.base_path / "guardrails"

        self.stakeholders_path = self.frameworks_path / "stakeholders"
        self.supervisor_path = self.phases_path / "supervisor"
        self.knowledge_path = self.frameworks_path / "knowledge"
        self.synthesis_path = self.phases_path / "synthesis"
        self.quality_path = self.phases_path / "quality"

        # Cache for loaded templates
        self._cache: dict[str, str] = {}

        # LangSmith Prompt Hub configuration (optional)
        self._prompt_hub_enabled = False
        self._prompt_hub_namespace = "cce"
        self._prompt_hub_allowlist = {self._normalize_template_path(path) for path in DEFAULT_PROMPT_HUB_ALLOWLIST}
        self._prompt_hub_sync_mode = "pull"
        self._prompt_hub_synced = False
        self._prompt_hub_client = None
        self._configure_prompt_hub()

        self.logger.info(f"PromptManager initialized with base path: {self.base_path}")

    def load_template(self, template_path: str, use_cache: bool = True) -> str:
        """
        Load a prompt template from file.

        Args:
            template_path: Path to template file (relative to base_path)
            use_cache: Whether to use cached version if available

        Returns:
            Template content as string
        """
        full_path = self.base_path / template_path
        normalized_path = self._normalize_template_path(template_path)

        # Check cache first
        if use_cache and str(full_path) in self._cache:
            return self._cache[str(full_path)]

        if self._should_use_prompt_hub(normalized_path):
            hub_content = self._load_template_from_prompt_hub(template_path)
            if hub_content is not None:
                if use_cache:
                    self._cache[str(full_path)] = hub_content
                return hub_content

        try:
            self.logger.info(f"Loading template from: {full_path}")
            print(f"🔍 [DEBUG] PromptManager: Loading template from: {full_path}")

            with open(full_path, encoding="utf-8") as f:
                content = f.read()

            # Cache the content
            self._cache[str(full_path)] = content

            self.logger.info(f"Template loaded successfully: {template_path} ({len(content)} chars)")
            print(f"✅ [DEBUG] PromptManager: Template loaded: {template_path} ({len(content)} chars)")
            return content

        except FileNotFoundError:
            self.logger.error(f"Template not found: {full_path}")
            print(f"❌ [DEBUG] PromptManager: Template not found: {full_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading template {template_path}: {e}")
            raise

    @staticmethod
    def _normalize_template_path(template_path: str) -> str:
        return str(Path(template_path).as_posix())

    def _configure_prompt_hub(self) -> None:
        try:
            from src.config_loader import get_config

            config = get_config()
            self._prompt_hub_enabled = bool(config.langsmith.prompt_hub_enabled)
            if config.langsmith.prompt_hub_namespace is not None:
                self._prompt_hub_namespace = config.langsmith.prompt_hub_namespace

            if config.langsmith.prompt_hub_allowlist:
                self._prompt_hub_allowlist = {
                    self._normalize_template_path(path) for path in config.langsmith.prompt_hub_allowlist
                }
            if config.langsmith.prompt_hub_sync_mode:
                self._prompt_hub_sync_mode = str(config.langsmith.prompt_hub_sync_mode).strip().lower()
        except Exception as exc:
            self.logger.debug("Prompt hub config not loaded: %s", exc)

        if self._prompt_hub_enabled and not LANGSMITH_AVAILABLE:
            self.logger.warning("Prompt Hub enabled but langsmith is unavailable; disabling hub.")
            self._prompt_hub_enabled = False

        if self._prompt_hub_enabled and not os.getenv("LANGSMITH_API_KEY"):
            self.logger.warning("Prompt Hub enabled without LANGSMITH_API_KEY; disabling hub.")
            self._prompt_hub_enabled = False

        if self._prompt_hub_sync_mode not in {"pull", "push", "both", "off"}:
            self.logger.warning(
                "Unknown prompt hub sync mode '%s'; defaulting to 'pull'",
                self._prompt_hub_sync_mode,
            )
            self._prompt_hub_sync_mode = "pull"

        if self._prompt_hub_enabled and self._should_push_prompt_hub() and not self._prompt_hub_synced:
            try:
                self.sync_prompt_hub()
            except Exception as exc:
                self.logger.warning("Prompt hub sync failed: %s", exc)

    def _should_use_prompt_hub(self, normalized_path: str) -> bool:
        return (
            self._prompt_hub_enabled
            and self._prompt_hub_sync_mode in {"pull", "both"}
            and normalized_path in self._prompt_hub_allowlist
        )

    def _should_push_prompt_hub(self) -> bool:
        return self._prompt_hub_enabled and self._prompt_hub_sync_mode in {"push", "both"}

    def _load_template_from_disk(self, template_path: str) -> str:
        full_path = self.base_path / template_path
        with open(full_path, encoding="utf-8") as handle:
            return handle.read()

    def _build_prompt_object(self, content: str) -> Any | None:
        try:
            from langchain_core.prompts import PromptTemplate
        except ImportError as exc:  # pragma: no cover - optional dependency
            self.logger.warning("Prompt Hub push requires langchain-core: %s", exc)
            return None

        try:
            return PromptTemplate.from_template(content)
        except Exception as exc:
            self.logger.warning("Failed to build prompt template for hub sync: %s", exc)
            return None

    def publish_prompt(
        self,
        template_path: str,
        *,
        description: str | None = None,
        readme: str | None = None,
        tags: list[str] | None = None,
        is_public: bool | None = None,
    ) -> str | None:
        """Publish a prompt file to LangSmith Prompt Hub."""
        if not self._ensure_prompt_hub_client():
            return None

        normalized_path = self._normalize_template_path(template_path)
        try:
            content = self._load_template_from_disk(normalized_path)
        except OSError as exc:
            self.logger.warning("Prompt Hub publish failed for %s: %s", normalized_path, exc)
            return None

        prompt_object = self._build_prompt_object(content)
        if prompt_object is None:
            return None

        prompt_id = self._prompt_hub_identifier(normalized_path)
        try:
            url = self._prompt_hub_client.push_prompt(
                prompt_id,
                object=prompt_object,
                description=description,
                readme=readme,
                tags=tags,
                is_public=is_public,
            )
            self.logger.info("Published prompt to hub: %s", prompt_id)
            return url
        except Exception as exc:
            self.logger.warning("Prompt Hub publish failed for %s: %s", prompt_id, exc)
            return None

    def sync_prompt_hub(self) -> dict[str, str]:
        """Sync allowlisted prompts to LangSmith Prompt Hub."""
        if not self._should_push_prompt_hub():
            return {}
        if not self._ensure_prompt_hub_client():
            return {}

        results: dict[str, str] = {}
        for template_path in sorted(self._prompt_hub_allowlist):
            url = self.publish_prompt(template_path)
            if url:
                results[template_path] = url

        if results:
            self.logger.info("Prompt Hub sync completed: %s prompts", len(results))
        self._prompt_hub_synced = True
        return results

    def _ensure_prompt_hub_client(self) -> bool:
        if self._prompt_hub_client is not None:
            return True
        if not LANGSMITH_AVAILABLE or LangSmithClient is None:
            return False
        try:
            self._prompt_hub_client = LangSmithClient()
            return True
        except Exception as exc:
            self.logger.warning("Failed to initialize LangSmith client for Prompt Hub: %s", exc)
            return False

    def _prompt_hub_identifier(self, template_path: str) -> str:
        normalized = self._normalize_template_path(template_path)
        slug = str(Path(normalized).with_suffix("").as_posix())
        safe_slug = slug.replace("/", "__")
        if self._prompt_hub_namespace:
            return f"{self._prompt_hub_namespace}/{safe_slug}"
        return safe_slug

    def _coerce_prompt_to_text(self, prompt: Any) -> str:
        if prompt is None:
            return ""
        if isinstance(prompt, str):
            return prompt

        template_attr = getattr(prompt, "template", None)
        if isinstance(template_attr, str):
            return template_attr

        messages = getattr(prompt, "messages", None)
        if messages:
            parts: list[str] = []
            for message in messages:
                if isinstance(message, str):
                    parts.append(message)
                    continue
                message_template = getattr(message, "template", None)
                if isinstance(message_template, str):
                    parts.append(message_template)
                    continue
                nested_prompt = getattr(message, "prompt", None)
                nested_template = getattr(nested_prompt, "template", None)
                if isinstance(nested_template, str):
                    parts.append(nested_template)
                    continue
                parts.append(str(message))
            return "\n".join(parts)

        to_string = getattr(prompt, "to_string", None)
        if callable(to_string):
            try:
                return to_string()
            except Exception:
                pass

        return str(prompt)

    def _load_template_from_prompt_hub(self, template_path: str) -> str | None:
        if not self._ensure_prompt_hub_client():
            return None

        prompt_id = self._prompt_hub_identifier(template_path)
        try:
            self.logger.info("Loading prompt from LangSmith hub: %s", prompt_id)
            prompt = self._prompt_hub_client.pull_prompt(prompt_id)
        except Exception as exc:
            self.logger.warning("Prompt Hub pull failed for %s: %s", prompt_id, exc)
            return None

        content = self._coerce_prompt_to_text(prompt).strip()
        if not content:
            self.logger.warning("Prompt Hub returned empty content for %s", prompt_id)
            return None
        return content

    def substitute_variables(self, template: str, variables: dict[str, Any]) -> str:
        """
        Substitute variables in a template using simple string replacement.

        Uses {{ variable_name }} syntax for substitution.

        Args:
            template: Template string with {{ variable }} placeholders
            variables: Dictionary of variable name -> value mappings

        Returns:
            Template with variables substituted
        """
        result = template

        for var_name, var_value in variables.items():
            # Try both formats: with and without spaces
            placeholder_no_spaces = f"{{{{{var_name}}}}}"
            placeholder_with_spaces = f"{{{{ {var_name} }}}}"

            # Convert value to string if needed
            if isinstance(var_value, (list, dict)):
                # For complex types, use a simple string representation
                if isinstance(var_value, list):
                    str_value = "\n".join(f"- {item}" for item in var_value)
                else:
                    str_value = str(var_value)
            else:
                str_value = str(var_value)

            # Debug output can be removed in production

            # Try both placeholder formats
            result = result.replace(placeholder_no_spaces, str_value)
            result = result.replace(placeholder_with_spaces, str_value)

        # Validate template substitution
        self.validate_template_substitution(result, variables)

        return result

    def validate_template_substitution(self, result: str, variables: dict[str, Any]) -> None:
        """
        Validate that template substitution was successful.

        Args:
            result: The result of template substitution
            variables: The variables that were used for substitution

        Raises:
            Warning: If unresolved placeholders are found
        """
        import re

        # Find all double-brace placeholders that weren't substituted
        unresolved_placeholders = re.findall(r"\{\{([^}]+)\}\}", result)

        if unresolved_placeholders:
            unresolved_vars = [var.strip() for var in unresolved_placeholders]
            self.logger.warning(f"Template substitution warning: Unresolved placeholders found: {unresolved_vars}")
            self.logger.warning(f"Available variables: {list(variables.keys())}")

            # Log the problematic template section for debugging
            for placeholder in unresolved_placeholders:
                placeholder_full = f"{{{{{placeholder}}}}}"
                if placeholder_full in result:
                    self.logger.warning(f"Unresolved placeholder: {placeholder_full}")

        # Check for single-brace patterns that might indicate incorrect syntax
        single_brace_patterns = re.findall(r"\{[^{][^}]*\}", result)
        if single_brace_patterns:
            # Filter out JSON examples from single-brace patterns
            json_examples = []
            non_json_patterns = []

            for pattern in single_brace_patterns:
                if self._is_json_example(pattern):
                    json_examples.append(pattern)
                else:
                    non_json_patterns.append(pattern)

            if non_json_patterns:
                self.logger.warning(
                    f"Template validation warning: Single-brace patterns found (may indicate incorrect syntax): {non_json_patterns}"
                )
                self.logger.warning("Consider using double braces {{variable_name}} for template variables")

            if json_examples:
                self.logger.debug(f"JSON examples detected (ignored in validation): {len(json_examples)} patterns")

    def _is_json_example(self, pattern: str) -> bool:
        """
        Check if a single-brace pattern is a JSON example rather than a template variable.

        Args:
            pattern: The pattern to check

        Returns:
            True if the pattern appears to be a JSON example
        """
        import json

        # Common JSON example indicators
        json_indicators = [
            '"perspective"',
            '"aspects"',
            '"analysis"',
            '"decision"',
            '"rationale"',
            '"consequences"',
            '"context"',
            '"status"',
            '"phase"',
            '"timestamp"',
            '"implementation_readiness"',
            '"ticket_coverage"',
            '"stakeholder_balance"',
            '"technical_feasibility"',
            '"clarity_completeness"',
            '"overall_score"',
            '"details"',
            '"recommendations"',
            '"pass_threshold"',
            # LangGraph-specific patterns
            '"validate"',
            '"end"',
            "END",
            "START",
        ]

        # Check if pattern contains JSON-like structure
        pattern_lower = pattern.lower()

        # Check for JSON key indicators
        has_json_keys = any(indicator in pattern_lower for indicator in json_indicators)

        # Check for JSON array indicators
        has_json_array = "[" in pattern and "]" in pattern

        # Check for JSON object indicators
        has_json_object = ":" in pattern and ('"' in pattern or "'" in pattern)

        # Check for common JSON patterns
        has_json_structure = has_json_keys or (has_json_array and has_json_object)

        # Try to parse as JSON (for complete JSON objects)
        try:
            json.loads(pattern)
            return True
        except (json.JSONDecodeError, ValueError):
            pass

        # If it has JSON structure indicators, consider it a JSON example
        return has_json_structure

    def get_stakeholder_prompt(self, stakeholder_type: str, stakeholder_config: dict[str, Any]) -> str:
        """
        Get the prompt template for a specific stakeholder type.

        Args:
            stakeholder_type: Type of stakeholder (e.g., "aider_integration")
            stakeholder_config: Configuration for the stakeholder

        Returns:
            Base stakeholder prompt template
        """
        self.logger.info(f"Getting stakeholder prompt for {stakeholder_type}")
        print(f"🔍 [DEBUG] PromptManager: Getting stakeholder prompt for {stakeholder_type}")

        try:
            # Load base stakeholder template
            self.logger.info(f"Loading base stakeholder template...")
            print(f"🔍 [DEBUG] PromptManager: Loading base stakeholder template...")
            base_template = self.load_template("frameworks/stakeholders/base_stakeholder.md")
            self.logger.info(f"Base template loaded, length: {len(base_template)}")
            print(f"🔍 [DEBUG] PromptManager: Base template loaded, length: {len(base_template)}")

            # Load stakeholder-specific additions if they exist
            specific_path = f"frameworks/stakeholders/{stakeholder_type}.md"
            try:
                specific_template = self.load_template(specific_path)
                # Combine base and specific templates
                combined_template = f"{base_template}\n\n## Specific Expertise\n\n{specific_template}"
            except FileNotFoundError:
                # No specific template, use base only
                combined_template = base_template

            # Load stakeholder-specific knowledge
            knowledge_content = self._load_stakeholder_knowledge(stakeholder_type)

            # Substitute stakeholder-specific variables
            variables = {
                "stakeholder_name": stakeholder_config.get("name", stakeholder_type),
                "stakeholder_domain": stakeholder_config.get("domain", "domain expertise"),
                "focus_areas": stakeholder_config.get("focus_areas", []),
                "aider_docs_and_code": knowledge_content.get("aider_docs_and_code", ""),
                "langgraph_knowledge": knowledge_content.get("langgraph_knowledge", ""),
            }

            # Debug output can be removed in production

            return self.substitute_variables(combined_template, variables)

        except Exception as e:
            self.logger.error(f"Error getting stakeholder prompt for {stakeholder_type}: {e}")
            # Return a basic fallback prompt
            return f"You are a {stakeholder_type} specialist providing domain expertise."

    def _load_stakeholder_knowledge(self, stakeholder_type: str) -> dict[str, str]:
        """
        Load domain-specific knowledge for a stakeholder type.

        Args:
            stakeholder_type: Type of stakeholder (e.g., "aider_integration")

        Returns:
            Dictionary containing knowledge content for different domains
        """
        knowledge_content = {"aider_docs_and_code": "", "langgraph_knowledge": ""}

        try:
            # Load AIDER knowledge for AIDER integration stakeholders
            if stakeholder_type == "aider_integration":
                aider_knowledge_path = self.knowledge_path / "aider_integration.md"
                if aider_knowledge_path.exists():
                    with open(aider_knowledge_path, encoding="utf-8") as f:
                        knowledge_content["aider_docs_and_code"] = f.read()
                        self.logger.debug(
                            f"Loaded AIDER knowledge: {len(knowledge_content['aider_docs_and_code'])} chars"
                        )

            # Load LangGraph knowledge for LangGraph architecture stakeholders
            if stakeholder_type == "langgraph_architecture":
                langgraph_knowledge_path = self.knowledge_path / "langgraph_architecture.md"
                if langgraph_knowledge_path.exists():
                    with open(langgraph_knowledge_path, encoding="utf-8") as f:
                        knowledge_content["langgraph_knowledge"] = f.read()
                        self.logger.debug(
                            f"Loaded LangGraph knowledge: {len(knowledge_content['langgraph_knowledge'])} chars"
                        )

        except Exception as e:
            self.logger.warning(f"Failed to load knowledge for {stakeholder_type}: {e}")
            # Return empty knowledge content on failure

        return knowledge_content

    def compose_stakeholder_analysis_prompt(self, stakeholder_prompt: str, context_sections: dict[str, str]) -> str:
        """
        Compose a complete stakeholder analysis prompt.

        Args:
            stakeholder_prompt: Base stakeholder prompt template
            context_sections: Dictionary of context sections to include

        Returns:
            Complete analysis prompt
        """

        # Build the analysis prompt structure
        analysis_template = """
{{stakeholder_prompt}}

## Analysis Context

### Integration Challenge
{{integration_challenge}}

### Charter
{{charter}}

### Your Focus Areas
{{focus_areas}}

### Previous Stakeholder Contributions
{{previous_contributions}}

### Analysis Guidance
{{analysis_guidance}}

## Your Task

Provide a detailed analysis from your domain perspective. Consider:

1. **Domain-Specific Concerns**: What are the key challenges and opportunities in your area?
2. **Integration Points**: How does your domain interact with other stakeholders' concerns?
3. **Implementation Recommendations**: What specific approaches do you recommend?
4. **Risk Assessment**: What are the potential risks and mitigation strategies?
5. **Success Criteria**: How will we know if your domain's concerns are properly addressed?

Be thorough, specific, and constructive in your analysis.
"""

        # Combine stakeholder prompt with context
        variables = {"stakeholder_prompt": stakeholder_prompt, **context_sections}

        return self.substitute_variables(analysis_template, variables)

    def get_supervisor_prompt(self, state: str = "coordination") -> str:
        """
        Get supervisor prompt for a specific state.

        Args:
            state: Supervisor state (e.g., "coordination", "synthesis", "quality")

        Returns:
            Supervisor prompt for the specified state
        """
        try:
            # Load base supervisor template
            base_template = self.load_template("phases/supervisor/base_supervisor.md")

            # Load state-specific template if it exists
            state_path = f"phases/supervisor/{state}.md"
            try:
                state_template = self.load_template(state_path)
                combined_template = f"{base_template}\n\n## Current State: {state.title()}\n\n{state_template}"
            except FileNotFoundError:
                # No state-specific template, use base only
                combined_template = base_template

            return combined_template

        except Exception as e:
            self.logger.error(f"Error getting supervisor prompt for state {state}: {e}")
            # Return basic fallback
            return "You are a supervisor coordinating a multi-stakeholder architecture discussion."

    def get_synthesis_prompt(self) -> str:
        """Get the synthesis engine prompt template."""
        try:
            return self.load_template("phases/synthesis/synthesis_engine.md")
        except FileNotFoundError:
            # Fallback synthesis prompt
            return """You are a synthesis engine that combines multiple stakeholder perspectives into a coherent architecture description.

Your task is to:
1. Identify common themes and patterns across stakeholder contributions
2. Resolve conflicts and contradictions between different perspectives  
3. Create a unified, implementable architecture description
4. Ensure all critical concerns are addressed

Be comprehensive, balanced, and practical in your synthesis."""

    def get_quality_gates_prompt(self) -> str:
        """Get the quality gates evaluation prompt template."""
        try:
            return self.load_template("phases/quality/quality_gates.md")
        except FileNotFoundError:
            # Fallback quality gates prompt
            return """You are a quality gates evaluator assessing architecture descriptions.

Evaluate the synthesis on these criteria:
1. **Implementation Readiness** (0-1): How ready is this for implementation?
2. **Ticket Coverage** (0-1): How well does this address the original requirements?
3. **Stakeholder Balance** (0-1): Are all stakeholder concerns adequately addressed?
4. **Technical Feasibility** (0-1): Is this technically sound and achievable?
5. **Clarity and Completeness** (0-1): Is the description clear and comprehensive?

        Provide scores, rationale, and specific improvement recommendations."""

    def get_cycling_prompt(self, prompt_name: str) -> str:
        """
        Get a cycling prompt template by name.

        Args:
            prompt_name: Template name without extension (e.g., "orientation")

        Returns:
            Cycling prompt template content
        """
        try:
            return self.load_template(f"cycling/{prompt_name}.md")
        except FileNotFoundError:
            self.logger.error(f"Cycling prompt not found: {prompt_name}")
            raise

    def create_template_directory(self, template_type: str) -> Path:
        """
        Create a template directory if it doesn't exist.

        Args:
            template_type: Type of template directory to create

        Returns:
            Path to the created directory
        """
        template_dir = self.base_path / template_type
        template_dir.mkdir(parents=True, exist_ok=True)
        return template_dir

    def list_templates(self, template_type: str | None = None) -> list[str]:
        """
        List available templates.

        Args:
            template_type: Optional filter by template type

        Returns:
            List of available template paths
        """
        if template_type:
            search_path = self.base_path / template_type
        else:
            search_path = self.base_path

        if not search_path.exists():
            return []

        templates = []
        for file_path in search_path.rglob("*.md"):
            rel_path = file_path.relative_to(self.base_path)
            templates.append(str(rel_path))

        return sorted(templates)

    def clear_cache(self):
        """Clear the template cache."""
        self._cache.clear()
        self.logger.info("Template cache cleared")

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        return {
            "cached_templates": len(self._cache),
            "cache_size_bytes": sum(len(content.encode("utf-8")) for content in self._cache.values()),
            "cached_paths": list(self._cache.keys()),
        }
