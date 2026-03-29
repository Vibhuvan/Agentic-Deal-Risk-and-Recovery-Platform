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