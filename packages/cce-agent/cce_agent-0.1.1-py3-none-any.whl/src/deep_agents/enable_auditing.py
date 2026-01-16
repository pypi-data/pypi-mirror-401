"""
Enable Context Auditing for Deep Agents

This script demonstrates how to enable comprehensive context auditing
in the deep agents system for debugging context explosion issues.
"""

import logging
import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.deep_agents.cce_deep_agent import createCCEDeepAgent


def main():
    """Enable context auditing in deep agents."""
    print("🔍 Enabling Context Auditing for Deep Agents...")

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Create deep agent with auditing enabled
        print("  🤖 Creating deep agent with context auditing enabled...")

        deep_agent = createCCEDeepAgent(
            llm=None,  # Will create default LLM
            context_mode="trim",
            enable_memory_persistence=True,
            enable_context_auditing=True,  # Enable comprehensive auditing
        )

        print("  ✅ Deep agent created with context auditing enabled!")
        print("  📁 Audit files will be written to: .artifacts/context_audit/")
        print("  📊 Each LLM call, post-hook, and tool call will be audited")
        print("  🔍 Check the audit files to identify context explosion sources")

        return deep_agent

    except Exception as e:
        print(f"  ❌ Failed to create deep agent with auditing: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    deep_agent = main()
    if deep_agent:
        print("\n🎉 Context auditing is now enabled!")
        print("📋 Next steps:")
        print("  1. Run your deep agents workflow")
        print("  2. Check .artifacts/context_audit/ for detailed audit files")
        print("  3. Look for large token counts in the audit files")
        print("  4. Identify which calls are causing context explosion")
    else:
        print("\n❌ Failed to enable context auditing")
