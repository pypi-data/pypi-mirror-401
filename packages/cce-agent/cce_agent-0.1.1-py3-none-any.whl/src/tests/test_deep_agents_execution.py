#!/usr/bin/env python3
"""
Test the execution phase with deep agents.
"""

import asyncio
import logging

# Add the project root to the path
import os
import sys
import tempfile

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def _create_deep_agent():
    """Create a deep agent with the best available LLM configuration."""
    if os.getenv("ANTHROPIC_API_KEY"):
        from src.deep_agents.cce_deep_agent import createCCEDeepAgent

        return createCCEDeepAgent()

    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:
            raise RuntimeError("OPENAI_API_KEY set but langchain_openai is unavailable") from exc

        from src.deep_agents.cce_deep_agent import createCCEDeepAgent

        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        return createCCEDeepAgent(llm=llm)

    raise RuntimeError("Missing ANTHROPIC_API_KEY or OPENAI_API_KEY for deep agents execution")


async def test_deep_agents_execution():
    """Test the execution phase with deep agents."""
    print("🧪 Testing deep agents execution phase...")

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No ANTHROPIC_API_KEY or OPENAI_API_KEY found in environment")
        return False

    print(f"✅ API key found: {api_key[:10]}...")

    try:
        # Initialize deep agent
        print("🚀 Initializing CCE Deep Agent...")
        deep_agent = _create_deep_agent()
        print("✅ Deep agent initialized successfully!")

        # Prepare execution instruction
        test_path = os.path.join(tempfile.gettempdir(), "execution_test.txt")
        instruction = f"""Create a file at {test_path} with the content:\nconsole.log('Deep agents execution working!');\n\nUse execute_bash_command or filesystem tools and confirm the file exists.\nDo not modify repository files or run git commands.\n"""
        message = HumanMessage(content=instruction)

        timeout_raw = os.getenv("DEEP_AGENTS_TIMEOUT_SECONDS", "300")
        try:
            timeout_seconds = int(timeout_raw)
        except ValueError:
            print(f"⚠️  Invalid DEEP_AGENTS_TIMEOUT_SECONDS={timeout_raw}; defaulting to 300s")
            timeout_seconds = 300

        config = {"configurable": {"thread_id": "deep-agents-execution-test"}}

        print("🚀 Testing deep agents execution...")
        if hasattr(deep_agent, "invoke_with_filesystem"):
            run_coro = deep_agent.invoke_with_filesystem(
                [message],
                context_memory={"test_path": test_path},
                remaining_steps=300,
                execution_phases=[{"cycle_count": 0, "phase": "execution_test"}],
                config=config,
            )
        else:
            run_coro = deep_agent.ainvoke(
                {
                    "messages": [message],
                    "remaining_steps": 300,
                    "context_memory": {"test_path": test_path},
                    "execution_phases": [{"cycle_count": 0, "phase": "execution_test"}],
                },
                config=config,
            )

        if timeout_seconds > 0:
            result = await asyncio.wait_for(run_coro, timeout=timeout_seconds)
        else:
            result = await run_coro

        print("✅ Deep agents execution completed!")
        print(f"📊 Result type: {type(result)}")

        if isinstance(result, dict):
            print(f"📊 Result keys: {list(result.keys())}")
            if result.get("messages"):
                last_message = result["messages"][-1]
                content = getattr(last_message, "content", str(last_message))
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"📝 Final summary preview: {preview}")

        # Check if execution_test.txt was created (filesystem middleware may normalize to workspace root)
        # Note: The test file may land under workspace root when using filesystem middleware tools.
        content = ""
        found = False
        normalized_path = os.path.normpath(test_path.lstrip(os.sep))
        workspace_test_path = os.path.join(PROJECT_ROOT, normalized_path)
        if os.path.exists(test_path):
            print("\n✅ execution_test.txt was created in temp directory!")
            with open(test_path) as f:
                content = f.read()
            found = True
        elif os.path.exists(workspace_test_path):
            print("\n✅ execution_test.txt was created under workspace root!")
            with open(workspace_test_path) as f:
                content = f.read()
            found = True
        else:
            # Also check artifact root as fallback
            from src.config.artifact_root import get_artifact_root

            artifact_test_path = get_artifact_root() / "execution_test.txt"
            if artifact_test_path.exists():
                print("\n✅ execution_test.txt was created in artifact root!")
                with open(artifact_test_path) as f:
                    content = f.read()
                found = True
            else:
                print("\n⚠️ execution_test.txt not found (may have been cleaned up)")

        if found:
            print(f"📄 Content: {content}")
            for cleanup_path in (test_path, workspace_test_path):
                if os.path.exists(cleanup_path):
                    try:
                        os.remove(cleanup_path)
                    except OSError:
                        pass
            return True

        print("\n❌ execution_test.txt was NOT created on disk")
        return False

    except TimeoutError:
        print("⏰ Deep agents execution timed out")
        return False
    except Exception as e:
        print(f"❌ Execution error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_deep_agents_execution())
    if success:
        print("\n🎉 Deep agents execution test completed successfully!")
    else:
        print("\n❌ Deep agents execution test failed!")
