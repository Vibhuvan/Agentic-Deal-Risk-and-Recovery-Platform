from agents.portfolio_agent import portfolio_node
from agents.planner_agent import planner_node
from orchestration.graph_runner import build_graph

def run_agents(state):

    #  AUTO DEAL SELECTION
    if not state.get("deal_id"):
        state = portfolio_node(state)

        selected = state.get("selected_deals", [])
        if selected:
            state["deal_id"] = selected[0]

    # PLANNER
    state = planner_node(state)

    plan = state.get("plan", [])

    if not plan:
        raise ValueError("No plan generated")

    print("PLAN:", plan)

    # LANGGRAPH EXECUTION
    graph = build_graph(plan)

    result = graph.invoke(state)

    return result