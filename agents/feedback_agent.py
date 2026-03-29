from datetime import datetime
import random

def feedback_node(state):
    logs = state.get("logs", [])

    signals = state.get("signals", {})
    actions = state.get("actions", {})

    # 🔥 Simulate outcome
    outcome = random.choice([
        "positive_reply",
        "no_response",
        "negative_reply"
    ])

    updated_signals = signals.copy()

    # Update signals based on outcome
    if outcome == "positive_reply":
        updated_signals["engagement_health"] = "active"
        updated_signals["reply_count"] += 1

    elif outcome == "no_response":
        updated_signals["last_engagement_days"] += 3

    elif outcome == "negative_reply":
        updated_signals["objections"].append("strong_rejection")

    feedback_data = {
        "outcome": outcome,
        "timestamp": datetime.utcnow().isoformat(),
        "updated_signals": updated_signals
    }

    logs.append(f"Feedback agent simulated outcome: {outcome}")

    return {
        **state,
        "signals": updated_signals,
        "feedback": feedback_data,
        "logs": logs
    }