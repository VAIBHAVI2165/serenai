import streamlit as st
from chat.chatbot import get_bot_reply
from emotion.emotion_detector import detect_emotion
from memory.memory_manager import log_emotion, fetch_mood_history
from ui.layout import mood_plot

st.set_page_config(page_title="SerenAI – Your Empathetic AI Companion", page_icon="🌸", layout="centered")

# ----- CSS Styling -----
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background-color: #30002f;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .stChatMessage {
        padding: 10px 16px;
        border-radius: 12px;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 16px;
    }
    .stChatMessage.user {
        background-color: #2e8bff;
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    .stChatMessage.assistant {
        background-color: #ffb3d9;
        color: black;
        align-self: flex-start;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ----- Header -----
st.title("🌸 SerenAI – Your Empathetic AI Companion")
st.markdown("Chat with me and explore your emotions 💬")

# ----- Session state -----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----- Chat Display -----
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f'<div class="stChatMessage user"><b>You:</b> {user_msg}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stChatMessage assistant"><b>SerenAI:</b> {bot_msg}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ----- Input -----
st.markdown("### ✍️ Type your message")
col1, col2 = st.columns([8, 2])
with col1:
    user_input = st.text_input("Your message:", key="user_input", label_visibility="collapsed", value="")
with col2:
    send_clicked = st.button("Send")

if (send_clicked or user_input.strip()):
    with st.spinner("SerenAI is thinking... 💭"):
        emotion_data = detect_emotion(user_input)
        reply = get_bot_reply(user_input, emotion_data)
        st.session_state.chat_history.append((user_input, reply))

        # Safely extract values
        if isinstance(emotion_data, dict):
            emotion = emotion_data.get("label", "neutral")
            try:
                intensity = float(emotion_data.get("intensity", 0.5))
            except ValueError:
                intensity = 0.5
            trigger = emotion_data.get("trigger", "")
        else:
            emotion = str(emotion_data)
            intensity = 0.5
            trigger = ""

        try:
            log_emotion(emotion, intensity, trigger, user_note=user_input)
        except Exception as e:
            st.warning(f"Error logging emotion: {e}")

    st.session_state.user_input = ""  # Clear input
    st.rerun()

# ----- Mood Timeline -----
st.markdown("## 🌈 Your Mood Timeline")
df = fetch_mood_history()
if df is not None and not df.empty:
    mood_plot(df)
else:
    st.info("No mood data yet. Start chatting to log your emotions!")
