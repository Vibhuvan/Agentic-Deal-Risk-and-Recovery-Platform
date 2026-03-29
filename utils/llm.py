from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(override=True)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def call_gemini(prompt: str) -> str:
    """Call OpenAI API (function name kept for backward compatibility)"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
