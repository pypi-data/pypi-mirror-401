"""
Test Phase 3: Memory Size Limits and Validation

This module tests the memory size limits and validation functionality
to ensure memory records are properly filtered and limited for context usage.
"""

import time
import unittest
from datetime import datetime
from typing import Any, Dict, List

from src.context_memory import MemoryRecord, MemoryType
from src.deep_agents.memory_serialization import (
    MAX_CONTEXT_METADATA_SIZE,
    MAX_CONTEXT_TAGS_COUNT,
    MAX_MEMORY_RECORD_SIZE_CONTEXT,
    MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT,
    MAX_TOTAL_MEMORY_RECORDS_CONTEXT,
    MIN_RELEVANCE_SCORE,
    PRIORITY_MEMORY_TYPES,
    filter_memory_records_for_context,
    serialize_memory_system_for_context,
    validate_memory_record_for_context,
)


class TestPhase3Limits(unittest.TestCase):
    """Test Phase 3 memory size limits and validation functionality."""

    def setUp(self):
        """Set up test data with various memory record scenarios."""
        # Create a valid memory record
        self.valid_record = MemoryRecord(
            content="Valid memory record with reasonable content",
            memory_type=MemoryType.WORKING,
            metadata={"message_type": "HumanMessage", "pattern_type": "simple"},
            tags=["valid", "test"],
            relevance_score=0.8,
            timestamp=datetime.now(),
        )

        # Create an oversized content record
        self.oversized_content_record = MemoryRecord(
            content="x" * (MAX_MEMORY_RECORD_SIZE_CONTEXT + 100),  # Exceeds size limit
            memory_type=MemoryType.WORKING,
            metadata={"message_type": "HumanMessage"},
            tags=["oversized"],
            relevance_score=0.8,
            timestamp=datetime.now(),
        )

        # Create an oversized metadata record
        self.oversized_metadata_record = MemoryRecord(
            content="Normal content",
            memory_type=MemoryType.PROCEDURAL,
            metadata={
                "message_type": "HumanMessage",
                "pattern_type": "tool_sequence",
                "large_data": "x" * (MAX_CONTEXT_METADATA_SIZE + 100),  # Exceeds metadata limit
            },
            tags=["oversized_metadata"],
            relevance_score=0.8,
            timestamp=datetime.now(),
        )

        # Create a record with too many tags
        self.too_many_tags_record = MemoryRecord(
            content="Normal content",
            memory_type=MemoryType.EPISODIC,
            metadata={"message_type": "HumanMessage"},
            tags=["tag1", "tag2", "tag3", "tag4", "tag5"],  # Exceeds tag limit
            relevance_score=0.8,
            timestamp=datetime.now(),
        )

        # Create a low relevance record
        self.low_relevance_record = MemoryRecord(
            content="Low relevance content",
            memory_type=MemoryType.WORKING,
            metadata={"message_type": "HumanMessage"},
            tags=["low_relevance"],
            relevance_score=0.3,  # Below minimum relevance
            timestamp=datetime.now(),
        )

        # Create multiple records for count limit testing
        self.multiple_records = []
        for i in range(MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT + 5):
            record = MemoryRecord(
                content=f"Memory record {i}",
                memory_type=MemoryType.WORKING,
                metadata={"message_type": "HumanMessage", "index": i},
                tags=["multiple", f"record_{i}"],
                relevance_score=0.7 + (i * 0.01),  # Varying relevance scores
                timestamp=datetime.now(),
            )
            self.multiple_records.append(record)

    def test_validate_memory_record_for_context_valid_record(self):
        """Test validation of a valid memory record."""
        validation = validate_memory_record_for_context(self.valid_record)

        # Should be valid
        self.assertTrue(validation["is_valid"])
        self.assertEqual(len(validation["violations"]), 0)

        # Check size info
        self.assertIn("content_size", validation["size_info"])
        self.assertIn("metadata_size", validation["size_info"])
        self.assertIn("tags_count", validation["size_info"])

        # Check relevance info
        self.assertIn("relevance_score", validation["relevance_info"])
        self.assertIn("is_priority_type", validation["relevance_info"])

        print(f"📊 Valid Record Validation: {validation['size_info']}")

    def test_validate_memory_record_for_context_oversized_content(self):
        """Test validation of a record with oversized content."""
        validation = validate_memory_record_for_context(self.oversized_content_record)

        # Should be invalid
        self.assertFalse(validation["is_valid"])
        self.assertGreater(len(validation["violations"]), 0)

        # Should have content size violation
        content_violation = any("Content size" in violation for violation in validation["violations"])
        self.assertTrue(content_violation, "Should have content size violation")

        print(f"📊 Oversized Content Validation: {validation['violations']}")

    def test_validate_memory_record_for_context_oversized_metadata(self):
        """Test validation of a record with oversized metadata."""
        validation = validate_memory_record_for_context(self.oversized_metadata_record)

        # Should be invalid
        self.assertFalse(validation["is_valid"])
        self.assertGreater(len(validation["violations"]), 0)

        # Should have metadata size violation
        metadata_violation = any("Metadata size" in violation for violation in validation["violations"])
        self.assertTrue(metadata_violation, "Should have metadata size violation")

        print(f"📊 Oversized Metadata Validation: {validation['violations']}")

    def test_validate_memory_record_for_context_too_many_tags(self):
        """Test validation of a record with too many tags."""
        validation = validate_memory_record_for_context(self.too_many_tags_record)

        # Should be invalid
        self.assertFalse(validation["is_valid"])
        self.assertGreater(len(validation["violations"]), 0)

        # Should have tags count violation
        tags_violation = any("Tags count" in violation for violation in validation["violations"])
        self.assertTrue(tags_violation, "Should have tags count violation")

        print(f"📊 Too Many Tags Validation: {validation['violations']}")

    def test_validate_memory_record_for_context_low_relevance(self):
        """Test validation of a record with low relevance score."""
        validation = validate_memory_record_for_context(self.low_relevance_record)

        # Should be invalid
        self.assertFalse(validation["is_valid"])
        self.assertGreater(len(validation["violations"]), 0)

        # Should have relevance score violation
        relevance_violation = any("Relevance score" in violation for violation in validation["violations"])
        self.assertTrue(relevance_violation, "Should have relevance score violation")

        print(f"📊 Low Relevance Validation: {validation['violations']}")

    def test_filter_memory_records_for_context_mixed_records(self):
        """Test filtering of mixed valid and invalid records."""
        mixed_records = [
            self.valid_record,
            self.oversized_content_record,
            self.oversized_metadata_record,
            self.too_many_tags_record,
            self.low_relevance_record,
        ]

        filtered_records = filter_memory_records_for_context(mixed_records)

        # Should only include valid records
        self.assertEqual(len(filtered_records), 1)
        self.assertEqual(filtered_records[0], self.valid_record)

        print(f"📊 Mixed Records Filtering: {len(mixed_records)} → {len(filtered_records)} records")

    def test_filter_memory_records_for_context_count_limits(self):
        """Test filtering with count limits."""
        filtered_records = filter_memory_records_for_context(self.multiple_records)

        # Should respect count limits
        self.assertLessEqual(len(filtered_records), MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT)

        # Should keep the most relevant records
        if len(filtered_records) > 1:
            relevance_scores = [getattr(record, "relevance_score", 0.0) for record in filtered_records]
            self.assertEqual(relevance_scores, sorted(relevance_scores, reverse=True), "Should be sorted by relevance")

        print(f"📊 Count Limits Filtering: {len(self.multiple_records)} → {len(filtered_records)} records")

    def test_serialize_memory_system_for_context_with_filtering(self):
        """Test system serialization with filtering applied."""
        test_state = {
            "working_memory": [self.valid_record, self.oversized_content_record],
            "episodic_memory": [self.too_many_tags_record],
            "procedural_memory": [self.oversized_metadata_record, self.low_relevance_record],
            "memory_stats": {"total_records": 5},
            "episodic_stats": {},
            "procedural_stats": {"total_patterns": 1},
            "working_memory_stats": {"record_count": 2},
            "last_memory_sync": time.time(),
        }

        serialized_system = serialize_memory_system_for_context(test_state)

        # Should have filtering applied
        self.assertTrue(serialized_system.get("filtering_applied", False))

        # Should have filtering stats
        self.assertIn("context_optimization_stats", serialized_system)
        context_stats = serialized_system["context_optimization_stats"]
        self.assertIn("filtering_stats", context_stats)

        filtering_stats = context_stats["filtering_stats"]
        self.assertIn("total_records_before", filtering_stats)
        self.assertIn("total_records_after", filtering_stats)

        # Should have filtered out invalid records
        self.assertGreater(filtering_stats["total_records_before"], filtering_stats["total_records_after"])

        print(
            f"📊 System Filtering: {filtering_stats['total_records_before']} → {filtering_stats['total_records_after']} records"
        )

    def test_memory_size_limits_constants(self):
        """Test that memory size limit constants are properly defined."""
        # Test size limits
        self.assertGreater(MAX_MEMORY_RECORD_SIZE_CONTEXT, 0)
        self.assertGreater(MAX_CONTEXT_METADATA_SIZE, 0)
        self.assertGreater(MAX_CONTEXT_TAGS_COUNT, 0)

        # Test count limits
        self.assertGreater(MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT, 0)
        self.assertGreater(MAX_TOTAL_MEMORY_RECORDS_CONTEXT, 0)

        # Test relevance thresholds
        self.assertGreaterEqual(MIN_RELEVANCE_SCORE, 0.0)
        self.assertLessEqual(MIN_RELEVANCE_SCORE, 1.0)

        # Test priority memory types
        self.assertIsInstance(PRIORITY_MEMORY_TYPES, list)
        self.assertGreater(len(PRIORITY_MEMORY_TYPES), 0)

        print(
            f"📊 Memory Limits: Content={MAX_MEMORY_RECORD_SIZE_CONTEXT}, Metadata={MAX_CONTEXT_METADATA_SIZE}, Tags={MAX_CONTEXT_TAGS_COUNT}"
        )
        print(
            f"📊 Count Limits: Per Type={MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT}, Total={MAX_TOTAL_MEMORY_RECORDS_CONTEXT}"
        )
        print(f"📊 Relevance Threshold: {MIN_RELEVANCE_SCORE}")

    def test_context_size_predictability(self):
        """Test that context size is predictable and controlled."""
        # Create a large number of records
        large_record_set = []
        for i in range(50):
            record = MemoryRecord(
                content=f"Memory record {i} with some content",
                memory_type=MemoryType.WORKING if i % 2 == 0 else MemoryType.PROCEDURAL,
                metadata={"message_type": "HumanMessage", "index": i},
                tags=["test", f"record_{i}"],
                relevance_score=0.6 + (i * 0.01),
                timestamp=datetime.now(),
            )
            large_record_set.append(record)

        # Filter the records
        filtered_records = filter_memory_records_for_context(large_record_set)

        # Should respect total count limit
        self.assertLessEqual(len(filtered_records), MAX_TOTAL_MEMORY_RECORDS_CONTEXT)

        # Should respect per-type count limits
        memory_type_counts = {}
        for record in filtered_records:
            memory_type = record.memory_type
            memory_type_counts[memory_type] = memory_type_counts.get(memory_type, 0) + 1

        for memory_type, count in memory_type_counts.items():
            self.assertLessEqual(count, MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT, f"Count for {memory_type} exceeds limit")

        print(f"📊 Context Size Control: {len(large_record_set)} → {len(filtered_records)} records")
        print(f"📊 Memory Type Distribution: {memory_type_counts}")


if __name__ == "__main__":
    unittest.main()
