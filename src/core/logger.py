"""Logging configuration and utilities"""

import logging
import os
from typing import Optional


class Logger:
    """Logger configuration class"""

    _instance: Optional[logging.Logger] = None

    @staticmethod
    def get_logger(name: str = "ai_agent", log_file: Optional[str] = None) -> logging.Logger:
        """Get or create logger instance"""
        if Logger._instance is not None:
            return Logger._instance

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            # File handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        Logger._instance = logger
        return logger

    @staticmethod
    def info(message: str) -> None:
        """Log info message"""
        logger = Logger.get_logger()
        logger.info(message)

    @staticmethod
    def debug(message: str) -> None:
        """Log debug message"""
        logger = Logger.get_logger()
        logger.debug(message)

    @staticmethod
    def warning(message: str) -> None:
        """Log warning message"""
        logger = Logger.get_logger()
        logger.warning(message)

    @staticmethod
    def error(message: str) -> None:
        """Log error message"""
        logger = Logger.get_logger()
        logger.error(message)

    @staticmethod
    def critical(message: str) -> None:
        """Log critical message"""
        logger = Logger.get_logger()
        logger.critical(message)
