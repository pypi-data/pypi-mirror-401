#!/usr/bin/env python3
"""
Run CCE Agent on GitHub Issue #140 with Deep Agents Integration

This script demonstrates the complete CCE workflow using the new deep agents integration.
It fetches the real issue data from GitHub and runs the full CCE analysis and implementation
using the deep agents approach for enhanced LLM-based code editing and sub-agent coordination.
"""

import asyncio
import os
import sys

# Add project to path
sys.path.insert(0, os.path.abspath("."))

from langchain_core.messages import HumanMessage

from src.deep_agents.cce_deep_agent import createCCEDeepAgent, get_cce_deep_agent_tools
from src.graphs.utils import get_graph_orchestration_manager
from src.models import Ticket
from src.tools.github_extractor import extract_ticket_from_url
from src.tools.shell_runner import ShellRunner

_READ_ONLY_ENV = "DEEP_AGENTS_READ_ONLY"


def _parse_read_only_args(argv: list[str]) -> tuple[bool, list[str]]:
    read_only = False
    env_value = os.getenv(_READ_ONLY_ENV)
    if env_value is not None:
        read_only = env_value.strip().lower() not in ("0", "false", "no", "off")

    remaining: list[str] = []
    for arg in argv:
        if arg == "--edit":
            read_only = False
        elif arg == "--read-only":
            read_only = True
        else:
            remaining.append(arg)

    return read_only, remaining


def _build_instruction(ticket: Ticket, read_only: bool) -> str:
    if read_only:
        constraints = [
            "- Do NOT modify files or run git commands.",
            "- Produce a concise plan and risk assessment only.",
            "- Provide a final summary at the end.",
            "- Call signal_cycle_complete when finished.",
        ]
    else:
        constraints = [
            "- Do NOT run git commands.",
            "- You MAY read and modify files in the workspace to implement the ticket.",
            "- Start with a concise plan and risk assessment, then implement the highest-priority changes.",
            "- If you modify files, sync them to disk before completing.",
            "- Provide a final summary at the end.",
            "- Call signal_cycle_complete when finished.",
        ]

    return (
        "You are running the CCE workflow in deep agents mode.\n\n"
        f"Ticket #{ticket.number}: {ticket.title}\n"
        f"URL: {ticket.url}\n\n"
        "Ticket Body:\n"
        f"{ticket.description}\n\n"
        "Constraints:\n"
        f"{chr(10).join(constraints)}\n"
    )


