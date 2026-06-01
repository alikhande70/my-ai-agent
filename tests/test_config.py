"""Unit tests for configuration"""

import unittest
import os
from unittest.mock import patch
from src.core.config import Config


class TestConfig(unittest.TestCase):
    """Test configuration class"""

    def setUp(self):
        """Set up test fixtures"""
        os.environ["OPENAI_API_KEY"] = "test-key"

    def tearDown(self):
        """Clean up after tests"""
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

    def test_default_config(self):
        """Test default configuration values"""
        config = Config()
        self.assertEqual(config.model, "gpt-4o-mini")
        self.assertEqual(config.temperature, 0.7)
        self.assertTrue(config.memory_enabled)

    def test_invalid_temperature(self):
        """Test invalid temperature validation"""
        with patch.dict(os.environ, {"TEMPERATURE": "3.0", "OPENAI_API_KEY": "test"}):
            with self.assertRaises(ValueError):
                Config()

    def test_missing_api_key(self):
        """Test missing API key validation"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                Config()

    def test_config_to_dict(self):
        """Test config to dictionary conversion"""
        config = Config()
        config_dict = config.to_dict()
        self.assertIn("model", config_dict)
        self.assertIn("temperature", config_dict)
        self.assertEqual(config_dict["api_key"], "***hidden***")


if __name__ == "__main__":
    unittest.main()
