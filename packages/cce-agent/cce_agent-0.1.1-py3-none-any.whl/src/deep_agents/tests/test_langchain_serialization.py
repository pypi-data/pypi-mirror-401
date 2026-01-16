"""
Test script for LangChain message serialization in the context auditing system.

This script tests the fix for the "Object of type HumanMessage is not JSON serializable" error.
"""

import logging
import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.deep_agents.context_auditor import ContextAuditor


# Mock LangChain message objects
class MockHumanMessage:
    def __init__(self, content: str):
        self.content = content
        self.type = "human"
        self.additional_kwargs = {}


class MockAIMessage:
    def __init__(self, content: str):
        self.content = content
        self.type = "ai"
        self.additional_kwargs = {}


def test_langchain_message_serialization():
    """Test that LangChain message objects can be properly serialized."""
    print("🧪 Testing LangChain Message Serialization...")

    # Create auditor
    workspace_root = os.path.abspath(".")
    auditor = ContextAuditor(workspace_root, "langchain_test_session")

    # Create mock LangChain messages
    human_message = MockHumanMessage("Hello, this is a human message.")
    ai_message = MockAIMessage("This is an AI response message.")

    # Test LLM call auditing with LangChain messages
    print("  📞 Testing LLM call auditing with LangChain messages...")
    input_messages = [human_message, ai_message]
    output_message = MockAIMessage("This is a test response from the LLM.")

    try:
        audit_file = auditor.audit_llm_call(
            input_messages=input_messages,
            output_message=output_message,
            model_name="test-model",
            call_type="langchain_test_call",
            metadata={"test": "langchain_serialization"},
        )
        print(f"    ✅ LLM call with LangChain messages audited: {audit_file}")
    except Exception as e:
        print(f"    ❌ LLM call auditing failed: {e}")
        return False

    # Test post-hook auditing with LangChain messages in state
    print("  🪝 Testing post-hook auditing with LangChain messages in state...")
    input_state = {"messages": [human_message, ai_message], "context": {"test": "data"}, "metadata": {"hook": "test"}}
    output_state = input_state.copy()
    output_state["processed"] = True

    try:
        audit_file = auditor.audit_post_hook(
            hook_name="langchain_test_hook",
            input_state=input_state,
            output_state=output_state,
            execution_time=0.1,
            metadata={"test": "langchain_serialization"},
        )
        print(f"    ✅ Post-hook with LangChain messages audited: {audit_file}")
    except Exception as e:
        print(f"    ❌ Post-hook auditing failed: {e}")
        return False

    # Test tool call auditing with LangChain messages
    print("  🔧 Testing tool call auditing with LangChain messages...")
    tool_input = {"messages": [human_message, ai_message], "file_path": "test.py"}
    tool_output = MockAIMessage("Tool execution result with LangChain message.")

    try:
        audit_file = auditor.audit_tool_call(
            tool_name="langchain_test_tool",
            tool_input=tool_input,
            tool_output=tool_output,
            execution_time=0.05,
            metadata={"test": "langchain_serialization"},
        )
        print(f"    ✅ Tool call with LangChain messages audited: {audit_file}")
    except Exception as e:
        print(f"    ❌ Tool call auditing failed: {e}")
        return False

    # Generate summary report
    print("  📊 Generating summary report...")
    try:
        summary_file = auditor.generate_summary_report()
        print(f"    ✅ Summary report generated: {summary_file}")
    except Exception as e:
        print(f"    ❌ Summary report generation failed: {e}")
        return False

    print("✅ LangChain message serialization test completed successfully!")
    return True


def main():
    """Run the LangChain serialization test."""
    print("🚀 Starting LangChain Message Serialization Test...")
    print("=" * 60)

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    try:
        success = test_langchain_message_serialization()

        if success:
            print("\n🎉 All LangChain serialization tests passed!")
            print("📁 Check the .artifacts/context_audit/langchain_test_session/ directory for audit files")
        else:
            print("\n❌ Some LangChain serialization tests failed!")

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
