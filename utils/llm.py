from dotenv import load_dotenv
load_dotenv()
from google import genai

# Initialize client (API key auto from env: GEMINI_API_KEY)
client = genai.Client()

def call_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",   # or "gemini-3-flash-preview"
        contents=prompt
    )
    return response.text
