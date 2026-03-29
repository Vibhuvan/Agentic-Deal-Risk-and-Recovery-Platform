from utils.llm import call_gemini
from utils.parser import extract_json

def planner_node(state):
    logs = state.get("logs", [])
    user_goal = state.get("user_goal", "full_autonomous")

    prompt = f"""
You are an AI planner.

User goal: {user_goal}



Rules:
- risk_only → ["fusion", "risk"]
- strategy_only → ["fusion", "risk", "strategy"]
- full_autonomous → ["fusion", "risk", "strategy", "execution", "feedback"]

Return JSON:
{{ "plan": [] }}
"""

    response = call_gemini(prompt)

    try:
        parsed = extract_json(response)
        plan = parsed.get("plan", [])
    except:
        if user_goal == "risk_only":
            plan = ["fusion", "risk"]
        elif user_goal == "strategy_only":
            plan = ["fusion", "risk", "strategy"]
        else:
            plan = ["fusion", "risk", "strategy", "execution", "feedback"]

    logs.append(f"Planner plan: {plan}")

    return {**state, "plan": plan, "logs": logs}