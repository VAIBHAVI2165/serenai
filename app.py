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

# 🌱 Init DB
init_db()

# 🌺 Page config
st.set_page_config(
    page_title="SerenAI – Your Empathetic AI Companion",
    page_icon="🌸",
    layout="wide"
)

# 💄 Optional Styling & Elevated Chat UI
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #fceff9, #e0f7fa);
            background-attachment: fixed;
            font-family: 'Segoe UI', sans-serif;
            color: #333;
        }

        h1, h2, h3, .stTabs, .stSubheader {
            color: #6a1b9a;
        }

        .chat-bubble {
            padding: 0.85rem 1.1rem;
            margin: 0.5rem 0;
            border-radius: 1rem;
            max-width: 80%;
            line-height: 1.5;
            font-size: 1.07rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
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

        .emotion-tag {
            font-size: 0.9rem;
            margin-left: 0.5rem;
            color: #6a1b9a;
        }

        .input-container {
            position: fixed;
            bottom: 2.5rem;
            left: 2.5rem;
            right: 2.5rem;
            background: #fff7fb;
            padding: 0.8rem;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 100;
        }

        .input-container input {
            width: 100%;
            padding: 0.7rem;
            font-size: 1.1rem;
            border-radius: 0.6rem;
            border: 1px solid #f4c2c2;
        }

        .stTextInput > div > div > input {
            background-color: #fff7fb !important;
            color: #333 !important;
        }

        #MainMenu, footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# 🌷 Render Header
render_ui()

# 🌸 Tabs
tab1, tab2 = st.tabs(["💬 Chat", "📈 Mood Timeline"])

with tab1:
    st.subheader("Let's explore your emotions and take care of your mind 💖")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render chat history
    for role, message in st.session_state.messages:
        if role == "user":
            st.markdown(f"<div class='chat-bubble user'>🧑‍💬 {message}</div>", unsafe_allow_html=True)
        elif role == "bot":
            st.markdown(f"<div class='chat-bubble bot'>🤖 {message}</div>", unsafe_allow_html=True)
        elif role == "emotion":
            st.markdown(f"<div class='emotion-tag'>🧠 <em>Detected Emotion</em>: {message}</div>", unsafe_allow_html=True)

    # Input bar
    with st.container():
        user_input = st.text_input("You:", placeholder="Type a message and press Enter...", key="chat_input")

        if user_input:
            # 1. Detect emotion
            emotion_label, confidence = detect_emotion(user_input)

            # 2. Get bot reply
            bot_reply = get_bot_reply(user_input, emotion_label)

            # 3. Log emotion
            log_emotion(emotion_label, confidence, user_input)

            # 4. Save chat to session state
            st.session_state.messages.append(("user", user_input))
            st.session_state.messages.append(("bot", bot_reply))
            st.session_state.messages.append(("emotion", f"{emotion_label} ({confidence * 100:.1f}%)"))

            # Clear input field
            st.experimental_rerun()

with tab2:
    st.subheader("📊 Mood Over Time")
    mood_history = fetch_mood_history()
    fig = mood_plot(mood_history)

    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No mood data yet. Start chatting with SerenAI to see your emotion history!")
