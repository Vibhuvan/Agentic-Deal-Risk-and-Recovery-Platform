import json
from agents.fusion_agent import fusion_node
from utils.llm import call_gemini
from utils.parser import extract_json

def portfolio_node(state):
    logs = state.get("logs", [])

    # Load all deals
    with open("data/raw/crm_deals.json") as f:
        deals = json.load(f)

    enriched_deals = []

    # 🔥 RUN FUSION FOR EACH DEAL
    for deal in deals:
        temp_state = {
            "deal_id": deal["deal_id"],
            "raw_data": {},
            "signals": {},
            "logs": []
        }

        temp_state = fusion_node(temp_state)

        enriched_deals.append({
            "deal_id": deal["deal_id"],
            "signals": temp_state.get("signals", {}),
            "raw_data": temp_state.get("raw_data", {})
        })

    # 🧠 SEND ENRICHED DATA TO LLM
    prompt = f"""
You are a portfolio monitoring AI.

Below are enriched deals with signals:

{json.dumps(enriched_deals, indent=2)}

Select deals that require immediate attention based on:
- High value
- Competitor mentions
- Low engagement
- High delay
- Close date near

Return JSON:

{{
  "selected_deals": ["D001"],
  "reason": "why selected"
}}
"""

    response = call_gemini(prompt)

    try:
        parsed = extract_json(response)
        selected = parsed.get("selected_deals", [])
        reason = parsed.get("reason", "")
    except:
        selected = [enriched_deals[0]["deal_id"]]
        reason = "fallback selection"

    logs.append(f"Portfolio selected: {selected}")
    logs.append(f"Reason: {reason}")

    return {
        **state,
        "selected_deals": selected,
        "logs": logs
    }