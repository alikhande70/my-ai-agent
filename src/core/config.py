"""Configuration management for AI Agent"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration class for AI Agent with validation"""

    # Load environment variables
    load_dotenv()

    # LLM Configuration
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    max_tokens: Optional[int] = None

    # Agent Configuration
    agent_name: str = os.getenv("AGENT_NAME", "AI Agent")
    system_prompt: str = os.getenv(
        "SYSTEM_PROMPT",
        "You are a helpful AI assistant. Provide clear, concise, and accurate responses."
    )

    # Execution Configuration
    max_iterations: int = int(os.getenv("MAX_ITERATIONS", "10"))
    timeout_seconds: int = int(os.getenv("TIMEOUT_SECONDS", "300"))

    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/agent.log")

    # Memory Configuration
    memory_enabled: bool = os.getenv("MEMORY_ENABLED", "true").lower() == "true"
    max_memory_size: int = int(os.getenv("MAX_MEMORY_SIZE", "1000"))

    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate configuration values"""
        if not self.api_key:
            raise ValueError("API_KEY is required. Set OPENAI_API_KEY environment variable.")

        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2")

        if self.max_iterations < 1:
            raise ValueError("Max iterations must be at least 1")

        if self.timeout_seconds < 1:
            raise ValueError("Timeout must be at least 1 second")

    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            "api_key": "***hidden***",
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "agent_name": self.agent_name,
            "system_prompt": self.system_prompt,
            "max_iterations": self.max_iterations,
            "timeout_seconds": self.timeout_seconds,
            "log_level": self.log_level,
            "memory_enabled": self.memory_enabled,
        }
