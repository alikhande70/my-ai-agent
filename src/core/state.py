from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str
    task_complete: bool
    error: Optional[str]