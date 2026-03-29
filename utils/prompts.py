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
You are an expert sales recovery strategist.

Based on deal analysis, generate a recovery strategy with specific talking points.

--- DEAL INFO ---
{deal}

--- EXTRACTED SIGNALS ---
{signals}

--- RISK ASSESSMENT ---
{risk}

TASK:
1. Identify 3-5 recovery strategy steps
2. Provide talking points to address objections
3. Recommend specific actions (email, call, escalation)
4. Suggest timeline for interventions

IMPORTANT:
- Be specific and actionable
- Focus on high-impact interventions
- Address root causes from risk assessment
- Consider engagement drops and objections

RETURN STRICT JSON ONLY:

{{
  "strategy_steps": [
    "step 1",
    "step 2",
    "step 3"
  ],
  "talking_points": [
    "point 1",
    "point 2"
  ],
  "recommended_actions": [
    "action 1",
    "action 2"
  ],
  "timeline_days": 3
}}
"""


def build_execution_prompt(deal, strategy, risk):
    return f"""
You are an expert sales execution specialist.

Generate concrete actions to execute the recovery strategy.

--- DEAL INFO ---
{deal}

--- RECOVERY STRATEGY ---
{strategy}

--- RISK FACTORS ---
{risk}

TASK:
1. Write 2-3 email templates (subject + body)
2. Schedule specific follow-up actions
3. Recommend escalation path if needed
4. Define success metrics

IMPORTANT:
- Make emails personalized and compelling
- Include specific talking points from strategy
- Set clear next-step deadlines
- Address key risk factors

RETURN STRICT JSON ONLY:

{{
  "email_primary": {{
    "subject": "subject line",
    "body": "email body"
  }},
  "email_followup": {{
    "subject": "subject line",
    "body": "email body"
  }},
  "followup_actions": [
    "action 1",
    "action 2"
  ],
  "escalation_trigger": "condition to escalate",
  "success_metrics": [
    "metric 1",
    "metric 2"
  ]
}}
"""