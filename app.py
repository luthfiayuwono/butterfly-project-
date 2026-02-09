import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Butterfly Abundance Chart", layout="wide")

# 2. Generate Data
np.random.seed(42)
n_points = 450
change_data = np.concatenate([
    np.random.normal(-65, 18, 250), 
    np.random.normal(0, 10, 80),    
    np.random.normal(60, 35, 120)   
])
change_data = np.clip(change_data, -98, 140)

# Create jitter (y-values) to create the "swarm" effect
jitter = np.random.uniform(-0.3, 0.3, size=len(change_data))

df = pd.DataFrame({
    'Species': [f'Species {i}' for i in range(len(change_data))],
    'Percent_Change': change_data,
    'Jitter': jitter,
    'Significant': np.random.choice([True, False], len(change_data), p=[0.4, 0.6])
})

# Define Colors & Borders
def get_style(row):
    if row['Percent_Change'] < -15:
        color = '#E67E22' # Orange
    elif row['Percent_Change'] > 15:
        color = '#7D9452' # Green
    else:
        color = '#D5D8DC' # Grey
    
    line_width = 1.5 if row['Significant'] else 0
    return color, line_width

styles = df.apply(get_style, axis=1)
df['Color'] = [s[0] for s in styles]
df['Line_Width'] = [s[1] for s in styles]

# 3. Create Figure using Graph Objects (The most stable method)
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Percent_Change'],
    y=df['Jitter'],
    mode='markers',
    marker=dict(
        size=10,
        color=df['Color'],
        line=dict(
            width=df['Line_Width'],
            color='black'
        ),
        opacity=0.8
    ),
    text=df['Species'],
    hovertemplate="<b>%{text}</b><br>Change: %{x:.1f}%<extra></extra>"
))

# 4. Replicate the Chart Layout
fig.update_layout(
    title={'text': "<b>Change in butterfly abundance, 2000-20</b>", 'x': 0.5, 'xanchor': 'center'},
    plot_bgcolor='white',
    xaxis=dict(
        title="",
        range=[-110, 150],
        tickvals=[-100, -75, -50, -25, 0, 25, 50, 75, 100],
        ticktext=['-100%', '-75', '-50', '-25', '0', '+25', '+50', '+75', '+100'],
        side='top',
        gridcolor='#F5F5F5',
        zeroline=False
    ),
    yaxis=dict(showticklabels=False, range=[-1, 1], fixedrange=True, zeroline=False),
    height=400,
    margin=dict(t=100, b=50, l=50, r=50)
)

# 5. Render
st.plotly_chart(fig, use_container_width=True)
st.caption("Each dot represents one species. Outlined dots indicate statistically significant trends. Data for the contiguous U.S.")
