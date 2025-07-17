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

    .stMarkdown {
        font-size: 1.1rem;
        color: #333;
        background-color: #fff9fc;
        padding: 0.75rem;
        border-radius: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ad1457;
    }
    </style>
""", unsafe_allow_html=True)

# 🌱 Initialize DB
init_db()

# 🌺 Page config
st.set_page_config(
    page_title="SerenAI – Your Empathetic AI Companion",
    page_icon="🌸",
    layout="wide"
)

# 🌷 Render top UI
render_ui()

# 🌼 Chat and Mood Timeline tabs
tab1, tab2 = st.tabs(["💬 Chat", "📈 Mood Timeline"])

# 💬 Chat interaction
with tab1:
    st.subheader("Let's explore your emotions and take care of your mind 💖")
    user_input = st.text_input("You:", "")

    if user_input:
        # Step 1: Emotion detection
        emotion_label, confidence = detect_emotion(user_input)

        # Step 2: Get reply from chatbot
        reply = get_bot_reply(user_input, emotion_label)

        # Step 3: Log emotion
        log_emotion(emotion_label, confidence, user_input)

        # Step 4: Show bot reply
        st.markdown(f"""
        <div style='background-color:#fff9fc; padding:1rem; border-radius:1rem; margin:1rem 0; color:#333;'>
        🤖 <strong>SerenAI</strong>: {reply}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"🧠 **Detected Emotion**: _{emotion_label}_ ({confidence * 100:.1f}%)")

# 📈 Mood graph
with tab2:
    st.subheader("📊 Mood Over Time")
    mood_history = fetch_mood_history()
    fig = mood_plot(mood_history)

    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No mood data yet. Start chatting with SerenAI to see your emotion history!")
