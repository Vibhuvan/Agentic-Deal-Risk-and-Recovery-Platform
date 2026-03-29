from langgraph.graph import StateGraph, END

from agents.fusion_agent import fusion_node
from agents.risk_agent import risk_node
from agents.strategy_agent import strategy_node
from agents.execution_agent import execution_node
from agents.feedback_agent import feedback_node

AGENT_MAP = {
    "fusion": fusion_node,
    "risk": risk_node,
    "strategy": strategy_node,
    "execution": execution_node,
    "feedback": feedback_node
}

def build_graph(plan):
    builder = StateGraph(dict)

    # Add nodes
    for step in plan:
        builder.add_node(step, AGENT_MAP[step])

    # Entry point
    builder.set_entry_point(plan[0])

    # Connect nodes
    for i in range(len(plan) - 1):
        builder.add_edge(plan[i], plan[i+1])

    # Feedback loop
    if "feedback" in plan:
        def retry_logic(state):
            outcome = state.get("feedback", {}).get("outcome")
            if outcome in ["no_response", "negative_reply"]:
                return "risk"
            return END

        builder.add_conditional_edges("feedback", retry_logic)
    else:
        builder.add_edge(plan[-1], END)

    return builder.compile()