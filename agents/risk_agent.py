from utils.llm import call_openai
from utils.prompts import build_risk_prompt
from utils.parser import extract_json

def risk_node(state):
    logs = state.get("logs", [])

    deal = state["raw_data"].get("deal", {})
    emails = state["raw_data"].get("emails", [])
    engagement = state["raw_data"].get("engagement", {})
    market = state["raw_data"].get("market", {})
    signals = state.get("signals", {})

    # Build MCP prompt
    prompt = build_risk_prompt(
        deal, emails, engagement, market, signals
    )

    # Call OpenAI
    response_text = call_openai(prompt)

    # Parse JSON
    risk_data = extract_json(response_text)

    logs.append("Risk agent (OpenAI MCP) executed")
    logs.append(f"Risk Score: {risk_data.get('risk_score')}")
    logs.append(f"Confidence: {risk_data.get('confidence')}")

    return {
        **state,
        "risk": risk_data,
        "logs": logs
    }