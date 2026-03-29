import json
import re

def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        pass

    # Extract JSON block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    # fallback safe structure
    return {
        "risk_score": 0.5,
        "confidence": 0.2,
        "factors": ["parsing_failed"],
        "reasoning": text
    }