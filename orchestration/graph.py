from langgraph.graph import StateGraph, END

from orchestration.state import DealState
from agents.fusion_agent import fusion_node
from agents.risk_agent import risk_node

builder = StateGraph(DealState)

builder.add_node("fusion", fusion_node)
builder.add_node("risk", risk_node)

builder.set_entry_point("fusion")
builder.add_edge("fusion", "risk")
builder.add_edge("risk", END)

graph = builder.compile()