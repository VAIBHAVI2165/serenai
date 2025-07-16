import streamlit as st
from chat.chatbot import get_bot_reply
from emotion.emotion_detector import detect_emotion
from memory.memory_manager import log_emotion
from ui.layout import render_ui, mood_plot

# Fake mood history for testing
mood_history = [
    ("happy", "2025-07-14 10:00"),
    ("sad", "2025-07-14 13:00"),
    ("angry", "2025-07-14 15:00"),
    ("calm", "2025-07-14 20:00")
]

render_ui()

user_input = st.text_input("You:", "")
if user_input:
    emotion = detect_emotion(user_input)
    reply = get_bot_reply(user_input, emotion)  # ✅ FIXED: passed emotion

    log_emotion(user_input, emotion)
    
    st.write(f"🤖 SerenAI: {reply}")
    st.write(f"🧠 Detected emotion: {emotion}")

# ✅ Pass mood_history to the plot function
fig = mood_plot(mood_history)
if fig:
    st.plotly_chart(fig)