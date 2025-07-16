import plotly.graph_objects as go

def mood_plot(mood_history):
    if not mood_history:
        return

    moods, timestamps = zip(*mood_history)

    fig = go.Figure(data=go.Scatter(
        x=timestamps,
        y=moods,
        mode='lines+markers',
        name='Mood Timeline'
    ))

    fig.update_layout(title='Your Mood Over Time',
                      xaxis_title='Time',
                      yaxis_title='Mood')

    return fig