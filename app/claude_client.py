import anthropic
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Debug: Print key (ONLY TEMPORARILY - REMOVE AFTER CONFIRMING)
print("🔐 Loaded API key:", os.getenv("ANTHROPIC_API_KEY"))

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Summarize function
def summarize_investor(profile: str):
    prompt = f"You're an elite investor relations strategist.Summarize this investor's background, interests, and optimal targeting strategy for our next round. Keep it concise, sharp, and focused on pitch alignment: {profile}"
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        temperature=0.5,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
