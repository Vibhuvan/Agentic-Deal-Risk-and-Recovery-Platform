def build_risk_prompt(deal, emails, engagement, market, signals):
    return f"""
You are an expert enterprise sales risk analyst AI.

Analyze a deal using MULTIPLE CONTEXTS:

--- CRM DATA ---
{deal}

--- EMAIL CONVERSATIONS ---
{emails}

--- ENGAGEMENT METRICS ---
{engagement}

--- MARKET SIGNALS ---
{market}

--- EXTRACTED SIGNALS ---
{signals}

TASK:
1. Compute deal risk score (0 to 1)
2. Provide confidence score (0 to 1)
3. Identify key risk factors
4. Provide detailed reasoning

IMPORTANT:
- Consider delays, objections, competitor pressure, inactivity
- Combine ALL contexts
- Be precise and realistic

RETURN STRICT JSON ONLY:

{{
  "risk_score": float,
  "confidence": float,
  "factors": [
    "factor 1",
    "factor 2"
  ],
  "reasoning": "detailed explanation"
}}
"""

def build_strategy_prompt(deal, signals, risk):
    return f"""
You are an expert enterprise sales strategist AI.

A deal has been analyzed and found to be at risk.

--- DEAL INFO ---
{deal}

--- SIGNALS ---
{signals}

--- RISK ANALYSIS ---
{risk}

TASK:
1. Identify ROOT CAUSES of risk
2. Create a MULTI-STEP recovery strategy
3. Prioritize actions (high → low impact)
4. Suggest communication + escalation steps
5. Estimate expected improvement in win probability

IMPORTANT:
- Be practical and realistic
- Focus on sales recovery actions
- Include outreach, meetings, escalation, pricing if needed

RETURN STRICT JSON:

{{
  "root_causes": [
    "cause 1",
    "cause 2"
  ],
  "strategy_steps": [
    {{
      "step": 1,
      "action": "action description",
      "owner": "sales_rep / manager / system",
      "priority": "high/medium/low"
    }}
  ],
  "recommended_channels": [
    "email",
    "call",
    "meeting"
  ],
  "expected_impact": {{
    "win_probability_increase": float,
    "revenue_recovery_estimate": float
  }},
  "summary": "concise explanation"
}}
"""

def build_execution_prompt(deal, strategy, risk):
    return f"""
You are an autonomous sales execution AI.

You are given a deal, risk analysis, and recovery strategy.

--- DEAL ---
{deal}

--- RISK ---
{risk}

--- STRATEGY ---
{strategy}

TASK:
1. Generate:
   - A personalized recovery email
   - A follow-up email
   - A call script for the sales rep

2. Ensure:
   - Professional tone
   - Highly contextual (mention competitor, pricing, urgency)
   - Clear CTA (call/meeting)

RETURN STRICT JSON:

{{
  "email_primary": {{
    "subject": "...",
    "body": "..."
  }},
  "email_followup": {{
    "subject": "...",
    "body": "..."
  }},
  "call_script": {{
    "opening": "...",
    "key_points": ["...", "..."],
    "closing": "..."
  }}
}}
"""