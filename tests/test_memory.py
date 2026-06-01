"""Unit tests for memory module"""

import unittest
from src.core.memory import Memory, Message


class TestMemory(unittest.TestCase):
    """Test memory class"""

    def setUp(self):
        """Set up test fixtures"""
        self.memory = Memory(max_size=10)

    def test_add_message(self):
        """Test adding message to memory"""
        self.memory.add_message("user", "Hello")
        self.assertEqual(len(self.memory.messages), 1)

    def test_get_messages(self):
        """Test retrieving messages"""
        self.memory.add_message("user", "Hello")
        self.memory.add_message("assistant", "Hi there")
        messages = self.memory.get_messages()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["content"], "Hello")

    def test_max_size_limit(self):
        """Test maximum size limit"""
        for i in range(15):
            self.memory.add_message("user", f"Message {i}")
        self.assertEqual(len(self.memory.messages), 10)

    def test_clear_memory(self):
        """Test clearing memory"""
        self.memory.add_message("user", "Hello")
        self.memory.clear_memory()
        self.assertEqual(len(self.memory.messages), 0)

    def test_context_operations(self):
        """Test context operations"""
        self.memory.set_context("key1", "value1")
        self.assertEqual(self.memory.get_context("key1"), "value1")
        self.assertIsNone(self.memory.get_context("nonexistent"))

    def test_memory_stats(self):
        """Test memory statistics"""
        for i in range(5):
            self.memory.add_message("user", f"Message {i}")
        stats = self.memory.get_memory_stats()
        self.assertEqual(stats["total_messages"], 5)
        self.assertEqual(stats["max_size"], 10)


if __name__ == "__main__":
    unittest.main()
