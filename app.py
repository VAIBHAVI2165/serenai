import streamlit as st
from chat.chatbot import get_bot_reply
from emotion.emotion_detector import detect_emotion
from memory.memory_manager import log_emotion
from ui.layout import mood_plot

st.set_page_config(page_title="SerenAI – Your Empathetic AI Companion", page_icon="🌸", layout="centered")

# ----- CSS Styling -----
st.markdown("""
    <style>
    body {
        background-color: #f7f5fa;
    }
    .stChatMessage {
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 10px;
        max-width: 85%;
        word-wrap: break-word;
    }
    .stChatMessage.user {
        background-color: #e6f0ff;
        align-self: flex-end;
    }
    .stChatMessage.assistant {
        background-color: #fff0f5;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ----- Header -----
st.title("🌸 SerenAI – Your Empathetic AI Companion")
st.markdown("Chat with me and explore your emotions 💬")

# ----- Initialize session state -----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----- Chat Container -----
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f'<div class="stChatMessage user"><b>You:</b> {user_msg}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stChatMessage assistant"><b>SerenAI:</b> {bot_msg}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ----- Message Input -----
st.markdown("### ✍️ Type your message")

col1, col2 = st.columns([8, 2])
with col1:
    user_input = st.text_input("Your message:", key="user_input", label_visibility="collapsed")
with col2:
    send_clicked = st.button("Send")

if (send_clicked or user_input) and user_input.strip():
    with st.spinner("SerenAI is thinking... 💭"):
        emotion = detect_emotion(user_input)
        reply = get_bot_reply(user_input, emotion)
        st.session_state.chat_history.append((user_input, reply))
        log_emotion(emotion)
    st.experimental_set_query_params()  # refresh page params without rerun
    st.rerun()  # this replaces experimental_rerun()

# ----- Mood Timeline -----
st.markdown("## 🌈 Your Mood Timeline")
mood_plot()
