from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def agent_node(state):
    response = llm.invoke(state['messages'])
    return {"messages": [response]}

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"messages": [{"role": "user", "content": "Hello, who are you?"}]})
    print(result['messages'][-1].content)

print("AI Agent ready! Try modifying the prompt.")