def _create_deep_agent():
    """Create a deep agent with the best available LLM configuration."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return createCCEDeepAgent()

    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:
            raise RuntimeError("OPENAI_API_KEY set but langchain_openai is unavailable") from exc

        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        return createCCEDeepAgent(llm=llm)

    raise RuntimeError("Missing ANTHROPIC_API_KEY or OPENAI_API_KEY for deep agents execution")


async def run_issue_with_deep_agents(issue_url, read_only: bool):
    """Run CCE workflow on a specified GitHub issue with deep agents integration."""

    print("🤖 Starting CCE Agent with Deep Agents Integration")
    print("=" * 60)

    # GitHub issue URL (now passed as parameter)
    print(f"📋 Target Issue: {issue_url}")
    print(f"🚀 Mode: Deep Agents Integration (Enhanced LLM-based code editing)")

    # 1. Initialize components
    shell_runner = ShellRunner()

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
            ticket = Ticket(
                number=140,
                title="GitHub Issue #140 (Manual Fallback)",
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
        ticket = Ticket(
            number=140,
            title="GitHub Issue #140 (Extraction Failed)",
            description=f"Extraction failed with error: {e}. Please check GitHub access and try again.",
            url=issue_url,
            state="unknown",
            author="unknown",
        )

    # 3. Initialize Deep Agent
    print(f"\n🤖 Initializing CCE Deep Agent...")
    print("-" * 40)

    deep_agent = None
    try:
        deep_agent = _create_deep_agent()
        print("✅ Deep agent created successfully!")
        print(f"   🧠 Deep agent: {type(deep_agent).__name__}")
        print(f"   🔧 invoke_with_filesystem: {hasattr(deep_agent, 'invoke_with_filesystem')}")
    except Exception as e:
        print(f"❌ Deep agent initialization failed: {e}")
        return False

    # Best-effort git context (no workflow integration here)
    current_branch_result = shell_runner.execute("git branch --show-current")
    if current_branch_result.exit_code == 0:
        print(f"🌿 Current branch: {current_branch_result.stdout.strip()}")
    else:
        print("🌿 Current branch: unknown (git not available)")

    # 4. Test Deep Agents Sub-Agent Capabilities
    print(f"\n🔬 Phase 1: Deep Agents Capability Test...")
    print("-" * 40)

    orchestration_manager = None
    try:
        # Test sub-agent delegation
        print("🧪 Testing sub-agent delegation capabilities...")

        # Import deep agents components for testing
        from src.deep_agents.stakeholder_agents import ALL_STAKEHOLDER_AGENTS
        from src.deep_agents.task_delegation import TaskDelegator

        task_delegator = TaskDelegator()
        print(f"✅ Task delegator initialized successfully")
        print(f"   Available stakeholder agents: {len(ALL_STAKEHOLDER_AGENTS)}")
        print(f"   Agent types: {', '.join([agent['name'] for agent in ALL_STAKEHOLDER_AGENTS])}")

        # Test planning tools
        from src.deep_agents.tools.planning import PLANNING_TOOLS

        print(f"✅ Planning tools available: {len(PLANNING_TOOLS)} tools")

        # Test tool availability
        available_tools = [tool for tool in get_cce_deep_agent_tools() if hasattr(tool, "name")]
        tool_names = {tool.name for tool in available_tools}
        bash_tool_present = "execute_bash_command" in tool_names or "execute_bash" in tool_names
        print(f"✅ Tool registry: {len(tool_names)} tools available")
        print(f"   execute_bash_command available: {'✅' if bash_tool_present else '❌'}")

        orchestration_manager = get_graph_orchestration_manager()
        available_graphs = orchestration_manager.get_available_graphs()
        print(f"✅ Graph orchestration: {', '.join(available_graphs) if available_graphs else 'None'}")

    except Exception as e:
        print(f"⚠️  Deep agents capability test failed: {e}")
        print("   Continuing with basic deep agents functionality...")

    # 5. Run CCE workflow using deep agents approach
    print(f"\n🚀 Running CCE Workflow with Deep Agents...")
    print("-" * 40)
    print("🎯 Processing ticket through enhanced deep agents pipeline...")

    workflow_success = False
    result = None

    try:
        instruction = _build_instruction(ticket, read_only)
        message = HumanMessage(content=instruction)

        config = {"configurable": {"thread_id": f"deep-agents-{ticket.number}"}}

        timeout_raw = os.getenv("DEEP_AGENTS_TIMEOUT_SECONDS", "2400")
        try:
            timeout_seconds = int(timeout_raw)
        except ValueError:
            print(f"⚠️  Invalid DEEP_AGENTS_TIMEOUT_SECONDS={timeout_raw}; defaulting to 2400s")
            timeout_seconds = 2400

        max_cycles = None
        try:
            from src.config import get_max_execution_cycles

            max_cycles = get_max_execution_cycles()
        except Exception:
            max_cycles = None

        if hasattr(deep_agent, "run_with_cycles"):
            run_coro = deep_agent.run_with_cycles(
                [message],
                context_memory={"ticket_url": ticket.url},
                remaining_steps=500,
                execution_phases=[{"cycle_count": 0, "phase": "ticket_processing"}],
                max_cycles=max_cycles,
                config=config,
            )
        elif hasattr(deep_agent, "invoke_with_filesystem"):
            run_coro = deep_agent.invoke_with_filesystem(
                [message],
                context_memory={"ticket_url": ticket.url},
                remaining_steps=500,
                execution_phases=[{"cycle_count": 0, "phase": "ticket_processing"}],
                config=config,
            )
        else:
            run_coro = deep_agent.ainvoke(
                {
                    "messages": [message],
                    "remaining_steps": 500,
                    "context_memory": {"ticket_url": ticket.url},
                    "execution_phases": [{"cycle_count": 0, "phase": "ticket_processing"}],
                },
                config=config,
            )

        if timeout_seconds > 0:
            result = await asyncio.wait_for(run_coro, timeout=timeout_seconds)
        else:
            result = await run_coro

        workflow_success = isinstance(result, dict) and bool(result.get("messages"))
        print(f"📊 Deep Agents CCE Workflow: {'✅ Success' if workflow_success else '⚠️ Completed with issues'}")

        if isinstance(result, dict):
            messages = result.get("messages") or []
            if messages:
                last_message = messages[-1]
                content = getattr(last_message, "content", str(last_message))
                summary_preview = content[:200] + "..." if len(content) > 200 else content
                print(f"📝 Final Summary: {summary_preview}")

            if result.get("todos"):
                print(f"🗒️  Todos: {len(result['todos'])}")

    except TimeoutError:
        print(f"⏰ Deep agents CCE workflow timed out after {timeout_seconds}s")
        return False
    except Exception as e:
        print(f"❌ Deep agents CCE workflow failed: {e}")
        print(f"   Error details: {type(e).__name__}: {str(e)}")
        return False

    # 6. Final Summary
    print(f"\n" + "=" * 60)
    print(f"📊 DEEP AGENTS CCE WORKFLOW SUMMARY")
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

    print(f"\n🤖 Deep Agents Integration:")
    print(f"   🧠 Deep Agent: {'✅ Enabled' if deep_agent else '❌ Disabled'}")
    print(f"   📊 Graph Orchestration: {'✅ Available' if orchestration_manager else '❌ Not Available'}")
    print(f"   🔧 Tool Integration: {'✅ Active' if deep_agent else '❌ Traditional'}")
    print(f"   🎯 Sub-Agent Delegation: {'✅ Available' if deep_agent else '❌ Not Available'}")

    print(f"\n📈 Workflow Result:")
    print(f"   ⚡ Execution: {'✅ Success' if workflow_success else '❌ Failed'}")

    if workflow_success:
        print(f"\n🎉 Deep Agents CCE Workflow completed successfully!")
        print(f"✅ Issue #{ticket.number} has been processed using deep agents.")
        print(f"🚀 Enhanced capabilities: LLM-based code editing, sub-agent coordination, advanced planning")
    else:
        print(f"\n❌ Deep Agents CCE Workflow encountered issues.")
        print(f"🚨 Check deep agents configuration and logs.")

    return workflow_success


async def check_deep_agents_only():
    """Quick test of just the deep agents integration functionality."""
    print("🤖 Testing Deep Agents Integration Only")
    print("=" * 40)

    try:
        deep_agent = _create_deep_agent()
        print(f"✅ Deep agents integration successful!")
        print(f"   🧠 Deep agent type: {type(deep_agent).__name__}")
        print(f"   🔗 invoke_with_filesystem: {hasattr(deep_agent, 'invoke_with_filesystem')}")

        available_tools = [tool for tool in get_cce_deep_agent_tools() if hasattr(tool, "name")]
        tool_names = {tool.name for tool in available_tools}
        bash_tool_present = "execute_bash_command" in tool_names or "execute_bash" in tool_names
        print(f"   🔧 Tools available: {len(tool_names)}")
        print(f"   📦 execute_bash_command available: {'✅' if bash_tool_present else '❌'}")

        orchestration_manager = get_graph_orchestration_manager()
        print(f"   📊 Graphs available: {orchestration_manager.get_available_graphs()}")

        return True

    except Exception as e:
        print(f"❌ Deep agents test crashed: {e}")
        return False


if __name__ == "__main__":
    print("🤖 CCE Agent with Deep Agents Integration")

    read_only, args = _parse_read_only_args(sys.argv[1:])

    # Parse command line arguments
    if len(args) < 1:
        print("Usage: python run_process_ticket_deep_agents.py <issue_url> [test] [--edit|--read-only]")
        print("Examples:")
        print("  python run_process_ticket_deep_agents.py https://github.com/owner/repo/issues/123")
        print("  python run_process_ticket_deep_agents.py https://github.com/owner/repo/issues/123 --edit")
        print("  python run_process_ticket_deep_agents.py https://github.com/owner/repo/issues/123 --read-only")
        print("  python run_process_ticket_deep_agents.py https://github.com/owner/repo/issues/123 test")
        print("  python run_process_ticket_deep_agents.py test  # Test deep agents only")
        print("  DEEP_AGENTS_READ_ONLY=0 python run_process_ticket_deep_agents.py <issue_url>")
        sys.exit(1)

    # Check if first argument is "test" (for backwards compatibility)
    if args[0] == "test":
        print("\n🔍 Running deep agents integration test only...")
        success = asyncio.run(check_deep_agents_only())
    elif len(args) > 1 and args[1] == "test":
        # Issue URL provided as first arg, "test" as second arg
        print("\n🔍 Running deep agents integration test only...")
        success = asyncio.run(check_deep_agents_only())
    else:
        # Issue URL provided as first argument
        issue_url = args[0]
        print(f"\n⚡ Running full CCE workflow with deep agents on: {issue_url}")
        success = asyncio.run(run_issue_with_deep_agents(issue_url, read_only))

    if success:
        print("\n🎯 Deep agents integration ready for production use!")
    else:
        print("\n🔧 Issues detected with deep agents - please review output above")

    sys.exit(0 if success else 1)
