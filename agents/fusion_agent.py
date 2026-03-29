import json
from datetime import datetime
from dateutil import parser

# -----------------------------
# LOAD ALL DATA
# -----------------------------
def load_all_data():
    with open("data/raw/crm_deals.json") as f:
        deals = json.load(f)

    with open("data/raw/emails.json") as f:
        emails = json.load(f)

    with open("data/raw/engagement.json") as f:
        engagement = json.load(f)

    with open("data/raw/market.json") as f:
        market = json.load(f)

    return deals, emails, engagement, market


# -----------------------------
# FILTER BY DEAL
# -----------------------------
def get_deal_context(deal_id, deals, emails, engagement, market):
    deal = next(d for d in deals if d["deal_id"] == deal_id)

    deal_emails = [e for e in emails if e["deal_id"] == deal_id]

    deal_engagement = next(
        (e for e in engagement if e["deal_id"] == deal_id), {}
    )

    deal_market = next(
        (m for m in market if m["deal_id"] == deal_id), {}
    )

    return deal, deal_emails, deal_engagement, deal_market


# -----------------------------
# SIGNAL EXTRACTION
# -----------------------------
def extract_signals(emails, engagement):
    if not emails:
        return {}

    emails = sorted(emails, key=lambda x: x["timestamp"])

    reply_count = 0
    delays = []
    objections = set()
    competitor_flag = False

    prev_time = None

    for email in emails:
        body = email["body"].lower()
        subject = email["subject"].lower()

        # Replies
        if "re:" in subject:
            reply_count += 1

        # Competitor detection
        if "competitor" in body:
            competitor_flag = True

        # Objections
        if "price" in body or "cost" in body:
            objections.add("pricing")
        if "approval" in body:
            objections.add("approval_delay")
        if "evaluating" in body or "reviewing" in body:
            objections.add("evaluation_delay")

        # Delay calculation
        current_time = parser.parse(email["timestamp"])
        if prev_time:
            delay = (current_time - prev_time).total_seconds() / 3600
            delays.append(delay)

        prev_time = current_time

    avg_delay = sum(delays) / len(delays) if delays else 0

    # Engagement signals
    last_engagement_days = engagement.get("last_engagement_days_ago", 0)

    signals = {
        "email_count": len(emails),
        "reply_count": reply_count,
        "avg_reply_delay_hours": round(avg_delay, 2),
        "competitor_mentioned": competitor_flag,
        "objections": list(objections),
        "last_engagement_days": last_engagement_days,
        "engagement_health": "low" if last_engagement_days > 7 else "active"
    }

    return signals


# -----------------------------
# FUSION NODE (LANGGRAPH)
# -----------------------------
def fusion_node(state):
    deal_id = state["deal_id"]
    logs = state.get("logs", [])

    # Load all data
    deals, emails, engagement, market = load_all_data()

    # Get context for this deal
    deal, deal_emails, deal_eng, deal_market = get_deal_context(
        deal_id, deals, emails, engagement, market
    )

    # Extract signals
    signals = extract_signals(deal_emails, deal_eng)

    logs.append(f"Fusion agent processed deal {deal_id}")
    logs.append(f"Extracted signals: {signals}")

    return {
        **state,
        "raw_data": {
            "deal": deal,
            "emails": deal_emails,
            "engagement": deal_eng,
            "market": deal_market
        },
        "signals": signals,
        "logs": logs
    }