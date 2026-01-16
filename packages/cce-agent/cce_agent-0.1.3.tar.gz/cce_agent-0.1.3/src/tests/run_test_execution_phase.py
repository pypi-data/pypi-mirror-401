#!/usr/bin/env python3
"""
Quick Execution Phase Test for process_ticket

This script bypasses the slow parts (GitHub extraction, complex planning)
and focuses specifically on testing the execution phase of process_ticket.
"""

import asyncio
import logging
import os
import sys

# Add project to path
sys.path.insert(0, os.path.abspath("."))

from src.agent import CCEAgent
from src.models import Ticket

# Enable detailed logging for execution phase debugging
logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")


async def test_execution_phase_only():
    """Fast test focusing only on execution phase."""

    print("🚀 Quick Execution Phase Test")
    print("=" * 50)

    # 1. Create a simple test ticket (no GitHub extraction)
    ticket = Ticket(
        number=999,
        title="Quick Execution Test - Add Simple Function",
        description="""Add a simple test function to main.py:

```python
def hello_execution():
    return "Execution phase is working!"
```

This should be a simple task to test the execution phase.""",
        url="http://test.local/999",
        state="open",
        author="test-user",
    )

    print(f"📋 Test Ticket: #{ticket.number} - {ticket.title}")

    # 2. Initialize CCE Agent (this is fast)
    print(f"\n🤖 Initializing CCE Agent...")
    workspace_root = os.path.abspath(".")
    agent = CCEAgent(workspace_root=workspace_root)

    # 3. Option A: Test process_ticket with limited cycles
    print(f"\n⚡ Testing process_ticket (execution focus)...")
    print("-" * 50)

    try:
        # Set environment to speed up execution
        os.environ["FEATURE_AIDER"] = "1"  # Enable AIDER for code generation

        # The key insight: process_ticket includes planning + execution
        # But we can monitor the execution phase specifically
        result = await agent.process_ticket(ticket)

        print(f"\n📊 EXECUTION RESULTS:")
        print(f"✅ process_ticket completed: {result is not None}")

        if result:
            if hasattr(result, "status"):
                print(f"🎯 Status: {result.status}")
            if hasattr(result, "execution_cycles"):
                print(f"🔄 Execution Cycles: {len(result.execution_cycles) if result.execution_cycles else 0}")
            if hasattr(result, "final_summary"):
                summary = (
                    result.final_summary[:200] + "..."
                    if result.final_summary and len(result.final_summary) > 200
                    else result.final_summary
                )
                print(f"📝 Final Summary: {summary}")

        return True

    except Exception as e:
        print(f"❌ Execution test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_execution_phase_direct():
    """Even faster - test execution graph directly."""

    print("\n" + "=" * 50)
    print("🎯 DIRECT EXECUTION GRAPH TEST")
    print("=" * 50)

    try:
        # Initialize agent
        workspace_root = os.path.abspath(".")
        agent = CCEAgent(workspace_root=workspace_root)

        # Create a minimal execution state
        from src.agent import ExecutionState

        execution_state: ExecutionState = {
            "messages": [],
            "plan": """# Simple Test Plan
            
Add a hello_execution() function to main.py that returns "Execution phase is working!"

## Steps:
1. Open main.py
2. Add the function 
3. Test it works""",
            "orientation": "",
            "cycle_count": 0,
            "max_cycles": 1,  # Keep it short!
            "agent_status": "running",
            "cycle_results": [],
        }

        print(f"🚀 Testing execution graph directly...")
        print(f"📋 Plan length: {len(execution_state['plan'])} chars")
        print(f"🔄 Max cycles: {execution_state['max_cycles']}")

        # Execute directly
        config = {"configurable": {"thread_id": "test-execution-direct"}, "recursion_limit": 25}

        result = await agent.execution_graph.ainvoke(execution_state, config=config)

        print(f"\n📊 DIRECT EXECUTION RESULTS:")
        print(f"✅ Execution graph completed: {result is not None}")

        if result:
            print(f"🎯 Final Status: {result.get('agent_status', 'unknown')}")
            print(f"🔄 Cycles Completed: {len(result.get('cycle_results', []))}")
            print(f"📝 Messages: {len(result.get('messages', []))}")

            # Show cycle results
            cycle_results = result.get("cycle_results", [])
            for i, cycle in enumerate(cycle_results):
                print(f"   Cycle {i + 1}: {getattr(cycle, 'final_thought', 'No summary')[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Direct execution test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def check_aider_availability():
    """Quick check if AIDER is working."""
    print("\n" + "=" * 50)
    print("🔍 AIDER AVAILABILITY CHECK")
    print("=" * 50)

    try:
        from src.tools.aider.wrapper import AiderctlWrapper

        aider_wrapper = AiderctlWrapper(strict_mode=False)
        availability = aider_wrapper.get_availability_status()

        print(f"📊 AIDER Status: {availability['status']}")
        print(f"💬 Message: {availability.get('message', 'No message')}")

        if availability.get("guidance"):
            print(f"💡 Guidance: {availability['guidance']}")

        # Check FEATURE_AIDER
        feature_aider = os.environ.get("FEATURE_AIDER", "0")
        print(f"🎛️  FEATURE_AIDER: {feature_aider}")

        if feature_aider != "1":
            print("⚠️  FEATURE_AIDER is not set to 1 - this will disable code generation!")

        return availability["status"] == "available" and feature_aider == "1"

    except Exception as e:
        print(f"❌ AIDER check failed: {e}")
        return False


async def main():
    """Run the quick execution test."""

    print("🚀 CCE Agent - Quick Execution Phase Test")
    print("Choose test type:")
    print("1. Full process_ticket (faster, but includes planning)")
    print("2. Direct execution graph test (fastest)")
    print("3. AIDER availability check only")

    # Quick command line handling
    test_type = "1"  # Default to process_ticket
    if len(sys.argv) > 1:
        test_type = sys.argv[1]

    # Always check AIDER first
    print(f"\n🔍 Step 1: Checking AIDER availability...")
    aider_ok = await check_aider_availability()

    if not aider_ok:
        print(f"\n⚠️  AIDER issues detected - execution may not work as expected")
        print(f"💡 Fix: Set FEATURE_AIDER=1 and ensure aiderctl is available")

    success = False

    if test_type == "3":
        success = aider_ok
    elif test_type == "2":
        print(f"\n🎯 Step 2: Testing execution graph directly...")
        success = await test_execution_phase_direct()
    else:
        print(f"\n⚡ Step 2: Testing process_ticket execution...")
        success = await test_execution_phase_only()

    # Summary
    print(f"\n" + "=" * 50)
    print(f"📊 QUICK TEST SUMMARY")
    print(f"=" * 50)

    print(f"🔍 AIDER Available: {'✅ Yes' if aider_ok else '❌ No'}")
    print(f"⚡ Execution Test: {'✅ Success' if success else '❌ Failed'}")

    if success and aider_ok:
        print(f"\n🎉 Execution phase is working correctly!")
    elif success and not aider_ok:
        print(f"\n⚠️  Test passed but AIDER issues may affect real execution")
    else:
        print(f"\n❌ Execution issues detected - check the output above")

    return success and aider_ok


if __name__ == "__main__":
    # Set FEATURE_AIDER by default for testing
    os.environ.setdefault("FEATURE_AIDER", "1")

    success = asyncio.run(main())
    sys.exit(0 if success else 1)
