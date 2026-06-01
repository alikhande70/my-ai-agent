"""Main AI Agent implementation with professional architecture"""

import time
from typing import Dict, List, Any, Optional
from functools import wraps

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

from src.core.config import Config
from src.core.logger import Logger
from src.core.memory import Memory
from src.core.exceptions import APIError, TimeoutError as AgentTimeoutError


class AgentState(TypedDict):
    """State definition for LangGraph"""
    messages: Annotated[list, operator.add]
    metadata: dict


def timeout_decorator(timeout_seconds: int):
    """Decorator to handle timeout"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            if elapsed > timeout_seconds:
                Logger.warning(
                    f"Function {func.__name__} took {elapsed:.2f}s (timeout: {timeout_seconds}s)"
                )
            return result
        return wrapper
    return decorator


class AIAgent:
    """Professional AI Agent implementation using LangGraph"""

    def __init__(self, config: Optional[Config] = None):
        """Initialize AI Agent with configuration"""
        self.config = config or Config()
        self.logger = Logger.get_logger("ai_agent", self.config.log_file)
        self.memory = Memory(max_size=self.config.max_memory_size)
        self.execution_count = 0
        self.total_tokens_used = 0

        self.logger.info(f"Initializing AI Agent: {self.config.agent_name}")
        self.logger.debug(f"Configuration: {self.config.to_dict()}")

        # Initialize LLM
        self._initialize_llm()

        # Build agent graph
        self._build_graph()

    def _initialize_llm(self) -> None:
        """Initialize LLM client"""
        try:
            self.llm = ChatOpenAI(
                model=self.config.model,
                temperature=self.config.temperature,
                api_key=self.config.api_key,
                max_tokens=self.config.max_tokens
            )
            self.logger.info(f"LLM initialized: {self.config.model}")
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM: {str(e)}")
            raise APIError(f"Failed to initialize LLM: {str(e)}")

    def _build_graph(self) -> None:
        """Build LangGraph execution graph"""
        self.graph = StateGraph(AgentState)
        
        # Add nodes
        self.graph.add_node("agent", self._agent_node)
        
        # Set entry point and edges
        self.graph.set_entry_point("agent")
        self.graph.add_edge("agent", END)
        
        # Compile graph
        self.app = self.graph.compile()
        self.logger.info("LangGraph compiled successfully")

    @timeout_decorator(300)
    def _agent_node(self, state: AgentState) -> Dict[str, Any]:
        """Process messages in agent node"""
        try:
            self.logger.debug(f"Processing state with {len(state['messages'])} messages")
            
            # Invoke LLM
            response = self.llm.invoke(state['messages'])
            
            self.logger.debug(f"LLM response received: {response.content[:100]}...")
            
            return {"messages": [response]}
        except Exception as e:
            self.logger.error(f"Error in agent node: {str(e)}")
            raise APIError(f"Error in agent node: {str(e)}")

    def _format_messages(self, user_input: str) -> List[Dict[str, str]]:
        """Format messages for LLM including system prompt and history"""
        messages = [
            {"role": "system", "content": self.config.system_prompt}
        ]

        # Add conversation history
        for msg in self.memory.get_messages():
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })

        # Add current user input
        messages.append({
            "role": "user",
            "content": user_input
        })

        return messages

    def process(self, user_input: str) -> str:
        """Process user input and return agent response"""
        if not user_input or not isinstance(user_input, str):
            raise ValueError("Input must be a non-empty string")

        self.execution_count += 1
        start_time = time.time()

        try:
            self.logger.info(f"[Execution #{self.execution_count}] Processing input: {user_input[:100]}...")

            # Store user message in memory
            if self.config.memory_enabled:
                self.memory.add_message("user", user_input)

            # Format messages
            messages = self._format_messages(user_input)

            # Invoke graph
            result = self.app.invoke({
                "messages": messages,
                "metadata": {"execution_id": self.execution_count}
            })

            # Extract response
            response = result['messages'][-1].content

            # Store assistant message in memory
            if self.config.memory_enabled:
                self.memory.add_message("assistant", response)

            elapsed_time = time.time() - start_time
            self.logger.info(f"Response generated in {elapsed_time:.2f}s")

            return response

        except Exception as e:
            self.logger.error(f"Error processing input: {str(e)}")
            raise

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            **self.memory.get_memory_stats(),
            "executions": self.execution_count,
            "total_tokens": self.total_tokens_used
        }

    def clear_memory(self) -> None:
        """Clear conversation memory"""
        self.memory.clear_memory()
        self.logger.info("Memory cleared")

    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "agent_name": self.config.agent_name,
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_iterations": self.config.max_iterations,
            "memory_enabled": self.config.memory_enabled,
            "execution_count": self.execution_count,
            "memory_stats": self.get_memory_stats()
        }
