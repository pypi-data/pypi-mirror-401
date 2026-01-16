"""
Test Phase 2 Integration: Context Optimization in Memory Hooks

This module tests the integration of context optimization into memory hooks
and reducers to ensure they work correctly together.
"""

import time
import unittest
from datetime import datetime
from typing import Any, Dict

from src.context_memory import MemoryRecord, MemoryType
from src.deep_agents.memory_hooks import (
    create_memory_context_optimization_hook,
    create_working_memory_sync_hook,
    get_memory_hook_status,
)
from src.deep_agents.memory_reducers import apply_context_optimization_to_memory_records, get_context_optimization_stats


class TestPhase2Integration(unittest.TestCase):
    """Test Phase 2 integration of context optimization into memory hooks."""

    def setUp(self):
        """Set up test data with realistic memory records."""
        # Create test memory records
        self.test_records = [
            MemoryRecord(
                content="User requested to implement memory optimization",
                memory_type=MemoryType.WORKING,
                metadata={"message_type": "HumanMessage", "message_id": "msg_1234567890", "timestamp": time.time()},
                tags=["human", "input", "request"],
                relevance_score=0.8,
                timestamp=datetime.now(),
            ),
            MemoryRecord(
                content="Successful file_operations using write_file",
                memory_type=MemoryType.PROCEDURAL,
                metadata={
                    "pattern_id": "pattern_bddfff33_1758302894",
                    "pattern_type": "tool_sequence",
                    "success_rate": 1.0,
                    "tool_sequence": ["write_file"],
                    "conditions": ["task_completion_detected"],
                    "outcomes": [],
                    "created_from_episode": 1758302887.315726,
                    "working_memory_size": 16,
                },
                tags=["tool_sequence", "file_operations", "success", "pattern", "procedural"],
                relevance_score=1.0,
                timestamp=datetime.fromisoformat("2025-09-19T17:28:14.952792+00:00"),
            ),
        ]

        # Create test state with messages to trigger working memory sync
        from langchain_core.messages import AIMessage, HumanMessage

        self.test_state = {
            "messages": [
                HumanMessage(content="User requested to implement memory optimization"),
                AIMessage(content="I'll help you implement memory optimization"),
            ],
            "working_memory": self.test_records,
            "episodic_memory": [],
            "procedural_memory": [self.test_records[1]],
            "memory_stats": {"context_optimization_enabled": True, "total_records": 2},
            "working_memory_stats": {},
            "episodic_stats": {},
            "procedural_stats": {"total_patterns": 1},
            "last_memory_sync": time.time(),
        }

    def test_working_memory_sync_hook_with_context_optimization(self):
        """Test that working memory sync hook includes context optimization metrics."""
        # Create the hook
        sync_hook = create_working_memory_sync_hook()

        # Apply the hook to test state
        updated_state = sync_hook(self.test_state)

        # Verify context optimization metrics are included
        self.assertIn("working_memory_stats", updated_state)
        working_memory_stats = updated_state["working_memory_stats"]

        # Check that context optimization metrics are present
        self.assertIn("context_optimization", working_memory_stats)
        context_optimization = working_memory_stats["context_optimization"]

        # Verify optimization metrics
        self.assertIn("original_size", context_optimization)
        self.assertIn("optimized_size", context_optimization)
        self.assertIn("size_reduction", context_optimization)
        self.assertIn("reduction_percentage", context_optimization)

        # Verify size reduction is positive
        self.assertGreater(context_optimization["size_reduction"], 0)
        self.assertGreater(context_optimization["reduction_percentage"], 0)

        print(f"📊 Working Memory Context Optimization: {context_optimization['reduction_percentage']:.1f}% reduction")

    def test_memory_context_optimization_hook(self):
        """Test the memory context optimization hook."""
        # Create the hook
        optimization_hook = create_memory_context_optimization_hook()

        # Apply the hook to test state
        updated_state = optimization_hook(self.test_state)

        # Verify context optimization stats are added
        self.assertIn("memory_stats", updated_state)
        memory_stats = updated_state["memory_stats"]

        # Check that context optimization stats are present
        self.assertIn("context_optimization_stats", memory_stats)
        context_stats = memory_stats["context_optimization_stats"]

        # Verify optimization metrics
        self.assertIn("original_size", context_stats)
        self.assertIn("optimized_size", context_stats)
        self.assertIn("size_reduction", context_stats)
        self.assertIn("reduction_percentage", context_stats)

        # Verify size reduction is significant
        self.assertGreater(
            context_stats["reduction_percentage"], 40, "Context optimization should achieve >40% reduction"
        )

        print(f"📊 Memory System Context Optimization: {context_stats['reduction_percentage']:.1f}% reduction")

    def test_memory_hook_status_includes_context_optimization(self):
        """Test that memory hook status includes context optimization information."""
        # Get memory hook status
        status = get_memory_hook_status(self.test_state)

        # Verify context optimization status fields are present
        self.assertIn("context_optimization_enabled", status)
        self.assertIn("last_context_optimization", status)
        self.assertIn("context_optimization_stats", status)
        self.assertIn("working_memory_context_optimization", status)

        # Verify context optimization is enabled
        self.assertTrue(status["context_optimization_enabled"])

        print(f"📊 Memory Hook Status: Context optimization enabled = {status['context_optimization_enabled']}")

    def test_apply_context_optimization_to_memory_records(self):
        """Test applying context optimization to memory records."""
        # Apply context optimization
        optimized_records = apply_context_optimization_to_memory_records(self.test_records)

        # Verify optimization was applied
        self.assertEqual(len(optimized_records), len(self.test_records))

        # Verify optimized records have minimal metadata
        for i, optimized_record in enumerate(optimized_records):
            original_record = self.test_records[i]

            # Essential fields should be preserved
            self.assertEqual(optimized_record["content"], original_record.content)
            self.assertEqual(optimized_record["memory_type"], original_record.memory_type.value)

            # Metadata should be filtered
            if "metadata" in optimized_record:
                context_metadata = optimized_record["metadata"]
                original_metadata = original_record.metadata

                # Should have fewer metadata fields
                self.assertLessEqual(len(context_metadata), len(original_metadata))

                # Non-essential fields should be filtered out
                excluded_fields = ["pattern_id", "success_rate", "tool_sequence", "conditions", "outcomes"]
                for field in excluded_fields:
                    if field in original_metadata:
                        self.assertNotIn(
                            field, context_metadata, f"Non-essential field '{field}' should be filtered out"
                        )

        print(f"📊 Applied context optimization to {len(optimized_records)} memory records")

    def test_get_context_optimization_stats(self):
        """Test getting context optimization statistics."""
        # Get optimization stats
        stats = get_context_optimization_stats(self.test_records)

        # Verify stats structure
        self.assertIn("original_size", stats)
        self.assertIn("optimized_size", stats)
        self.assertIn("size_reduction", stats)
        self.assertIn("reduction_percentage", stats)
        self.assertIn("record_count", stats)

        # Verify stats values
        self.assertEqual(stats["record_count"], len(self.test_records))
        self.assertGreater(stats["original_size"], 0)
        self.assertGreater(stats["optimized_size"], 0)
        self.assertGreater(stats["size_reduction"], 0)
        self.assertGreater(stats["reduction_percentage"], 0)

        # Verify significant size reduction
        self.assertGreater(stats["reduction_percentage"], 40, "Context optimization should achieve >40% reduction")

        print(
            f"📊 Context Optimization Stats: {stats['reduction_percentage']:.1f}% reduction ({stats['original_size']} → {stats['optimized_size']} chars)"
        )

    def test_end_to_end_context_optimization_workflow(self):
        """Test the complete context optimization workflow."""
        # Step 1: Apply working memory sync hook
        sync_hook = create_working_memory_sync_hook()
        state_after_sync = sync_hook(self.test_state)

        # Step 2: Apply context optimization hook
        optimization_hook = create_memory_context_optimization_hook()
        state_after_optimization = optimization_hook(state_after_sync)

        # Step 3: Get final status
        final_status = get_memory_hook_status(state_after_optimization)

        # Verify the complete workflow
        self.assertTrue(final_status["context_optimization_enabled"])
        self.assertIn("context_optimization_stats", final_status)
        self.assertIn("working_memory_context_optimization", final_status)

        # Verify significant optimization was achieved
        context_stats = final_status["context_optimization_stats"]
        if context_stats:
            self.assertGreater(
                context_stats["reduction_percentage"], 30, "End-to-end optimization should achieve >30% reduction"
            )
            print(f"📊 End-to-End Context Optimization: {context_stats['reduction_percentage']:.1f}% reduction")

        working_memory_stats = final_status["working_memory_context_optimization"]
        if working_memory_stats:
            self.assertGreater(
                working_memory_stats["reduction_percentage"],
                0,
                "Working memory optimization should achieve >0% reduction",
            )
            print(f"📊 Working Memory Optimization: {working_memory_stats['reduction_percentage']:.1f}% reduction")


if __name__ == "__main__":
    unittest.main()
