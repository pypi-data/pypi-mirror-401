"""
ADR Integration Hook for Deep Agents Execution

This module provides ADR (Architecture Decision Record) integration for deep agents
execution, allowing architectural decisions to be captured during implementation
phases, not just during planning.
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# Import ADR system from stakeholder generator
try:
    from ..stakeholder_generator.adr import ADRManager, ArchitectureDecision
except ImportError:
    # Fallback if stakeholder generator not available
    ADRManager = None
    ArchitectureDecision = None

logger = logging.getLogger(__name__)


class ADRIntegrationHook:
    """
    Hook for capturing architectural decisions during deep agents execution.

    This hook monitors deep agents execution and creates ADRs for significant
    architectural decisions made during implementation.
    """

    def __init__(self, workspace_root: str, enabled: bool = True):
        """
        Initialize ADR integration hook.

        Args:
            workspace_root: Root directory for ADR storage
            enabled: Whether ADR capture is enabled
        """
        self.workspace_root = workspace_root
        self.enabled = enabled
        self.adr_manager = None
        self.decision_count = 0

        if self.enabled and ADRManager:
            try:
                self.adr_manager = ADRManager(output_directory=workspace_root)
                logger.info("✅ ADR integration hook initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize ADR manager: {e}")
                self.enabled = False
        elif not ADRManager:
            logger.warning("⚠️ ADR system not available - ADR integration disabled")
            self.enabled = False

    def should_capture_decision(self, tool_name: str, tool_args: dict[str, Any], context: dict[str, Any]) -> bool:
        """
        Determine if a tool call represents an architectural decision worth capturing.

        Args:
            tool_name: Name of the tool being called
            tool_args: Arguments passed to the tool
            context: Execution context

        Returns:
            True if this should be captured as an ADR
        """
        if not self.enabled:
            return False

        # Define architectural decision patterns
        architectural_patterns = {
            # File operations that create new architecture
            "write_file": self._is_architectural_file_creation,
            "edit_file": self._is_architectural_file_edit,
            # Planning and architecture tools
            "create_plan": lambda args, ctx: True,
            "update_plan": lambda args, ctx: True,
            "research_codebase": lambda args, ctx: True,
            # Configuration changes
            "read_file": self._is_config_file_read,
        }

        # Check if this tool call matches architectural patterns
        if tool_name in architectural_patterns:
            return architectural_patterns[tool_name](tool_args, context)

        return False

    def _is_architectural_file_creation(self, tool_args: dict[str, Any], context: dict[str, Any]) -> bool:
        """Check if file creation represents architectural decision."""
        file_path = tool_args.get("file_path", "")
        content = tool_args.get("content", "")

        # Check for architectural file patterns
        architectural_files = [
            "architecture",
            "design",
            "spec",
            "adr",
            "decision",
            "config",
            "constants",
            "integration",
            "hook",
            "manager",
        ]

        # Check if file path or content suggests architectural significance
        file_lower = file_path.lower()
        content_lower = content.lower()

        # File path patterns
        if any(pattern in file_lower for pattern in architectural_files):
            return True

        # Content patterns
        architectural_keywords = [
            "architecture",
            "design pattern",
            "integration",
            "decision",
            "strategy",
            "approach",
            "implementation",
            "framework",
        ]

        if any(keyword in content_lower for keyword in architectural_keywords):
            return True

        return False

    def _is_architectural_file_edit(self, tool_args: dict[str, Any], context: dict[str, Any]) -> bool:
        """Check if file edit represents architectural decision."""
        file_path = tool_args.get("file_path", "")
        changes = tool_args.get("changes", "")

        # Check for architectural file patterns
        architectural_files = [
            "architecture",
            "design",
            "spec",
            "adr",
            "decision",
            "config",
            "constants",
            "integration",
            "hook",
            "manager",
            "agent",
            "graph",
            "state",
            "workflow",
        ]

        file_lower = file_path.lower()
        changes_lower = changes.lower()

        # File path patterns
        if any(pattern in file_lower for pattern in architectural_files):
            return True

        # Check for significant architectural changes
        significant_changes = [
            "class",
            "def ",
            "import",
            "from ",
            "architecture",
            "design",
            "pattern",
            "integration",
            "workflow",
        ]

        if any(change in changes_lower for change in significant_changes):
            return True

        return False

    def _is_config_file_read(self, tool_args: dict[str, Any], context: dict[str, Any]) -> bool:
        """Check if config file read suggests architectural decision."""
        file_path = tool_args.get("file_path", "")

        config_files = ["config", "constants", "settings", "env", "yaml", "json", "toml", "ini", "properties"]

        file_lower = file_path.lower()
        return any(pattern in file_lower for pattern in config_files)

    def capture_decision(
        self, tool_name: str, tool_args: dict[str, Any], context: dict[str, Any], result: Any = None
    ) -> ArchitectureDecision | None:
        """
        Capture an architectural decision as an ADR.

        Args:
            tool_name: Name of the tool that made the decision
            tool_args: Arguments passed to the tool
            context: Execution context
            result: Result of the tool execution

        Returns:
            Created ADR or None if not captured
        """
        if not self.enabled or not self.adr_manager:
            return None

        try:
            self.decision_count += 1

            # Generate ADR content based on tool and context
            adr_content = self._generate_adr_content(tool_name, tool_args, context, result)

            # Create the ADR
            adr = self.adr_manager.create_adr(
                title=adr_content["title"],
                context=adr_content["context"],
                decision=adr_content["decision"],
                consequences=adr_content["consequences"],
                status="Accepted",
            )

            logger.info(f"📝 ADR captured: {adr.title}")
            return adr

        except Exception as e:
            logger.error(f"❌ Failed to capture ADR: {e}")
            return None

    def _generate_adr_content(
        self, tool_name: str, tool_args: dict[str, Any], context: dict[str, Any], result: Any
    ) -> dict[str, str]:
        """Generate ADR content based on tool execution."""

        # Get context information
        ticket_title = context.get("ticket_title", "Unknown Ticket")
        execution_phase = context.get("execution_phase", "Implementation")

        # Generate title
        if tool_name == "write_file":
            file_path = tool_args.get("file_path", "unknown")
            title = f"Architecture Decision: Created {os.path.basename(file_path)}"
        elif tool_name == "edit_file":
            file_path = tool_args.get("file_path", "unknown")
            title = f"Architecture Decision: Modified {os.path.basename(file_path)}"
        elif tool_name == "create_plan":
            title = "Architecture Decision: Plan Creation Approach"
        elif tool_name == "update_plan":
            title = "Architecture Decision: Plan Update Strategy"
        else:
            title = f"Architecture Decision: {tool_name} Execution"

        # Generate context
        context_text = f"""
