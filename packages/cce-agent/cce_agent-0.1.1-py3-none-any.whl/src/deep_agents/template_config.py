"""
Template Configuration System for Deep Agents

This module provides configurable template systems for instruction generation,
following existing configuration patterns in the CCE Deep Agent system.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TemplateType(Enum):
    """Types of instruction templates."""

    DEEP_AGENT_EXECUTION = "deep_agent_execution"
    PLANNING_GRAPH = "planning_graph"
    PHASE_EXECUTION = "phase_execution"
    CUSTOM = "custom"


class ValidationLevel(Enum):
    """Validation levels for template processing."""

    STRICT = "strict"
    MODERATE = "moderate"
    LENIENT = "lenient"


@dataclass
class TemplateConfig:
    """Configuration for instruction templates."""

    template_type: TemplateType
    name: str
    description: str
    template_string: str
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    validation_level: ValidationLevel = ValidationLevel.MODERATE
    fallback_template: str | None = None
    custom_parameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TemplateValidationResult:
    """Results of template validation."""

    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    validated_fields: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    invalid_fields: list[str] = field(default_factory=list)


class TemplateConfigurationManager:
    """
    Manages template configurations for different agent types and use cases.

    This class provides a centralized system for managing instruction templates
    with validation, fallbacks, and configuration following existing patterns.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize template configuration manager.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.templates: dict[str, TemplateConfig] = {}
        self.default_templates: dict[TemplateType, str] = {}

        # Initialize with default templates
        self._initialize_default_templates()

        # Load custom templates if provided
        if "custom_templates" in self.config:
            self._load_custom_templates(self.config["custom_templates"])

    def _initialize_default_templates(self) -> None:
        """Initialize default template configurations."""
        # Deep Agent Execution Template
        deep_agent_template = TemplateConfig(
            template_type=TemplateType.DEEP_AGENT_EXECUTION,
            name="deep_agent_execution_default",
            description="Default template for deep agent execution instructions",
            template_string="""You are executing a plan for GitHub ticket: {ticket_title}

TICKET DESCRIPTION:
{ticket_description}

PLAN TO EXECUTE:
{plan}

INSTRUCTIONS:
1. Execute the plan step by step
2. Use the available tools to implement the required changes
3. Focus on the specific requirements in the ticket description
4. You have access to all existing files in the virtual filesystem
5. Use write_file, edit_file to make changes
6. IMPORTANT: Use sync_to_disk tool at the end to save changes to real files
7. Provide clear progress updates as you work

Current focus: {orientation}""",
            required_fields=["ticket_title", "ticket_description", "plan", "orientation"],
            optional_fields=["additional_context", "constraints"],
            validation_level=ValidationLevel.MODERATE,
            fallback_template="Execute the plan: {plan}\nFocus: {orientation}",
            metadata={"version": "1.0", "created_by": "template_system", "last_updated": "2025-09-22"},
        )

        # Planning Graph Template
        planning_template = TemplateConfig(
            template_type=TemplateType.PLANNING_GRAPH,
            name="planning_graph_default",
            description="Default template for planning graph instructions",
            template_string="""Analyze the following GitHub ticket and create a comprehensive implementation plan:

TICKET: {ticket_title}
DESCRIPTION: {ticket_description}

CONTEXT: {context}

Please provide:
1. Technical analysis
2. Architectural considerations
3. Implementation phases
4. Risk assessment
5. Success criteria""",
            required_fields=["ticket_title", "ticket_description"],
            optional_fields=["context", "constraints", "requirements"],
            validation_level=ValidationLevel.STRICT,
            fallback_template="Create implementation plan for: {ticket_title}",
            metadata={"version": "1.0", "created_by": "template_system", "last_updated": "2025-09-22"},
        )

        # Phase Execution Template
        phase_template = TemplateConfig(
            template_type=TemplateType.PHASE_EXECUTION,
            name="phase_execution_default",
            description="Default template for phase execution instructions",
            template_string="""Execute Phase {phase_number}: {phase_name}

DESCRIPTION: {phase_description}
OBJECTIVES: {objectives}
SUCCESS CRITERIA: {success_criteria}

CONTEXT: {context}

Please execute this phase step by step and provide progress updates.""",
            required_fields=["phase_number", "phase_name", "phase_description", "objectives", "success_criteria"],
            optional_fields=["context", "dependencies", "constraints"],
            validation_level=ValidationLevel.MODERATE,
            fallback_template="Execute phase: {phase_name} - {phase_description}",
            metadata={"version": "1.0", "created_by": "template_system", "last_updated": "2025-09-22"},
        )

        # Register default templates
        self.templates["deep_agent_execution_default"] = deep_agent_template
        self.templates["planning_graph_default"] = planning_template
        self.templates["phase_execution_default"] = phase_template

        # Set default template mappings
        self.default_templates[TemplateType.DEEP_AGENT_EXECUTION] = "deep_agent_execution_default"
        self.default_templates[TemplateType.PLANNING_GRAPH] = "planning_graph_default"
        self.default_templates[TemplateType.PHASE_EXECUTION] = "phase_execution_default"

        logger.info("Initialized default template configurations")

    def _load_custom_templates(self, custom_templates: dict[str, Any]) -> None:
        """Load custom templates from configuration."""
        for template_name, template_data in custom_templates.items():
            try:
                template_config = TemplateConfig(
                    template_type=TemplateType(template_data.get("template_type", "custom")),
                    name=template_name,
                    description=template_data.get("description", ""),
                    template_string=template_data.get("template_string", ""),
                    required_fields=template_data.get("required_fields", []),
                    optional_fields=template_data.get("optional_fields", []),
                    validation_level=ValidationLevel(template_data.get("validation_level", "moderate")),
                    fallback_template=template_data.get("fallback_template"),
                    custom_parameters=template_data.get("custom_parameters", {}),
                    metadata=template_data.get("metadata", {}),
                )

                self.templates[template_name] = template_config
                logger.info(f"Loaded custom template: {template_name}")

            except Exception as e:
                logger.error(f"Failed to load custom template {template_name}: {e}")

    def get_template(self, template_name: str) -> TemplateConfig | None:
        """
        Get template configuration by name.

        Args:
            template_name: Name of the template

        Returns:
            Template configuration or None if not found
        """
        return self.templates.get(template_name)

    def get_default_template(self, template_type: TemplateType) -> TemplateConfig | None:
        """
        Get default template for a specific type.

        Args:
            template_type: Type of template

        Returns:
            Default template configuration or None if not found
        """
        default_name = self.default_templates.get(template_type)
        if default_name:
            return self.templates.get(default_name)
        return None

    def validate_template_data(self, template_config: TemplateConfig, data: dict[str, Any]) -> TemplateValidationResult:
        """
        Validate data against template configuration.

        Args:
            template_config: Template configuration to validate against
            data: Data to validate

        Returns:
            Validation result with success status and details
        """
        result = TemplateValidationResult(success=True)

        try:
            # Check required fields
            for field in template_config.required_fields:
                if field not in data:
                    result.missing_fields.append(field)
                    result.errors.append(f"Missing required field: {field}")
                    result.success = False
                else:
                    result.validated_fields.append(field)

            # Validate field types and content based on validation level
            if template_config.validation_level == ValidationLevel.STRICT:
                self._validate_strict_mode(template_config, data, result)
            elif template_config.validation_level == ValidationLevel.MODERATE:
                self._validate_moderate_mode(template_config, data, result)
            else:  # LENIENT
                self._validate_lenient_mode(template_config, data, result)

            # Check for unknown fields
            all_known_fields = set(template_config.required_fields + template_config.optional_fields)
            for field in data:
                if field not in all_known_fields:
                    result.warnings.append(f"Unknown field: {field}")

        except Exception as e:
            result.success = False
            result.errors.append(f"Validation error: {str(e)}")

        return result

    def _validate_strict_mode(
        self, template_config: TemplateConfig, data: dict[str, Any], result: TemplateValidationResult
    ) -> None:
        """Validate in strict mode with comprehensive checks."""
        for field, value in data.items():
            if field in template_config.required_fields:
                if not isinstance(value, str) or len(value.strip()) == 0:
                    result.invalid_fields.append(field)
                    result.errors.append(f"Field {field} must be a non-empty string")
                    result.success = False
                elif len(value) < 5:
                    result.warnings.append(f"Field {field} is very short (less than 5 characters)")

    def _validate_moderate_mode(
        self, template_config: TemplateConfig, data: dict[str, Any], result: TemplateValidationResult
    ) -> None:
        """Validate in moderate mode with balanced checks."""
        for field, value in data.items():
            if field in template_config.required_fields:
                if not isinstance(value, str):
                    result.invalid_fields.append(field)
                    result.errors.append(f"Field {field} must be a string")
                    result.success = False
                elif len(value.strip()) == 0:
                    result.warnings.append(f"Field {field} is empty or whitespace only")
                elif len(value) < 3:
                    result.warnings.append(f"Field {field} is very short (less than 3 characters)")

    def _validate_lenient_mode(
        self, template_config: TemplateConfig, data: dict[str, Any], result: TemplateValidationResult
    ) -> None:
        """Validate in lenient mode with minimal checks."""
        for field, value in data.items():
            if field in template_config.required_fields:
                if value is None:
                    result.invalid_fields.append(field)
                    result.errors.append(f"Field {field} cannot be None")
                    result.success = False
                elif isinstance(value, str) and len(value.strip()) == 0:
                    result.warnings.append(f"Field {field} is empty")

    def generate_instruction(self, template_name: str, data: dict[str, Any]) -> str:
        """
        Generate instruction using template and data.

        Args:
            template_name: Name of the template to use
            data: Data to fill into template

        Returns:
            Generated instruction string

        Raises:
            ValueError: If template not found or validation fails
        """
        template_config = self.get_template(template_name)
        if not template_config:
            raise ValueError(f"Template not found: {template_name}")

        # Validate data
        validation_result = self.validate_template_data(template_config, data)

        if not validation_result.success:
            # Try fallback template if available
            if template_config.fallback_template:
                logger.warning(f"Template validation failed for {template_name}, using fallback")
                try:
                    return template_config.fallback_template.format(**data)
                except Exception as e:
                    logger.error(f"Fallback template also failed: {e}")

            error_msg = f"Template validation failed: {', '.join(validation_result.errors)}"
            raise ValueError(error_msg)

        # Log warnings if any
        if validation_result.warnings:
            for warning in validation_result.warnings:
                logger.warning(f"Template validation warning for {template_name}: {warning}")

        # Generate instruction
        try:
            instruction = template_config.template_string.format(**data)
            logger.info(f"Generated instruction using template {template_name} (length: {len(instruction)} chars)")
            return instruction
        except KeyError as e:
            error_msg = f"Missing required field for template {template_name}: {str(e)}"
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Failed to generate instruction from template {template_name}: {str(e)}"
            raise ValueError(error_msg)

    def list_templates(self) -> list[str]:
        """List all available template names."""
        return list(self.templates.keys())

    def list_templates_by_type(self, template_type: TemplateType) -> list[str]:
        """List template names for a specific type."""
        return [name for name, config in self.templates.items() if config.template_type == template_type]


# Default template configuration
DEFAULT_TEMPLATE_CONFIG: dict[str, Any] = {
    "enabled": True,
    "default_validation_level": "moderate",
    "enable_fallbacks": True,
    "custom_templates": {},
    "template_cache": {"enabled": True, "max_size": 100, "ttl_seconds": 3600},
}


def get_template_config(config_name: str = None, key: str = None, default: Any = None) -> Any:
    """
    Get template configuration value.

    Args:
        config_name: Name of the configuration section
        key: Optional specific key within the section
        default: Default value if not found

    Returns:
        Configuration value
    """
    if config_name is None:
        return DEFAULT_TEMPLATE_CONFIG

    if config_name not in DEFAULT_TEMPLATE_CONFIG:
        return default

    config = DEFAULT_TEMPLATE_CONFIG[config_name]

    if key is None:
        return config

    return config.get(key, default)
