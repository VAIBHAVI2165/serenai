# chatbot.py
import openai
import os
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")  # Store in .env or set manually

def get_bot_reply(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an empathetic companion who replies gently and supportively."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response['choices'][0]['message']['content']
