from dotenv import load_dotenv
import os
load_dotenv(override=True)
from google import genai


print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))
# Initialize client (API key auto from env: GEMINI_API_KEY)
client = genai.Client()

def call_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",   # or "gemini-3-flash-preview"
        contents=prompt
    )
    return response.text
