import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Butterfly Abundance Chart", layout="wide")

# Custom CSS for fonts and styling
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .title { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Generate Mock Data
np.random.seed(42)
n_points = 450
change_data = np.concatenate([
    np.random.normal(-65, 18, 250), # Large group declining
    np.random.normal(0, 10, 80),    # Stable group
    np.random.normal(60, 35, 120)   # Improving group
])
change_data = np.clip(change_data, -98, 140)

df = pd.DataFrame({
    'Species': [f'Species {i}' for i in range(len(change_data))],
    'Percent_Change': change_data,
    'Significant': np.random.choice([True, False], len(change_data), p=[0.4, 0.6])
})

# 3. Logic for Visual Styles
def get_color(val):
    if val < -15: return '#E67E22'  # Orange-ish
    if val > 15: return '#7D9452'   # Muted Green
    return '#D5D8DC'                # Light Grey

df['Color'] = df['Percent_Change'].apply(get_color)

# 4. Create the Interactive Beeswarm (Strip Plot)
fig = px.strip(
    df, 
    x='Percent_Change', 
    hover_name='Species',
    color='Color',
    color_discrete_map="identity",
    stripmode='overlay'
)

# 5. Styling to match your original image
fig.update_traces(
    marker=dict(
        size=9, 
        opacity=0.9,
        line=dict(
            width=df['Significant'].apply(lambda x: 1.5 if x else 0),
            color='black'
        )
    )
)

fig.update_layout(
    title={
        'text': "<b>Change in butterfly abundance, 2000-20</b>",
        'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top',
        'font': dict(size=24, color='#333333')
    },
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        title="",
        range=[-110, 150],
        tickvals=[-100, -75, -50, -25, 0, 25, 50, 75, 100],
        ticktext=['-100%', '-75', '-50', '-25', '0', '+25', '+50', '+75', '+100'],
        side='top',
        gridcolor='#F0F0F0'
    ),
    yaxis=dict(showticklabels=False, title=""),
    height=400,
    margin=dict(l=50, r=50, t=100, b=50)
)

# 6. Render in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Footer text
st.caption("Each dot represents one species. Outlined dots indicate statistically significant trends.")
