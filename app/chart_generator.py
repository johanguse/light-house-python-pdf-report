import plotly.graph_objects as go
import plotly.express as px
from reportlab.platypus import Image
from reportlab.lib.units import inch
from io import BytesIO

def create_gauge_chart(score, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        title={'text': title, 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'red'},
                {'range': [50, 90], 'color': 'yellow'},
                {'range': [90, 100], 'color': 'green'}
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="lavender",
        font={'color': "darkblue", 'family': "Arial"}
    )
    img_bytes = fig.to_image(format="png", width=300, height=200)
    return Image(BytesIO(img_bytes), width=3*inch, height=2*inch)

def create_bar_chart(data):
    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        title="Load Time Breakdown",
        labels={'x': 'Metric', 'y': 'Time (seconds)'},
        color=list(data.values()),
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        paper_bgcolor="lavender",
        plot_bgcolor="lavender",
        font={'color': "darkblue", 'family': "Arial"}
    )
    img_bytes = fig.to_image(format="png", width=600, height=300)
    return Image(BytesIO(img_bytes), width=6*inch, height=3*inch)