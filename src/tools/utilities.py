"""Utility tools for AI Agent"""

from datetime import datetime
from typing import List, Dict, Any
import re


class TextUtils:
    """Text processing utilities"""

    @staticmethod
    def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)

    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)

    @staticmethod
    def sanitize(text: str) -> str:
        """Sanitize text by removing special characters"""
        return re.sub(r'[^a-zA-Z0-9\s\.\!\?\,]', '', text)

    @staticmethod
    def word_count(text: str) -> int:
        """Count words in text"""
        return len(text.split())

    @staticmethod
    def char_count(text: str, spaces: bool = False) -> int:
        """Count characters in text"""
        if spaces:
            return len(text)
        return len(text.replace(" ", ""))


class DateUtils:
    """Date and time utilities"""

    @staticmethod
    def current_timestamp() -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()

    @staticmethod
    def format_date(date_str: str, input_format: str = "%Y-%m-%d", 
                   output_format: str = "%B %d, %Y") -> str:
        """Format date from one format to another"""
        try:
            date_obj = datetime.strptime(date_str, input_format)
            return date_obj.strftime(output_format)
        except ValueError as e:
            return f"Error: {str(e)}"

    @staticmethod
    def days_until(target_date: str, date_format: str = "%Y-%m-%d") -> int:
        """Calculate days until target date"""
        try:
            target = datetime.strptime(target_date, date_format)
            diff = (target - datetime.now()).days
            return diff
        except ValueError as e:
            return -1

    @staticmethod
    def get_time_info() -> Dict[str, Any]:
        """Get current time information"""
        now = datetime.now()
        return {
            "timestamp": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "month": now.strftime("%B"),
            "year": now.year
        }
