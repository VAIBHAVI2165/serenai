# ui/layout.py
import streamlit as st
import pandas as pd
import plotly.express as px

def render_ui():
    st.markdown("# 🌸 SerenAI – Your Empathetic AI Companion")
    st.markdown("Let’s explore your emotions and take care of your mind 💖")

def mood_plot(mood_history):
    if not mood_history:
        return None

    mood_to_score = {"sad": 0, "anxious": 1, "calm": 2, "happy": 3, "angry": 4}
    df = pd.DataFrame(mood_history, columns=["emotion", "timestamp"])
    df["score"] = df["emotion"].map(mood_to_score)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = px.line(df, x="timestamp", y="score", text="emotion",
                  labels={"score": "Mood", "timestamp": "Time"},
                  title="Mood Over Time")
    fig.update_traces(mode="lines+markers+text", textposition="top center")
    fig.update_layout(yaxis=dict(
        tickvals=[0, 1, 2, 3, 4],
        ticktext=["sad", "anxious", "calm", "happy", "angry"]
    ))
    return fig
