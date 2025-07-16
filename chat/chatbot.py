def get_bot_reply(user_input, emotion):
    if emotion == "sad":
        return "I'm really sorry you're feeling sad. Want to share what’s bothering you?"
    elif emotion == "happy":
        return "That’s wonderful! I’m happy you're feeling good. Want to talk about what made your day?"
    elif emotion == "angry":
        return "It's okay to feel angry sometimes. Want to vent or do something to cool off together?"
    elif emotion == "calm":
        return "That’s peaceful. Let's keep this calm energy going 🧘"
    elif emotion == "anxious":
        return "Take a deep breath. I'm right here with you. Want to try a calming exercise?"
    else:
        return "I’m here for you. Let’s talk about anything on your mind 💬"
