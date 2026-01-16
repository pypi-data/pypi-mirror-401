#!/usr/bin/env python3
"""
Basic Deep Agents Integration Test

This script tests the basic deep agents integration functionality
without running the full CCE workflow.
"""

import asyncio
import os
import sys

import pytest

# Add project to path
sys.path.insert(0, os.path.abspath("."))

from src.deep_agents.cce_deep_agent import createCCEDeepAgent, get_cce_deep_agent_tools
from src.graphs.utils import get_graph_orchestration_manager


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


@pytest.mark.asyncio
async def test_deep_agents_basic():
    """Test basic deep agents integration functionality."""

    print("🧠 Testing Basic Deep Agents Integration")
    print("=" * 50)

    orchestration_manager = None
    try:
        # Initialize CCE Deep Agent
        print("🤖 Initializing CCE Deep Agent...")
        deep_agent = _create_deep_agent()
        print("✅ Deep agent created successfully!")

        # Test 1: Deep Agents Integration Status
        print("\n📊 Test 1: Deep Agents Integration Status")
        print("-" * 40)

        if deep_agent is not None:
            print("✅ Deep Agents Integration: ENABLED")
            print(f"   🧠 Deep Agent Type: {type(deep_agent).__name__}")
        else:
            print("❌ Deep Agents Integration: DISABLED")
            return False

        # Test 2: Invocation Helper
        print("\n📊 Test 2: Invocation Helper")
        print("-" * 40)

        if hasattr(deep_agent, "invoke_with_filesystem"):
            print("✅ invoke_with_filesystem: Available")
        else:
            print("❌ invoke_with_filesystem: Not Available")

        # Test 3: Graph Orchestration
        print("\n📊 Test 3: Graph Orchestration")
        print("-" * 40)

        orchestration_manager = get_graph_orchestration_manager()
        if orchestration_manager:
            print("✅ Graph Orchestration Manager: Available")
            print(f"   🔧 Manager Type: {type(orchestration_manager).__name__}")

            # Test available graphs
            try:
                available_graphs = orchestration_manager.get_available_graphs()
                print(f"   📈 Available Graphs: {available_graphs}")

                if available_graphs:
                    print("   ✅ Graph Discovery: Working")
                else:
                    print("   ⚠️  Graph Discovery: No graphs available")

            except Exception as e:
                print(f"   ❌ Graph Discovery: Failed - {e}")
        else:
            print("❌ Graph Orchestration Manager: Not Available")

        # Test 4: Tool Integration
        print("\n📊 Test 4: Tool Integration")
        print("-" * 40)

        available_tools = [tool for tool in get_cce_deep_agent_tools() if hasattr(tool, "name")]
        tool_names = {tool.name for tool in available_tools}
        bash_tool_present = "execute_bash_command" in tool_names or "execute_bash" in tool_names
        if tool_names:
            print("✅ Tool Registry: Available")
            print(f"   🛠️  Tools count: {len(tool_names)}")
            print(f"   🧪 execute_bash_command present: {'✅' if bash_tool_present else '❌'}")
        else:
            print("❌ Tool Registry: Not Available")

        # Summary
        print("\n" + "=" * 50)
        print("📊 DEEP AGENTS INTEGRATION TEST SUMMARY")
        print("=" * 50)

        tests_passed = 0
        total_tests = 4

        if deep_agent is not None:
            tests_passed += 1
        if hasattr(deep_agent, "invoke_with_filesystem"):
            tests_passed += 1
        if orchestration_manager:
            tests_passed += 1
        if tool_names:
            tests_passed += 1

        success_rate = (tests_passed / total_tests) * 100

        print(f"🎯 Tests Passed: {tests_passed}/{total_tests} ({success_rate:.1f}%)")

        if success_rate >= 80:
            print("🎉 Deep Agents Integration: READY FOR PRODUCTION")
            print("✅ All core components are working properly")
            return True
        elif success_rate >= 50:
            print("⚠️  Deep Agents Integration: PARTIALLY WORKING")
            print("🔧 Some components need attention")
            return False
        else:
            print("❌ Deep Agents Integration: NEEDS WORK")
            print("🚨 Multiple components are not working")
            return False

    except Exception as e:
        print(f"❌ Deep agents test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧠 Basic Deep Agents Integration Test")
    print("This test verifies that deep agents integration is working")
    print("without running the full CCE workflow.\n")

    success = asyncio.run(test_deep_agents_basic())

    if success:
        print("\n🎯 Deep agents integration is ready for production use!")
        print("💡 You can now run the full workflow with: python src/tests/run_process_ticket_deep_agents.py")
    else:
        print("\n🔧 Issues detected - please review output above")
        print("💡 Fix the issues before running the full workflow")

    sys.exit(0 if success else 1)
