# ui/layout.py

import streamlit as st
import plotly.express as px
import pandas as pd

def render_ui():
    # 🌸 Centered, calm title
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 3em; color: #D988BC;">🌸 SerenAI</h1>
            <h3 style="color: #A569BD;">Your Empathetic AI Companion</h3>
            <p style="font-size: 1.2em; color: #566573;">
                Let’s explore your emotions and take care of your mind 💖
            </p>
        </div>
    """, unsafe_allow_html=True)

def mood_plot(df):
    if df is None or df.empty:
        return None

    df['date'] = pd.to_datetime(df['date'])
    df['intensity'] = df['intensity'].astype(float)

    fig = px.line(
        df,
        x='date',
        y='intensity',
        color='emotion',
        markers=True,
        title='📈 Emotional Intensity Over Time',
        labels={'date': 'Date', 'intensity': 'Intensity (%)', 'emotion': 'Emotion'},
        hover_data={'trigger': True, 'user_note': True}
    )

    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
        height=500,
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Helvetica, sans-serif", size=14),
        legend_title_text='Emotion'
    )

    fig.update_traces(mode="lines+markers", line_shape="spline")

    return fig
