import streamlit as st
from chat.chatbot import get_bot_reply
from emotion.emotion_detector import detect_emotion
from memory.memory_manager import log_emotion, fetch_mood_history
from ui.layout import render_ui, mood_plot

# Set page config
st.set_page_config(page_title="SerenAI – Your Empathetic AI Companion", page_icon="🌸", layout="wide")

# Render UI
render_ui()

# Create tabs
tab1, tab2 = st.tabs(["💬 Chat", "📈 Mood Timeline"])

with tab1:
    st.subheader("Let's explore your emotions and take care of your mind 💖")
    user_input = st.text_input("You:", "")

    if user_input:
        # Detect emotion with confidence
        emotion_label, confidence = detect_emotion(user_input)
        
        # Get chatbot reply tailored to emotion
        reply = get_bot_reply(user_input, emotion_label)
        
        # Log into DB with optional notes
        log_emotion(user_input, emotion_label, confidence)
        
        # Display chatbot reply
        st.markdown(f"🤖 **SerenAI**: {reply}")
        st.markdown(f"🧠 **Detected Emotion**: _{emotion_label}_ ({confidence * 100:.1f}%)")

with tab2:
    st.subheader("📊 Mood Over Time")

    # Fetch from SQLite DB
    mood_history = fetch_mood_history()

    # Plot using Plotly
    fig = mood_plot(mood_history)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
