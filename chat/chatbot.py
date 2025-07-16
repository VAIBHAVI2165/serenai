import os
from dotenv import load_dotenv
import openai

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client instance (✅ SDK v1+ requirement)
client = openai.OpenAI(api_key=api_key)

def get_bot_reply(user_input, emotion=None):
    system_prompt = "You are SerenAI, an empathetic AI companion. Respond to the user's messages with emotional intelligence and kindness."

    if emotion:
        system_prompt += f" The user appears to be feeling {emotion}. Please respond accordingly."

    # ✅ Use a valid and accessible model name
    response = client.chat.completions.create(
        model="gpt-4o",  # <-- Updated from "gpt-4"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content
