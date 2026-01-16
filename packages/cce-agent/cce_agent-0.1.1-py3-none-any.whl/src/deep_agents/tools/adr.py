"""
ADR Tools for Deep Agents

This module provides tools for managing Architecture Decision Records (ADRs)
during deep agents execution, allowing agents to create, view, and manage ADRs
as part of their workflow.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool

# Import ADR system from stakeholder generator
try:
    from ...stakeholder_generator.adr import ADRManager, ArchitectureDecision
except ImportError:
    # Fallback if stakeholder generator not available
    ADRManager = None
    ArchitectureDecision = None

logger = logging.getLogger(__name__)

# ADR manager instances cache
_adr_manager_instances: dict[str, ADRManager] = {}


def get_adr_manager(workspace_root: str) -> ADRManager | None:
    """Get or create ADR manager instance for specific workspace."""
    if workspace_root not in _adr_manager_instances and ADRManager:
        try:
            # Ensure workspace root exists
            os.makedirs(workspace_root, exist_ok=True)
            _adr_manager_instances[workspace_root] = ADRManager(output_directory=workspace_root)
            logger.info(f"✅ ADR manager initialized for workspace: {workspace_root}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize ADR manager for {workspace_root}: {e}")
            return None

    return _adr_manager_instances.get(workspace_root)


@tool
def create_adr_tool(
    title: str, context: str, decision: str, consequences: str, status: str = "Accepted", workspace_root: str = "."
) -> str:
    """
    Create a new Architecture Decision Record (ADR).

    Args:
        title: Title of the ADR
        context: Context and background information
        decision: The architectural decision made
        consequences: Consequences and implications of the decision
        status: Status of the decision (default: "Accepted")
        workspace_root: Root directory for ADR storage

    Returns:
        Status message about ADR creation
    """
    try:
        adr_manager = get_adr_manager(workspace_root)
        if not adr_manager:
            return "❌ ADR system not available - cannot create ADR"

        # Create the ADR
        adr = adr_manager.create_adr(
            title=title, context=context, decision=decision, consequences=consequences, status=status
        )

        logger.info(f"📝 ADR created: {adr.title}")
        return f"✅ ADR created successfully: {adr.title}"

    except Exception as e:
        logger.error(f"❌ Failed to create ADR: {e}")
        return f"❌ Failed to create ADR: {str(e)}"


@tool
def list_adrs_tool(workspace_root: str = ".", limit: int = 10) -> str:
    """
    List recent Architecture Decision Records (ADRs).

    Args:
        workspace_root: Root directory for ADR storage
        limit: Maximum number of ADRs to return

    Returns:
        Formatted list of recent ADRs
    """
    try:
        adr_manager = get_adr_manager(workspace_root)
        if not adr_manager:
            return "❌ ADR system not available - cannot list ADRs"

        # Get ADR directory
        adr_directory = adr_manager.output_directory

        if not os.path.exists(adr_directory):
            return "📝 No ADRs found - ADR directory does not exist"

        # List ADR files
        adr_files = [f for f in os.listdir(adr_directory) if f.endswith(".json")]
        adr_files.sort(reverse=True)  # Most recent first

        if not adr_files:
            return "📝 No ADRs found"

        # Load and format ADRs
        adrs = []
        for adr_file in adr_files[:limit]:
            try:
                with open(os.path.join(adr_directory, adr_file)) as f:
                    adr_data = json.load(f)
                    adrs.append(adr_data)
            except Exception as e:
                logger.warning(f"⚠️ Failed to load ADR file {adr_file}: {e}")

        if not adrs:
            return "📝 No valid ADRs found"

        # Format output
        output = f"📝 Recent ADRs (showing {len(adrs)} of {len(adr_files)}):\n\n"

        for i, adr in enumerate(adrs, 1):
            output += f"{i}. **{adr.get('title', 'Untitled')}**\n"
            output += f"   Status: {adr.get('status', 'Unknown')}\n"
            output += f"   Date: {adr.get('timestamp', 'Unknown')}\n"
            output += f"   Decision: {adr.get('decision', 'No decision recorded')[:100]}...\n\n"

        return output

    except Exception as e:
        logger.error(f"❌ Failed to list ADRs: {e}")
        return f"❌ Failed to list ADRs: {str(e)}"


@tool
def get_adr_tool(adr_title: str, workspace_root: str = ".") -> str:
    """
    Get details of a specific Architecture Decision Record (ADR).

    Args:
        adr_title: Title or partial title of the ADR to retrieve
        workspace_root: Root directory for ADR storage

    Returns:
        Detailed ADR information
    """
    try:
        adr_manager = get_adr_manager(workspace_root)
        if not adr_manager:
            return "❌ ADR system not available - cannot retrieve ADR"

        # Get ADR directory
        adr_directory = adr_manager.output_directory

        if not os.path.exists(adr_directory):
            return "❌ ADR directory does not exist"

        # Search for ADR files
        adr_files = [f for f in os.listdir(adr_directory) if f.endswith(".json")]

        # Find matching ADR
        matching_adr = None
        for adr_file in adr_files:
            try:
                with open(os.path.join(adr_directory, adr_file)) as f:
                    adr_data = json.load(f)
                    if adr_title.lower() in adr_data.get("title", "").lower():
                        matching_adr = adr_data
                        break
            except Exception as e:
                logger.warning(f"⚠️ Failed to load ADR file {adr_file}: {e}")

        if not matching_adr:
            return f"❌ ADR not found: {adr_title}"

        # Format detailed output
        output = f"📝 ADR Details: {matching_adr.get('title', 'Untitled')}\n\n"
        output += f"**Status**: {matching_adr.get('status', 'Unknown')}\n"
        output += f"**Date**: {matching_adr.get('timestamp', 'Unknown')}\n\n"
        output += f"**Context**:\n{matching_adr.get('context', 'No context provided')}\n\n"
        output += f"**Decision**:\n{matching_adr.get('decision', 'No decision recorded')}\n\n"
        output += f"**Consequences**:\n{matching_adr.get('consequences', 'No consequences recorded')}\n"

        return output

    except Exception as e:
        logger.error(f"❌ Failed to get ADR: {e}")
        return f"❌ Failed to get ADR: {str(e)}"


@tool
def adr_summary_tool(workspace_root: str = ".") -> str:
    """
    Get summary of all Architecture Decision Records (ADRs).

    Args:
        workspace_root: Root directory for ADR storage

    Returns:
        Summary of ADR system status and statistics
    """
    try:
        adr_manager = get_adr_manager(workspace_root)
        if not adr_manager:
            return "❌ ADR system not available"

        # Get ADR directory
        adr_directory = adr_manager.output_directory

        if not os.path.exists(adr_directory):
            return "📝 ADR system initialized but no ADRs created yet"

        # Count ADR files
        adr_files = [f for f in os.listdir(adr_directory) if f.endswith(".json")]

        if not adr_files:
            return "📝 ADR system active but no ADRs created yet"

        # Analyze ADRs
        status_counts = {}
        recent_adrs = []

        for adr_file in adr_files:
            try:
                with open(os.path.join(adr_directory, adr_file)) as f:
                    adr_data = json.load(f)
                    status = adr_data.get("status", "Unknown")
                    status_counts[status] = status_counts.get(status, 0) + 1

                    # Keep track of recent ADRs
                    recent_adrs.append(
                        {
                            "title": adr_data.get("title", "Untitled"),
                            "status": status,
                            "timestamp": adr_data.get("timestamp", "Unknown"),
                        }
                    )
            except Exception as e:
                logger.warning(f"⚠️ Failed to load ADR file {adr_file}: {e}")

        # Sort by timestamp (most recent first)
        recent_adrs.sort(key=lambda x: x["timestamp"], reverse=True)

        # Format summary
        output = f"📊 ADR System Summary\n\n"
        output += f"**Total ADRs**: {len(adr_files)}\n"
        output += f"**ADR Directory**: {adr_directory}\n\n"

        if status_counts:
            output += f"**Status Breakdown**:\n"
            for status, count in status_counts.items():
                output += f"  - {status}: {count}\n"
            output += "\n"

        if recent_adrs:
            output += f"**Recent ADRs** (last 5):\n"
            for i, adr in enumerate(recent_adrs[:5], 1):
                output += f"  {i}. {adr['title']} ({adr['status']})\n"

        return output

    except Exception as e:
        logger.error(f"❌ Failed to get ADR summary: {e}")
        return f"❌ Failed to get ADR summary: {str(e)}"


# Export tools for use in deep agents
ADR_TOOLS = [create_adr_tool, list_adrs_tool, get_adr_tool, adr_summary_tool]
