"""
Test script for the context auditing system.

This script demonstrates how the context auditing system works and can be used
to test the auditing functionality without running the full deep agents system.
"""

import logging
import os
import sys
import time
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.deep_agents.audited_llm_wrapper import wrap_llm_with_auditing
from src.deep_agents.audited_post_hook import audited_post_hook
from src.deep_agents.audited_tool_wrapper import wrap_tool_with_auditing
from src.deep_agents.context_auditor import ContextAuditor


# Mock LLM for testing
class MockLLM:
    def __init__(self, model_name="test-model"):
        self.model_name = model_name

    def invoke(self, messages, **kwargs):
        # Simulate processing time
        time.sleep(0.1)
        return f"Mock response to {len(messages)} messages"

    async def ainvoke(self, messages, **kwargs):
        # Simulate processing time
        time.sleep(0.1)
        return f"Mock async response to {len(messages)} messages"


# Mock tool for testing
class MockTool:
    def __init__(self, name="test-tool"):
        self.name = name

    def _run(self, *args, **kwargs):
        # Simulate processing time
        time.sleep(0.05)
        return f"Mock tool result for {len(args)} args and {len(kwargs)} kwargs"


def test_context_auditor():
    """Test the basic context auditor functionality."""
    print("🧪 Testing Context Auditor...")

    # Create auditor
    workspace_root = os.path.abspath(".")
    auditor = ContextAuditor(workspace_root, "test_session")

    # Test LLM call auditing
    print("  📞 Testing LLM call auditing...")
    input_messages = [
        {"role": "user", "content": "Hello, this is a test message."},
        {"role": "assistant", "content": "This is a response message."},
    ]
    output_message = "This is a test response from the LLM."

    audit_file = auditor.audit_llm_call(
        input_messages=input_messages,
        output_message=output_message,
        model_name="test-model",
        call_type="test_call",
        metadata={"test": True},
    )
    print(f"    ✅ LLM call audited: {audit_file}")

    # Test post-hook auditing
    print("  🪝 Testing post-hook auditing...")
    input_state = {"messages": input_messages, "context": {"test": "data"}, "metadata": {"hook": "test"}}
    output_state = input_state.copy()
    output_state["processed"] = True

    audit_file = auditor.audit_post_hook(
        hook_name="test_hook",
        input_state=input_state,
        output_state=output_state,
        execution_time=0.1,
        metadata={"test": True},
    )
    print(f"    ✅ Post-hook audited: {audit_file}")

    # Test tool call auditing
    print("  🔧 Testing tool call auditing...")
    tool_input = {"arg1": "value1", "arg2": "value2"}
    tool_output = "Tool execution result"

    audit_file = auditor.audit_tool_call(
        tool_name="test_tool",
        tool_input=tool_input,
        tool_output=tool_output,
        execution_time=0.05,
        metadata={"test": True},
    )
    print(f"    ✅ Tool call audited: {audit_file}")

    # Generate summary report
    print("  📊 Generating summary report...")
    summary_file = auditor.generate_summary_report()
    print(f"    ✅ Summary report generated: {summary_file}")

    print("✅ Context Auditor test completed!")


def test_audited_llm_wrapper():
    """Test the audited LLM wrapper."""
    print("🧪 Testing Audited LLM Wrapper...")

    # Create mock LLM
    mock_llm = MockLLM("test-model")

    # Wrap with auditing
    workspace_root = os.path.abspath(".")
    audited_llm = wrap_llm_with_auditing(mock_llm, workspace_root)

    # Test invoke
    print("  📞 Testing LLM invoke...")
    messages = [{"role": "user", "content": "Test message 1"}, {"role": "user", "content": "Test message 2"}]

    response = audited_llm.invoke(messages)
    print(f"    ✅ LLM invoke completed: {response}")

    # Test async invoke
    print("  📞 Testing async LLM invoke...")
    import asyncio

    async def test_async():
        response = await audited_llm.ainvoke(messages)
        print(f"    ✅ Async LLM invoke completed: {response}")

    asyncio.run(test_async())

    print("✅ Audited LLM Wrapper test completed!")


def test_audited_tool_wrapper():
    """Test the audited tool wrapper."""
    print("🧪 Testing Audited Tool Wrapper...")

    # Create mock tool
    mock_tool = MockTool("test-tool")

    # Wrap with auditing
    workspace_root = os.path.abspath(".")
    audited_tool = wrap_tool_with_auditing(mock_tool, workspace_root)

    # Test tool execution
    print("  🔧 Testing tool execution...")
    result = audited_tool._run("arg1", "arg2", kwarg1="value1", kwarg2="value2")
    print(f"    ✅ Tool execution completed: {result}")

    print("✅ Audited Tool Wrapper test completed!")


def test_audited_post_hook():
    """Test the audited post-hook decorator."""
    print("🧪 Testing Audited Post-Hook...")

    # Create a test hook function
    @audited_post_hook("test_hook", os.path.abspath("."))
    def test_hook(state):
        # Simulate some processing
        time.sleep(0.05)
        state["processed"] = True
        state["timestamp"] = time.time()
        return state

    # Test hook execution
    print("  🪝 Testing post-hook execution...")
    input_state = {"messages": [{"role": "user", "content": "Test"}], "context": {"test": "data"}}

    output_state = test_hook(input_state)
    print(f"    ✅ Post-hook execution completed: {output_state.get('processed', False)}")

    print("✅ Audited Post-Hook test completed!")


def main():
    """Run all tests."""
    print("🚀 Starting Context Auditing System Tests...")
    print("=" * 60)

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Run tests
        test_context_auditor()
        print()

        test_audited_llm_wrapper()
        print()

        test_audited_tool_wrapper()
        print()

        test_audited_post_hook()
        print()

        print("🎉 All tests completed successfully!")
        print("📁 Check the .artifacts/context_audit/ directory for audit files")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
