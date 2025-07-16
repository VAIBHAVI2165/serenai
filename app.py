import streamlit as st
from chat.chatbot import get_bot_reply
from emotion.emotion_detector import detect_emotion
from memory.memory_manager import log_emotion, fetch_mood_history, init_db
from ui.layout import render_ui, mood_plot

# Initialize DB
init_db()

# Streamlit config
st.set_page_config(page_title="SerenAI – Your Empathetic AI Companion", page_icon="🌸", layout="wide")

# Render header
render_ui()

# Tabs for Chat and Mood
tab1, tab2 = st.tabs(["💬 Chat", "📈 Mood Timeline"])

with tab1:
    st.subheader("Let's explore your emotions and take care of your mind 💖")
    user_input = st.text_input("You:", "")

    if user_input:
        # Detect emotion
        emotion_label, confidence = detect_emotion(user_input)
        
        # Get bot reply with emotion context
        reply = get_bot_reply(user_input, emotion_label)
        
        # Log emotion into DB
        log_emotion(user_input, emotion_label, confidence)
        
        # Show result
        st.markdown(f"🤖 **SerenAI**: {reply}")
        st.markdown(f"🧠 **Detected Emotion**: _{emotion_label}_ ({confidence*100:.1f}%)")

with tab2:
    st.subheader("📊 Mood Over Time")
    mood_history = fetch_mood_history()
    fig = mood_plot(mood_history)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
