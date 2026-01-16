"""
Minimal Working Memory Integration Example for CCE Deep Agents.

This demonstrates the correct way to use deep agents with proper state management,
based on the research findings from graph_integration.py and command_integration.py.
"""

import asyncio
import logging
from typing import Any, Dict

from langchain_core.messages import HumanMessage

from .cce_deep_agent import createCCEDeepAgent
from .state import CCEDeepAgentState

logger = logging.getLogger(__name__)


async def minimal_memory_example():
    """
    Demonstrate proper deep agents usage with memory integration.

    Based on research findings:
    - Deep agents require proper CCEDeepAgentState initialization
    - State must include messages, remaining_steps, context_memory, execution_phases
    - Agent is invoked with ainvoke(state) not invoke(string)
    """

    print("🧪 Minimal Memory Integration Example")
    print("=" * 50)

    # Step 1: Create the deep agent
    print("1. Creating deep agent...")
    try:
        agent = createCCEDeepAgent(enable_memory_persistence=False)
        print("   ✅ Deep agent created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create deep agent: {e}")
        return

    # Step 2: Create proper state (based on graph_integration.py pattern)
    print("2. Creating proper state...")
    try:
        instruction = "Test the memory system integration"
        instruction_message = HumanMessage(content=instruction)

        # Create state following the pattern from graph_integration.py:588-593
        # CCEDeepAgentState is a TypedDict, so we create it as a dict
        state = {
            "messages": [instruction_message],
            "remaining_steps": 1000,
            "context_memory": {},
            "execution_phases": [{"cycle_count": 0}],
        }

        print(f"   ✅ State created with {len(state['messages'])} messages")
        print(f"   📝 Remaining steps: {state['remaining_steps']}")
        print(f"   🧠 Context memory: {list(state['context_memory'].keys())}")

    except Exception as e:
        print(f"   ❌ Failed to create state: {e}")
        return

    # Step 3: Invoke agent with proper state
    print("3. Invoking agent with proper state...")
    try:
        # Use ainvoke with state, not invoke with string
        result = await agent.ainvoke(state)
        print("   ✅ Agent invocation successful")

        # Check if memory system is working
        if isinstance(result, dict) and "messages" in result and result["messages"]:
            print(f"   📝 Agent returned {len(result['messages'])} messages")

        # Check for memory-related fields in result
        memory_fields = ["working_memory", "episodic_memory", "procedural_memory", "memory_stats"]
        found_memory_fields = [field for field in memory_fields if field in result]

        if found_memory_fields:
            print(f"   🧠 Memory fields found: {found_memory_fields}")
        else:
            print("   ⚠️ No memory fields found in result")

    except Exception as e:
        print(f"   ❌ Agent invocation failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return

    print("=" * 50)
    print("🎉 Minimal memory integration example completed!")
    print("✅ This demonstrates the correct deep agents usage pattern")


def test_minimal_memory_sync():
    """
    Test minimal memory synchronization without full agent invocation.
    """
    print("\n🧪 Testing Minimal Memory Synchronization")
    print("=" * 50)

    try:
        from .memory_hooks import create_memory_management_hook

        # Create memory hook
        memory_hook = create_memory_management_hook()
        print("   ✅ Memory hook created")

        # Create test state
        test_state = {
            "messages": [HumanMessage(content="Test message for memory sync")],
            "working_memory": [],
            "memory_stats": {},
        }

        # Test memory hook
        result_state = memory_hook(test_state)
        print("   ✅ Memory hook executed successfully")

        # Check if memory was updated
        if "working_memory" in result_state and result_state["working_memory"]:
            print(f"   🧠 Working memory updated: {len(result_state['working_memory'])} records")
        else:
            print("   ⚠️ Working memory not updated")

        if "memory_stats" in result_state:
            print(f"   📊 Memory stats: {result_state['memory_stats']}")

    except Exception as e:
        print(f"   ❌ Memory synchronization test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Run the minimal example
    asyncio.run(minimal_memory_example())

    # Test memory synchronization
    test_minimal_memory_sync()
