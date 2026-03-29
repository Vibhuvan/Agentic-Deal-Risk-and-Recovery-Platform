from langgraph.graph import StateGraph, END

from orchestration.state import DealState
from agents.fusion_agent import fusion_node
from agents.risk_agent import risk_node
from agents.strategy_agent import strategy_node
from agents.execution_agent import execution_node
from agents.feedback_agent import feedback_node     

builder = StateGraph(DealState)

builder.add_node("fusion", fusion_node)
builder.add_node("risk", risk_node)
builder.add_node("strategy", strategy_node)
builder.add_node("execution", execution_node)
builder.add_node("feedback", feedback_node)
builder.set_entry_point("fusion")
builder.add_edge("fusion", "risk")
builder.add_edge("risk", "strategy")
builder.add_edge("strategy", "execution")
builder.add_edge("execution", "feedback")
builder.add_edge("feedback", END)

graph = builder.compile()