from utils.llm import call_gemini
from utils.prompts import build_strategy_prompt
from utils.parser import extract_json

def strategy_node(state):
    logs = state.get("logs", [])

    deal = state["raw_data"].get("deal", {})
    signals = state.get("signals", {})
    risk = state.get("risk", {})

    # Build prompt
    prompt = build_strategy_prompt(deal, signals, risk)

    # Call Gemini
    response_text = call_gemini(prompt)

    # Parse JSON
    strategy_data = extract_json(response_text)

    logs.append("Strategy agent executed")
    logs.append(f"Generated {len(strategy_data.get('strategy_steps', []))} steps")

    return {
        **state,
        "strategy": strategy_data,
        "logs": logs
    }