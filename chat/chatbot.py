# chat/chatbot.py
import os
from dotenv import load_dotenv
from together import Together

# Load API key securely from .env
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

# Ensure key is present
if not api_key:
    raise ValueError("TOGETHER_API_KEY not found in environment variables.")

# Create Together client
client = Together(api_key=api_key)

def get_bot_reply(user_input, emotion=None):
    system_prompt = "You are SerenAI, an empathetic AI companion. Respond to the user's messages with emotional intelligence and kindness."

    if emotion:
        system_prompt += f" The user appears to be feeling {emotion}. Please respond accordingly."

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content
