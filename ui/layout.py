def mood_plot(df=None):
    if df is None or df.empty:
        st.info("No mood data to show yet. Start logging your emotions to see insights here!")
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

    st.plotly_chart(fig, use_container_width=True)
