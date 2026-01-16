#!/usr/bin/env python3
"""
Quick Planning Phase Test for CCE Agent

This script focuses specifically on testing the planning phase of the CCE workflow.
It bypasses GitHub extraction and execution to isolate and test the planning functionality.
"""

import asyncio
import logging
import os
import sys

# Add project to path
sys.path.insert(0, os.path.abspath("."))

from src.agent import CCEAgent
from src.models import Ticket

# Enable detailed logging for planning phase debugging
logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")


async def test_planning_phase_only():
    """Test the planning phase in isolation."""

    print("🚀 Quick Planning Phase Test")
    print("=" * 50)

    # 1. Create a test ticket (no GitHub extraction)
    ticket = Ticket(
        number=999,
        title="Quick Planning Test - Add Configurable Run Modes",
        description="""## Description

Implement configurable run modes for the CCE agent that provide different levels of human oversight and intervention. This enables the agent to operate in demo mode (fully autonomous), guided mode (strategic checkpoints), or expert mode (comprehensive oversight) based on user preferences and use case requirements.

## Background

Different use cases require different levels of human involvement. Demo scenarios need end-to-end autonomous operation, development work may benefit from strategic checkpoints, and critical production changes may require comprehensive oversight.

## Requirements

### 1. Demo Mode (Fully Autonomous)
- [ ] Zero human interruptions or approval gates
- [ ] End-to-end execution without pausing
- [ ] Automatic fallback strategies for failures
- [ ] Comprehensive logging for post-execution review

### 2. Guided Mode (Strategic Checkpoints)
- [ ] Orientation gate: Human approval of planning and approach
- [ ] Evaluation gate: Human review of results before submission
- [ ] Critical failure interrupts with human decision options
- [ ] Configurable checkpoint frequency

### 3. Expert Mode (Comprehensive Oversight)
- [ ] All guided mode checkpoints plus additional signals
- [ ] Budget threshold interrupts (cost, time, complexity)
- [ ] Quality threshold interrupts (test coverage, code quality)
- [ ] Critical file modification approvals
- [ ] Granular control over agent decisions""",
        url="http://test.local/999",
        state="open",
        author="test-user",
    )

    print(f"📋 Test Ticket: #{ticket.number} - {ticket.title}")

    # 2. Initialize CCE Agent
    print(f"\n🤖 Initializing CCE Agent...")
    workspace_root = os.path.abspath(".")
    agent = CCEAgent(workspace_root=workspace_root)

    # 3. Test planning phase directly
    print(f"\n🎯 Testing Planning Phase...")
    print("-" * 50)

    try:
        # Create initial planning state
        from langchain_core.messages import HumanMessage

        from src.agent import PlanningState

        initial_state: PlanningState = {
            "messages": [HumanMessage(content=ticket.description)],
            "shared_plan": "",
            "technical_analysis": "",
            "architectural_analysis": "",
            "consensus_reached": False,
            "iteration_count": 0,
            "max_iterations": 3,
            "structured_phases": None,
        }

        print(f"📊 Initial State:")
        print(f"   - Messages: {len(initial_state['messages'])}")
        print(f"   - Max iterations: {initial_state['max_iterations']}")
        print(f"   - Content length: {len(initial_state['messages'][0].content)} chars")

        # Execute planning graph
        config = {"configurable": {"thread_id": "test-planning-phase"}, "recursion_limit": 25}

        print(f"\n🚀 Executing planning graph...")
        result = await agent.planning_graph.ainvoke(initial_state, config=config)

        print(f"\n📊 PLANNING RESULTS:")
        print(f"✅ Planning completed: {result is not None}")

        if result:
            print(f"🎯 Consensus reached: {result.get('consensus_reached', False)}")
            print(f"🔄 Iterations used: {result.get('iteration_count', 0)}")
            print(f"📝 Shared plan length: {len(result.get('shared_plan', ''))} chars")
            print(f"🔧 Technical analysis length: {len(result.get('technical_analysis', ''))} chars")
            arch_analysis = result.get("architectural_analysis", "")
            arch_analysis_length = len(arch_analysis) if isinstance(arch_analysis, str) else len(str(arch_analysis))
            print(f"🏗️  Architectural analysis length: {arch_analysis_length} chars")
            print(
                f"📋 Structured phases: {len(result.get('structured_phases', [])) if result.get('structured_phases') else 0}"
            )

            # Show plan preview
            shared_plan = result.get("shared_plan", "")
            if shared_plan:
                preview = shared_plan[:300] + "..." if len(shared_plan) > 300 else shared_plan
                print(f"\n📋 Plan Preview:")
                print(f"   {preview}")

            # Show structured phases if available
            structured_phases = result.get("structured_phases", [])
            if structured_phases:
                print(f"\n📋 Structured Phases ({len(structured_phases)}):")
                for i, phase in enumerate(structured_phases[:3]):  # Show first 3 phases
                    phase_name = phase.get("phase_name", f"Phase {i + 1}")
                    print(f"   {i + 1}. {phase_name}")

        return True

    except Exception as e:
        print(f"❌ Planning test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_planning_phase_with_research():
    """Test planning phase with explicit research step."""

    print("\n" + "=" * 50)
    print("🔍 PLANNING WITH RESEARCH TEST")
    print("=" * 50)

    try:
        # Initialize agent
        workspace_root = os.path.abspath(".")
        agent = CCEAgent(workspace_root=workspace_root)

        # Test research step directly
        print(f"🔍 Testing research_codebase command...")

        research_result = await agent.command_orchestrator.execute_command_sequence(
            [
                {
                    "command": "research_codebase",
                    "params": {
                        "research_question": "configurable run modes implementation patterns",
                        "context": "Implement configurable run modes for the CCE agent",
                    },
                }
            ]
        )

        print(f"📊 Research Results:")
        print(f"✅ Research completed: {research_result is not None}")

        if research_result:
            print(f"📝 Research content length: {len(str(research_result))} chars")
            print(f"🔍 Research preview: {str(research_result)[:200]}...")

        # Test create_plan command
        print(f"\n📋 Testing create_plan command...")

        plan_result = await agent.command_orchestrator.execute_command_sequence(
            [
                {
                    "command": "create_plan",
                    "params": {
                        "plan_topic": "Add Configurable Run Modes",
                        "context": "Implement configurable run modes for the CCE agent that provide different levels of human oversight and intervention.",
                    },
                }
            ]
        )

        print(f"📊 Plan Creation Results:")
        print(f"✅ Plan created: {plan_result is not None}")

        if plan_result:
            print(f"📝 Plan content length: {len(str(plan_result))} chars")
            print(f"🔍 Plan preview: {str(plan_result)[:200]}...")

        return True

    except Exception as e:
        print(f"❌ Planning with research test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_command_orchestrator():
    """Test the command orchestrator directly."""

    print("\n" + "=" * 50)
    print("🎯 COMMAND ORCHESTRATOR TEST")
    print("=" * 50)

    try:
        # Initialize agent
        workspace_root = os.path.abspath(".")
        agent = CCEAgent(workspace_root=workspace_root)

        print(f"🔍 Command Orchestrator Type: {type(agent.command_orchestrator)}")
        print(f"📋 Available Commands: {list(agent.command_orchestrator.commands.keys())}")

        # Test a simple command sequence
        print(f"\n🚀 Testing simple command sequence...")

        result = await agent.command_orchestrator.execute_command_sequence(
            [
                {
                    "command": "create_plan",
                    "params": {"plan_topic": "Test Planning", "context": "This is a test of the planning system."},
                }
            ]
        )

        print(f"📊 Command Sequence Results:")
        print(f"✅ Sequence completed: {result is not None}")

        if result:
            print(f"📝 Result type: {type(result)}")
            print(f"📝 Result length: {len(str(result))} chars")

        return True

    except Exception as e:
        print(f"❌ Command orchestrator test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Run the planning phase tests."""

    print("🚀 CCE Agent - Planning Phase Test Suite")
    print("Choose test type:")
    print("1. Full planning phase test (recommended)")
    print("2. Planning with explicit research steps")
    print("3. Command orchestrator test only")
    print("4. All tests")

    # Quick command line handling
    test_type = "1"  # Default to full planning test
    if len(sys.argv) > 1:
        test_type = sys.argv[1]

    success_count = 0
    total_tests = 0

    if test_type in ["1", "4"]:
        print(f"\n🎯 Test 1: Full Planning Phase Test")
        total_tests += 1
        success = await test_planning_phase_only()
        if success:
            success_count += 1
            print("✅ Planning phase test passed")
        else:
            print("❌ Planning phase test failed")

    if test_type in ["2", "4"]:
        print(f"\n🔍 Test 2: Planning with Research")
        total_tests += 1
        success = await test_planning_phase_with_research()
        if success:
            success_count += 1
            print("✅ Planning with research test passed")
        else:
            print("❌ Planning with research test failed")

    if test_type in ["3", "4"]:
        print(f"\n🎯 Test 3: Command Orchestrator")
        total_tests += 1
        success = await test_command_orchestrator()
        if success:
            success_count += 1
            print("✅ Command orchestrator test passed")
        else:
            print("❌ Command orchestrator test failed")

    # Summary
    print(f"\n" + "=" * 50)
    print(f"📊 PLANNING TEST SUMMARY")
    print(f"=" * 50)

    print(f"✅ Tests Passed: {success_count}/{total_tests}")
    print(f"📊 Success Rate: {(success_count / total_tests) * 100:.1f}%")

    if success_count == total_tests:
        print(f"\n🎉 All planning phase tests passed!")
        print(f"💡 The planning system is working correctly")
    elif success_count > 0:
        print(f"\n⚠️  Some planning tests passed - check failed tests above")
    else:
        print(f"\n❌ All planning tests failed - check the output above")

    return success_count == total_tests


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
