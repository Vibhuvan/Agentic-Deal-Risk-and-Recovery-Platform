from utils.llm import call_gemini
from utils.prompts import build_execution_prompt
from utils.parser import extract_json
from datetime import datetime

def execution_node(state):
    logs = state.get("logs", [])

    deal = state["raw_data"].get("deal", {})
    strategy = state.get("strategy", {})
    risk = state.get("risk", {})

    # Build prompt
    prompt = build_execution_prompt(deal, strategy, risk)

    # Call Gemini
    response_text = call_gemini(prompt)

    # Parse response
    content = extract_json(response_text)

    # Simulated execution logs
    execution_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "actions_executed": [
            {
                "type": "email_sent",
                "target": deal.get("account_name"),
                "subject": content.get("email_primary", {}).get("subject")
            },
            {
                "type": "followup_scheduled",
                "delay_days": 2
            },
            {
                "type": "call_task_created",
                "owner": deal.get("owner")
            }
        ]
    }

    logs.append("Execution agent executed")
    logs.append(f"Email sent to {deal.get('account_name')}")

    return {
        **state,
        "actions": {
            "generated_content": content,
            "execution_log": execution_log
        },
        "logs": logs
    }