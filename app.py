# app.py

import streamlit as st
from chat.chatbot import get_bot_reply
from emotion.emotion_detector import detect_emotion
from memory.memory_manager import log_emotion, fetch_mood_history, init_db
from ui.layout import render_ui, mood_plot

# 🌸 Background and Theme Styling
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.ibb.co/3hkQw4k/calm-pink-gradient.png');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Helvetica', sans-serif;
    }
    input, textarea {
        background-color: #fff0f5 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🌱 Initialize database
init_db()

# 🌸 Streamlit page config
st.set_page_config(
    page_title="SerenAI – Your Empathetic AI Companion",
    page_icon="🌸",
    layout="wide"
)

# 🌼 Render header
render_ui()

# 🧭 Tabs for Chat and Mood
tab1, tab2 = st.tabs(["💬 Chat", "📈 Mood Timeline"])

# 💬 Chatbot interaction
with tab1:
    st.subheader("Let's explore your emotions and take care of your mind 💖")
    user_input = st.text_input("You:", "")

    if user_input:
        # Detect emotion
        emotion_label, confidence = detect_emotion(user_input)

        # Get bot reply
        reply = get_bot_reply(user_input, emotion_label)

        # Log emotion
        log_emotion(emotion_label, confidence, user_input)

        # Show response
        st.markdown(f"🤖 **SerenAI**: {reply}")
        st.markdown(f"🧠 **Detected Emotion**: _{emotion_label}_ ({confidence * 100:.1f}%)")

# 📈 Mood timeline visualization
with tab2:
    st.subheader("📊 Mood Over Time")

    mood_history = fetch_mood_history()
    fig = mood_plot(mood_history)

    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No mood data yet. Start chatting with SerenAI to see your emotion history!")
