import streamlit as st
from chat.chatbot import get_bot_reply
from emotion.emotion_detector import detect_emotion
from memory.memory_manager import log_emotion
from ui.layout import mood_plot

st.set_page_config(page_title="SerenAI", page_icon="🌙", layout="wide")

# Tabs
tab1, tab2 = st.tabs(["💬 Chat", "📈 Mood Tracker"])

# Chat tab
with tab1:
    st.title("💬 SerenAI - Your Emotional Wellness Companion")
    user_input = st.text_input("What's on your mind today?")

    if user_input:
        emotion = detect_emotion(user_input)
        response = get_bot_reply(user_input, emotion)
        log_emotion(emotion, user_input)
        
        st.markdown(f"**You feel:** _{emotion}_")
        st.markdown(f"**SerenAI says:** {response}")

# Mood Tracker
with tab2:
    st.title("📈 Your Mood Timeline")
    mood_plot()
