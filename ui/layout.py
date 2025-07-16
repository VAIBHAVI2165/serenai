import plotly.graph_objects as go

def render_ui():
    import streamlit as st
    st.title("🌸 SerenAI – Your Empathetic AI Companion")
    st.write("Let’s explore your emotions and take care of your mind 💖")

def mood_plot(mood_history):
    import datetime
    if not mood_history:
        return None

    moods, timestamps = zip(*mood_history)
    timestamps = [datetime.datetime.strptime(t, "%Y-%m-%d %H:%M") for t in timestamps]

    mood_to_num = {
        "sad": 1,
        "anxious": 2,
        "calm": 3,
        "happy": 4,
        "angry": 5
    }

    y_vals = [mood_to_num.get(mood, 0) for mood in moods]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=y_vals,
        mode="lines+markers",
        line=dict(shape='spline', smoothing=1.3, color='purple'),
        name="Mood"
    ))

    fig.update_layout(
        title="🧠 Mood Over Time",
        xaxis_title="Timestamp",
        yaxis=dict(
            title="Mood",
            tickmode='array',
            tickvals=list(mood_to_num.values()),
            ticktext=list(mood_to_num.keys())
        )
    )

    return fig