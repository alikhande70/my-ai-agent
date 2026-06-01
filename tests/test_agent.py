import pytest
from src.agent.core import AIAgent

def test_agent_initialization():
    agent = AIAgent()
    assert agent.name is not None

def test_agent_run():
    agent = AIAgent()
    result = agent.run("Test task")
    assert "Task completed" in result