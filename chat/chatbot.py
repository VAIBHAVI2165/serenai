import openai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_bot_reply(user_input, emotion=None):
    # Empathetic system message
    system_prompt = "You are SerenAI, an empathetic AI companion. Respond to the user's messages with emotional intelligence and kindness."
    
    if emotion:
        system_prompt += f" The user appears to be feeling {emotion}. Please respond accordingly."

    # Create a chat completion (new API format)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content
