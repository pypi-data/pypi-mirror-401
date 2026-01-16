#!/usr/bin/env python3
"""
Run the CCE Agent on a GitHub issue with automatic extraction.

This script demonstrates the complete CCE workflow and supports CLI arguments
for selecting the target issue and running extraction-only checks.
"""

import argparse
import asyncio
import os
import re
import sys

# Add project to path
sys.path.insert(0, os.path.abspath("."))

from src.agent import CCEAgent
from src.models import Ticket
from src.tools.github_extractor import extract_ticket_from_url
from src.tools.shell_runner import ShellRunner

DEFAULT_ISSUE_URL = "https://github.com/jkbrooks/personal_project_management/issues/140"


def _extract_issue_number(issue_url: str) -> int | None:
    match = re.search(r"/issues/(\\d+)", issue_url)
    return int(match.group(1)) if match else None


async def run_issue(issue_url: str) -> bool:
    """Run CCE workflow on a GitHub issue with automatic extraction."""

    print("🚀 Starting CCE Agent with GitHub Extraction")
    print("=" * 60)

    print(f"📋 Target Issue: {issue_url}")

    # 1. Initialize components
    shell_runner = ShellRunner()
    ticket = None

    # 2. Extract ticket data from GitHub
    print("\n🔍 Phase 0: GitHub Ticket Extraction...")
    print("-" * 40)

    try:
        print("⏳ Fetching issue data from GitHub...")
        ticket = await extract_ticket_from_url(issue_url, shell_runner)

        if ticket is None:
            print("❌ Failed to extract GitHub issue data")
            print("💡 Possible solutions:")
            print("   - Install gh CLI: `brew install gh` or `apt install gh-cli`")
            print("   - Authenticate: `gh auth login`")
            print("   - Check network connectivity")
            print("   - Verify issue URL is accessible")

            # Fallback to manual ticket creation
            print("\n🔄 Falling back to manual ticket creation...")
            issue_number = _extract_issue_number(issue_url) or 0
            issue_label = f"#{issue_number}" if issue_number else "unknown"
            ticket = Ticket(
                number=issue_number,
                title=f"GitHub Issue {issue_label} (Manual Fallback)",
                description="Failed to automatically extract issue data. Please check gh CLI setup.",
                url=issue_url,
                state="unknown",
                author="unknown",
            )
        else:
            print("✅ GitHub extraction successful!")
            print(f"   📋 Issue: #{ticket.number} - {ticket.title}")
            print(f"   👤 Author: {ticket.author}")
            print(f"   🏷️  State: {ticket.state}")
            print(f"   📝 Labels: {', '.join(ticket.labels) if ticket.labels else 'None'}")
            print(f"   👥 Assignees: {', '.join(ticket.assignees) if ticket.assignees else 'None'}")
            print(f"   🎯 Milestone: {ticket.milestone or 'None'}")
            print(f"   💬 Comments: {len(ticket.comments)}")
            print(f"   😊 Reactions: {dict(ticket.reactions) if ticket.reactions else 'None'}")

            # Show description preview
            description_preview = (
                ticket.description[:200] + "..." if len(ticket.description) > 200 else ticket.description
            )
            print(f"   📄 Description: {description_preview}")

            # Show top comments
            if ticket.comments:
                print(f"\n   💬 Recent Comments:")
                for i, comment in enumerate(ticket.comments[:2]):
                    comment_preview = comment.body[:100] + "..." if len(comment.body) > 100 else comment.body
                    print(f"      {i + 1}. @{comment.author}: {comment_preview}")
                if len(ticket.comments) > 2:
                    print(f"      ... and {len(ticket.comments) - 2} more comments")

    except Exception as e:
        print(f"❌ GitHub extraction failed: {e}")
        print("\n🔄 Creating fallback ticket...")

        # Fallback ticket
        issue_number = _extract_issue_number(issue_url) or 0
        issue_label = f"#{issue_number}" if issue_number else "unknown"
        ticket = Ticket(
            number=issue_number,
            title=f"GitHub Issue {issue_label} (Extraction Failed)",
            description=f"Extraction failed with error: {e}. Please check GitHub access and try again.",
            url=issue_url,
            state="unknown",
            author="unknown",
        )

    # 3. Initialize CCE Agent
    print(f"\n🤖 Initializing CCE Agent...")
    workspace_root = os.path.abspath(".")
    agent = CCEAgent(workspace_root=workspace_root)

    # 4. Run CCE workflow using process_ticket method
    print(f"\n🚀 Running Complete CCE Workflow...")
    print("-" * 40)
    print("🎯 Processing ticket through full CCE pipeline...")

    # Initialize success variables
    planning_success = False
    orientation_success = False
    execution_success = False
    reconciliation_success = False
    workflow_success = False

    try:
        # Use the main process_ticket method which handles the entire workflow
        result = await agent.process_ticket(ticket)

        # Check if the result has the expected attributes
        workflow_success = hasattr(result, "status") and result.status in ["success", "completed"]
        print(f"📊 CCE Workflow: {'✅ Success' if workflow_success else '⚠️ Completed with issues'}")

        if hasattr(result, "final_summary") and result.final_summary:
            summary_preview = (
                result.final_summary[:200] + "..." if len(result.final_summary) > 200 else result.final_summary
            )
            print(f"📝 Final Summary: {summary_preview}")

        if hasattr(result, "execution_cycles") and result.execution_cycles:
            print(f"🔄 Execution Cycles: {len(result.execution_cycles)}")

        if hasattr(result, "planning_result") and result.planning_result:
            planning_success = hasattr(result.planning_result, "status") and result.planning_result.status == "success"
            print(f"📋 Planning: {'✅ Success' if planning_success else '⚠️ Issues'}")

        # Set success status based on workflow completion
        if workflow_success:
            planning_success = True
            orientation_success = True
            execution_success = True
            reconciliation_success = True

    except Exception as e:
        print(f"❌ CCE workflow failed: {e}")
        result = None
        workflow_success = False

    # 5. Run intelligent tests on changes (separate from main workflow)
    print(f"\n🧪 Phase 5: Intelligent Test Execution...")
    print("-" * 40)
    print("🎯 Running intelligent test selection based on changes...")

    try:
        from src.tools.commands.run_tests import run_tests

        # Use the correct parameter name for run_tests
        test_result = await run_tests.ainvoke({"test_type": "changes"})  # Uses intelligent selection!
        print(f"📊 Test Execution: {test_result}")

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        test_result = "❌ Failed"

    # 6. Final Summary
    print(f"\n" + "=" * 60)
    print(f"📊 CCE WORKFLOW SUMMARY")
    print(f"=" * 60)

    print(f"🎫 Issue: #{ticket.number} - {ticket.title}")
    print(f"🔗 URL: {ticket.url}")
    print(f"👤 Author: {ticket.author}")
    print(f"🏷️  State: {ticket.state}")

    if ticket.labels:
        print(f"📝 Labels: {', '.join(ticket.labels)}")
    if ticket.assignees:
        print(f"👥 Assignees: {', '.join(ticket.assignees)}")
    if ticket.milestone:
        print(f"🎯 Milestone: {ticket.milestone}")

    print(f"\n📈 Phase Results:")
    print(f"   📋 Planning: {'✅ Success' if planning_success else '❌ Failed'}")
    print(f"   🎯 Orientation: {'✅ Success' if orientation_success else '❌ Failed'}")
    print(f"   ⚡ Execution: {'✅ Success' if execution_success else '❌ Failed'}")
    print(f"   🔄 Reconciliation: {'✅ Success' if reconciliation_success else '❌ Failed'}")
    print(f"   🧪 Testing: {test_result}")

    total_phases = 5
    test_success = "✅" in str(test_result) or "Success" in str(test_result)
    successful_phases = sum(
        [
            1 if planning_success else 0,
            1 if orientation_success else 0,
            1 if execution_success else 0,
            1 if reconciliation_success else 0,
            1 if test_success else 0,
        ]
    )

    success_rate = (successful_phases / total_phases) * 100
    print(f"\n🎯 Overall Success Rate: {successful_phases}/{total_phases} ({success_rate:.1f}%)")

    if success_rate >= 80:
        print("\n🎉 CCE Workflow completed successfully!")
        if ticket:
            print(f"✅ Issue #{ticket.number} has been processed with high success rate.")
    elif success_rate >= 50:
        print("\n⚠️  CCE Workflow completed with mixed results.")
        print("🔧 Some phases need attention. Review the logs above.")
    else:
        print("\n❌ CCE Workflow encountered significant issues.")
        print("🚨 Multiple phases failed. Check system configuration and logs.")

    print("\n💡 Next Steps:")
    if ticket and hasattr(ticket, "comments") and len(ticket.comments) > 0:
        print(f"   - Review {len(ticket.comments)} comments from GitHub for additional context")
    print("   - Check generated artifacts and implementation results")
    print("   - Validate changes against issue requirements")
    print("   - Consider creating follow-up issues for any remaining work")

    return success_rate >= 80


async def test_extraction_only(issue_url: str) -> bool:
    """Quick test of just the GitHub extraction functionality."""
    print("🔍 Testing GitHub Extraction Only")
    print("=" * 40)
    shell_runner = ShellRunner()

    try:
        ticket = await extract_ticket_from_url(issue_url, shell_runner)

        if ticket:
            print("✅ Extraction successful!")
            print(f"   Issue: #{ticket.number} - {ticket.title}")
            print(f"   Author: {ticket.author}")
            print(f"   Comments: {len(ticket.comments)}")
            print(f"   Labels: {', '.join(ticket.labels)}")
            return True
        else:
            print(f"❌ Extraction failed - no ticket returned")
            return False

    except Exception as e:
        print(f"❌ Extraction crashed: {e}")
        return False


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the CCE workflow on a GitHub issue.")
    parser.add_argument(
        "issue_url",
        nargs="?",
        default=DEFAULT_ISSUE_URL,
        help="GitHub issue URL to process",
    )
    parser.add_argument(
        "--test-extraction",
        action="store_true",
        help="Run extraction only without executing the full workflow",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.test_extraction:
        success = asyncio.run(test_extraction_only(args.issue_url))
    else:
        success = asyncio.run(run_issue(args.issue_url))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
