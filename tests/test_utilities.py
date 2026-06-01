"""Unit tests for utility tools"""

import unittest
from src.tools.utilities import TextUtils, DateUtils


class TestTextUtils(unittest.TestCase):
    """Test text utilities"""

    def test_truncate(self):
        """Test text truncation"""
        text = "This is a long text that needs truncation"
        truncated = TextUtils.truncate(text, max_length=20)
        self.assertLessEqual(len(truncated), 20)
        self.assertTrue(truncated.endswith("..."))

    def test_extract_emails(self):
        """Test email extraction"""
        text = "Contact me at test@example.com or admin@site.org"
        emails = TextUtils.extract_emails(text)
        self.assertEqual(len(emails), 2)
        self.assertIn("test@example.com", emails)

    def test_extract_urls(self):
        """Test URL extraction"""
        text = "Visit https://example.com and http://site.org"
        urls = TextUtils.extract_urls(text)
        self.assertEqual(len(urls), 2)

    def test_word_count(self):
        """Test word counting"""
        text = "This is a test"
        count = TextUtils.word_count(text)
        self.assertEqual(count, 4)

    def test_char_count(self):
        """Test character counting"""
        text = "Hello World"
        char_count = TextUtils.char_count(text, spaces=False)
        self.assertEqual(char_count, 10)


class TestDateUtils(unittest.TestCase):
    """Test date utilities"""

    def test_current_timestamp(self):
        """Test current timestamp"""
        timestamp = DateUtils.current_timestamp()
        self.assertIsNotNone(timestamp)
        self.assertIn("T", timestamp)

    def test_format_date(self):
        """Test date formatting"""
        formatted = DateUtils.format_date("2024-01-15")
        self.assertIn("January", formatted)

    def test_get_time_info(self):
        """Test getting time info"""
        info = DateUtils.get_time_info()
        self.assertIn("timestamp", info)
        self.assertIn("date", info)
        self.assertIn("time", info)
        self.assertIn("day_of_week", info)


if __name__ == "__main__":
    unittest.main()
