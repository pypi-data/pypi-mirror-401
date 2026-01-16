"""
Test Context-Optimized Memory Serialization

This module tests the context-optimized memory serialization functions
to ensure they reduce metadata overhead by 80-90% while preserving
essential information for context usage.
"""

import json
import time
import unittest
from datetime import datetime
from typing import Any, Dict

from src.context_memory import MemoryRecord, MemoryType
from src.deep_agents.memory_serialization import (
    filter_metadata_for_context,
    serialize_memory_record,
    serialize_memory_record_for_context,
    serialize_memory_system_for_context,
)


class TestContextOptimization(unittest.TestCase):
    """Test context-optimized memory serialization functions."""

    def setUp(self):
        """Set up test data with realistic memory records."""
        # Create a realistic procedural memory record with extensive metadata
        self.procedural_record = MemoryRecord(
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
                "episode_id": "episode_12345678_1758302887",
                "task_id": "task_98765432_1758302887",
                "session_id": "session_abcdef12_1758302887",
                "user_id": "user_xyz789_1758302887",
                "agent_id": "agent_456def_1758302887",
                "conversation_id": "conv_789abc_1758302887",
                "thread_id": "thread_def123_1758302887",
                "message_id": "msg_456789_1758302887",
                "created_at": "2025-09-19T17:28:14.952792+00:00",
                "updated_at": "2025-09-19T17:28:14.952792+00:00",
                "accessed_at": "2025-09-19T17:28:14.952792+00:00",
                "version": "1.0.0",
                "hash": "sha256:abcdef1234567890",
                "checksum": "md5:1234567890abcdef",
                "signature": "rsa:signature123456",
                "fingerprint": "fp:1234567890abcdef",
                "uuid": "550e8400-e29b-41d4-a716-446655440000",
                "id": "record_1234567890",
            },
            tags=["tool_sequence", "file_operations", "success", "pattern", "procedural"],
            relevance_score=1.0,
            timestamp=datetime.fromisoformat("2025-09-19T17:28:14.952792+00:00"),
        )

        # Create a working memory record with simpler metadata
        self.working_record = MemoryRecord(
            content="User requested to implement memory optimization",
            memory_type=MemoryType.WORKING,
            metadata={"message_type": "HumanMessage", "message_id": "msg_1234567890", "timestamp": time.time()},
            tags=["human", "input", "request"],
            relevance_score=0.8,
            timestamp=datetime.now(),
        )

        # Create test state with memory records
        self.test_state = {
            "working_memory": [self.working_record],
            "episodic_memory": [],
            "procedural_memory": [self.procedural_record],
            "memory_stats": {"total_records": 2},
            "episodic_stats": {},
            "procedural_stats": {"total_patterns": 1},
            "working_memory_stats": {"record_count": 1},
            "last_memory_sync": time.time(),
        }

    def test_serialize_memory_record_for_context_reduces_size(self):
        """Test that context-optimized serialization reduces size significantly."""
        # Serialize with full metadata
        full_serialization = serialize_memory_record(self.procedural_record)
        full_size = len(json.dumps(full_serialization))

        # Serialize with context optimization
        context_serialization = serialize_memory_record_for_context(self.procedural_record)
        context_size = len(json.dumps(context_serialization))

        # Calculate reduction percentage
        reduction_percentage = ((full_size - context_size) / full_size) * 100

        # Verify significant size reduction (target: 80-90%)
        self.assertGreater(reduction_percentage, 70, f"Size reduction should be >70%, got {reduction_percentage:.1f}%")
        self.assertLess(context_size, full_size, "Context serialization should be smaller than full serialization")

        print(f"📊 Size Reduction: {reduction_percentage:.1f}% ({full_size} → {context_size} chars)")

    def test_context_optimization_preserves_essential_fields(self):
        """Test that essential fields are preserved in context optimization."""
        context_serialization = serialize_memory_record_for_context(self.procedural_record)

        # Essential fields that must be preserved
        essential_fields = ["content", "memory_type", "timestamp"]
        for field in essential_fields:
            self.assertIn(field, context_serialization, f"Essential field '{field}' should be preserved")

        # Verify content is preserved
        self.assertEqual(context_serialization["content"], self.procedural_record.content)
        self.assertEqual(context_serialization["memory_type"], "procedural")

    def test_context_optimization_filters_metadata(self):
        """Test that non-essential metadata is filtered out."""
        context_serialization = serialize_memory_record_for_context(self.procedural_record)

        # Check that metadata exists but is filtered
        self.assertIn("metadata", context_serialization)
        context_metadata = context_serialization["metadata"]

        # Essential metadata fields that should be preserved
        essential_metadata_fields = ["pattern_type"]
        for field in essential_metadata_fields:
            if field in self.procedural_record.metadata:
                self.assertIn(field, context_metadata, f"Essential metadata field '{field}' should be preserved")

        # Non-essential metadata fields that should be filtered out
        excluded_metadata_fields = [
            "pattern_id",
            "success_rate",
            "tool_sequence",
            "conditions",
            "outcomes",
            "created_from_episode",
            "working_memory_size",
            "episode_id",
            "task_id",
            "session_id",
            "user_id",
            "agent_id",
            "conversation_id",
            "thread_id",
            "message_id",
            "created_at",
            "updated_at",
            "accessed_at",
            "version",
            "hash",
            "checksum",
            "signature",
            "fingerprint",
            "uuid",
            "id",
        ]

        for field in excluded_metadata_fields:
            self.assertNotIn(field, context_metadata, f"Non-essential metadata field '{field}' should be filtered out")

    def test_context_optimization_limits_tags(self):
        """Test that tags are limited to most relevant ones."""
        context_serialization = serialize_memory_record_for_context(self.procedural_record)

        # Check that tags are limited
        if "tags" in context_serialization:
            context_tags = context_serialization["tags"]
            original_tags = self.procedural_record.tags

            # Tags should be limited to 3 or fewer
            self.assertLessEqual(len(context_tags), 3, "Context tags should be limited to 3 or fewer")

            # Should be a subset of original tags
            for tag in context_tags:
                self.assertIn(tag, original_tags, f"Context tag '{tag}' should be from original tags")

    def test_serialize_memory_system_for_context(self):
        """Test context-optimized system serialization."""
        context_system = serialize_memory_system_for_context(self.test_state, max_records_per_type=5)

        # Verify structure
        self.assertIn("working_memory", context_system)
        self.assertIn("procedural_memory", context_system)
        self.assertIn("context_optimized", context_system)
        self.assertTrue(context_system["context_optimized"])

        # Verify optimization stats
        self.assertIn("context_optimization_stats", context_system)
        stats = context_system["context_optimization_stats"]
        self.assertIn("reduction_percentage", stats)
        self.assertGreater(stats["reduction_percentage"], 60, "System optimization should achieve >60% reduction")

        print(f"📊 System Size Reduction: {stats['reduction_percentage']:.1f}%")

    def test_filter_metadata_for_context(self):
        """Test metadata filtering function."""
        original_metadata = self.procedural_record.metadata
        filtered_metadata = filter_metadata_for_context(original_metadata)

        # Verify filtering
        self.assertLess(len(filtered_metadata), len(original_metadata), "Filtered metadata should be smaller")

        # Verify essential fields are preserved
        essential_fields = ["pattern_type"]
        for field in essential_fields:
            if field in original_metadata:
                self.assertIn(field, filtered_metadata, f"Essential field '{field}' should be preserved")

        # Verify non-essential fields are filtered out
        excluded_fields = ["pattern_id", "success_rate", "tool_sequence", "conditions", "outcomes"]
        for field in excluded_fields:
            self.assertNotIn(field, filtered_metadata, f"Non-essential field '{field}' should be filtered out")

    def test_context_optimization_with_working_memory(self):
        """Test context optimization with working memory records."""
        context_serialization = serialize_memory_record_for_context(self.working_record)

        # Verify essential fields are preserved
        self.assertEqual(context_serialization["content"], self.working_record.content)
        self.assertEqual(context_serialization["memory_type"], "working")

        # Verify metadata is preserved for working memory (simpler metadata)
        if "metadata" in context_serialization:
            context_metadata = context_serialization["metadata"]
            original_metadata = self.working_record.metadata

            # Working memory metadata should be preserved as it's simpler
            # Only essential fields are preserved: message_type, pattern_type
            essential_fields = ["message_type", "pattern_type"]
            for key in essential_fields:
                if key in original_metadata:
                    self.assertIn(
                        key, context_metadata, f"Essential working memory metadata '{key}' should be preserved"
                    )

    def test_json_serialization_compatibility(self):
        """Test that context-optimized serialization produces valid JSON."""
        context_serialization = serialize_memory_record_for_context(self.procedural_record)

        # Should be able to serialize to JSON without errors
        json_str = json.dumps(context_serialization)
        self.assertIsInstance(json_str, str)

        # Should be able to deserialize from JSON
        deserialized = json.loads(json_str)
        self.assertEqual(deserialized, context_serialization)


if __name__ == "__main__":
    unittest.main()