Execution Context:
- Ticket: {ticket_title}
- Phase: {execution_phase}
- Tool: {tool_name}
- Timestamp: {datetime.utcnow().isoformat()}

Tool Arguments:
{tool_args}

Execution Context:
{context}
"""

        # Generate decision
        if tool_name == "write_file":
            file_path = tool_args.get("file_path", "")
            content = tool_args.get("content", "")
            decision = f"Created new file {file_path} with architectural significance. This file represents a key architectural component or decision in the implementation."
        elif tool_name == "edit_file":
            file_path = tool_args.get("file_path", "")
            changes = tool_args.get("changes", "")
            decision = f"Modified file {file_path} with architectural changes. The modifications represent significant architectural decisions or improvements."
        elif tool_name == "create_plan":
            decision = "Created implementation plan using stakeholder-driven approach. This plan incorporates multi-stakeholder perspectives and architectural considerations."
        elif tool_name == "update_plan":
            decision = "Updated implementation plan based on execution feedback. This update reflects architectural decisions made during implementation."
        else:
            decision = f"Executed {tool_name} as part of architectural implementation. This execution represents a key architectural decision or component."

        # Generate consequences
        consequences = f"""
This decision has the following consequences:

1. **Implementation Impact**: This decision affects the overall system architecture and implementation approach.

2. **Future Maintenance**: Future changes to this component will need to consider the architectural decisions made here.

3. **System Integration**: This decision may impact how other components integrate with this part of the system.

4. **Documentation**: This ADR serves as documentation for future developers and architects.

5. **Traceability**: This decision is now traceable through the ADR system for future reference and analysis.
"""

        return {"title": title, "context": context_text, "decision": decision, "consequences": consequences}

    def get_adr_summary(self) -> dict[str, Any]:
        """Get summary of captured ADRs."""
        if not self.enabled or not self.adr_manager:
            return {"enabled": False, "total_decisions": 0, "adr_directory": None}

        return {
            "enabled": True,
            "total_decisions": self.decision_count,
            "adr_directory": self.adr_manager.output_directory,
            "adr_manager_available": True,
        }


def create_adr_integration_hook(workspace_root: str, enabled: bool = True) -> ADRIntegrationHook:
    """
    Create an ADR integration hook for deep agents execution.

    Args:
        workspace_root: Root directory for ADR storage
        enabled: Whether ADR capture is enabled

    Returns:
        Configured ADR integration hook
    """
    return ADRIntegrationHook(workspace_root=workspace_root, enabled=enabled)
