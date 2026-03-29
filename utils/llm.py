from dotenv import load_dotenv
import os
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY", "")

if api_key:
    import openai
    client = openai.OpenAI(api_key=api_key)
    
    def call_openai(prompt: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
else:
    # Mock implementation for demo without API key
    import json
    
    def call_openai(prompt: str) -> str:
        """Mock OpenAI response for demonstration"""
        if "risk" in prompt.lower():
            return json.dumps({
                "risk_score": 0.72,
                "confidence": 0.85,
                "factors": [
                    "No response in last 7 days",
                    "Prospect evaluating competitor",
                    "Pricing objection raised"
                ],
                "reasoning": "Deal shows concerning engagement decline. Prospect is actively evaluating alternatives and has raised cost concerns. High risk of lost opportunity without immediate intervention."
            })
        elif "strategy" in prompt.lower():
            return json.dumps({
                "strategy_steps": [
                    "Schedule executive briefing to address pricing",
                    "Provide ROI calculator showing cost benefits",
                    "Introduce success story from similar industry",
                    "Offer flexible payment terms"
                ],
                "talking_points": [
                    "We can tailor pricing for your use case",
                    "Average 40% cost reduction vs competitors",
                    "2-week faster deployment"
                ]
            })
        elif "execution" in prompt.lower():
            return json.dumps({
                "email_primary": {
                    "subject": "ROI Analysis for Your Deal",
                    "body": "Hi, I wanted to share a customized ROI analysis for your organization..."
                },
                "followup_actions": [
                    "Call in 2 days if no response",
                    "Send pricing comparison in 3 days",
                    "Escalate to CFO after 5 days"
                ]
            })
        else:
            return json.dumps({"signal": "processed", "status": "success"})