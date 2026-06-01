"""Memory management for AI Agent"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Message:
    """Represents a single message in memory"""
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class Memory:
    """Memory management for conversation history"""

    def __init__(self, max_size: int = 1000):
        """Initialize memory with maximum size"""
        self.max_size = max_size
        self.messages: List[Message] = []
        self.context: Dict[str, Any] = {}

    def add_message(
        self, 
        role: str, 
        content: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add message to memory"""
        message = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(message)

        # Remove oldest message if exceeding max size
        if len(self.messages) > self.max_size:
            self.messages.pop(0)

    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all messages in memory"""
        return [msg.to_dict() for msg in self.messages]

    def get_last_n_messages(self, n: int) -> List[Dict[str, Any]]:
        """Get last n messages"""
        return [msg.to_dict() for msg in self.messages[-n:]]

    def clear_memory(self) -> None:
        """Clear all messages from memory"""
        self.messages.clear()

    def set_context(self, key: str, value: Any) -> None:
        """Set context variable"""
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context variable"""
        return self.context.get(key, default)

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_messages": len(self.messages),
            "max_size": self.max_size,
            "context_size": len(self.context),
            "memory_usage_percent": (len(self.messages) / self.max_size) * 100
        }
