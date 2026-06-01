"""Custom exceptions for AI Agent"""


class AIAgentException(Exception):
    """Base exception for AI Agent"""
    pass


class ConfigurationError(AIAgentException):
    """Raised when configuration is invalid"""
    pass


class APIError(AIAgentException):
    """Raised when API call fails"""
    pass


class TimeoutError(AIAgentException):
    """Raised when operation times out"""
    pass


class MemoryError(AIAgentException):
    """Raised when memory operations fail"""
    pass


class ValidationError(AIAgentException):
    """Raised when validation fails"""
    pass
