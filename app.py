# app.py

import os
import streamlit as st
from dotenv import load_dotenv
from chat.chatbot import get_bot_reply
from emotion.emotion_detector import detect_emotion
from memory.memory_manager import log_emotion, fetch_mood_history, init_db
from ui.layout import render_ui, mood_plot

# 🌿 Load environment variables
load_dotenv()

# 🌸 Streamlit Theme & Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #fceff9, #e0f7fa);
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
        color: #333;
    }

    .chat-bubble {
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        border-radius: 1rem;
        max-width: 75%;
        line-height: 1.4;
        font-size: 1.05rem;
    }

    .user {
        background-color: #f8bbd0;
        margin-left: auto;
        color: #000;
    }

    .bot {
        background-color: #e1bee7;
        margin-right: auto;
        color: #000;
    }

    .stTextInput > div > div > input {
        background-color: #fff7fb !important;
        border: 1px solid #f4c2c2 !important;
        color: #222 !important;
        padding: 0.5rem !important;
        font-size: 1.1rem;
        border-radius: 0.5rem;
    }

    h1, h2, h3, .stTabs, .stSubheader {
        color: #6a1b9a;
    }
    </style>
""", unsafe_allow_html=True)

# 🌱 Init DB
init_db()

# 🌺 Page config
st.set_page_config(
    page_title="SerenAI – Your Empathetic AI Companion",
    page_icon="🌸",
    layout="wide"
)

# 🌷 Render UI
render_ui()

# 💬 Chat tab
tab1, tab2 = st.tabs(["💬 Chat", "📈 Mood Timeline"])

with tab1:
    st.subheader("Let's explore your emotions and take care of your mind 💖")

    # Initialize conversation state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Input box
    user_input = st.text_input("You:", "", key="chat_input")

    if user_input:
        # 1. Detect emotion
        emotion_label, confidence = detect_emotion(user_input)

        # 2. Get reply
        bot_reply = get_bot_reply(user_input, emotion_label)

        # 3. Log emotion
        log_emotion(emotion_label, confidence, user_input)

        # 4. Save messages
        st.session_state.messages.append(("user", user_input))
        st.session_state.messages.append(("bot", bot_reply))
        st.session_state.messages.append(("emotion", f"{emotion_label} ({confidence * 100:.1f}%)"))

    # Show conversation
    for role, message in st.session_state.messages:
        if role == "user":
            st.markdown(f"<div class='chat-bubble user'>🧑‍💬 {message}</div>", unsafe_allow_html=True)
        elif role == "bot":
            st.markdown(f"<div class='chat-bubble bot'>🤖 {message}</div>", unsafe_allow_html=True)
        elif role == "emotion":
            st.markdown(f"<div style='font-size: 0.9rem; margin-left: 0.5rem;'>🧠 <em>Detected Emotion</em>: {message}</div>", unsafe_allow_html=True)

# 📈 Mood timeline
with tab2:
    st.subheader("📊 Mood Over Time")
    mood_history = fetch_mood_history()
    fig = mood_plot(mood_history)

    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No mood data yet. Start chatting with SerenAI to see your emotion history!")
