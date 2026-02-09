import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Butterfly Abundance Chart", layout="wide")

# 2. Generate Mock Data
np.random.seed(42)
n_points = 450
change_data = np.concatenate([
    np.random.normal(-65, 18, 250), 
    np.random.normal(0, 10, 80),    
    np.random.normal(60, 35, 120)   
])
change_data = np.clip(change_data, -98, 140)

df = pd.DataFrame({
    'Species': [f'Species {i}' for i in range(len(change_data))],
    'Percent_Change': change_data,
    'Significant': np.random.choice([True, False], len(change_data), p=[0.4, 0.6])
})

# Add visual helper columns
df['Color'] = df['Percent_Change'].apply(lambda x: '#E67E22' if x < -15 else ('#7D9452' if x > 15 else '#D5D8DC'))
df['Border_Width'] = df['Significant'].apply(lambda x: 1.5 if x else 0)

# 3. Create the Plot
fig = px.strip(
    df, 
    x='Percent_Change', 
    hover_name='Species',
    color='Color',
    color_discrete_map="identity",
    stripmode='overlay'
)

# 4. Styling (Careful with indentation here!)
fig.update_traces(
    marker=dict(size=9, opacity=0.9, line=dict(color='black')),
    marker_line_width=df['Border_Width']
)

fig.update_layout(
    title={'text': "<b>Change in butterfly abundance, 2000-20</b>", 'x': 0.5, 'xanchor': 'center'},
    plot_bgcolor='white',
    xaxis=dict(
        title="",
        range=[-110, 150],
        tickvals=[-100, -75, -50, -25, 0, 25, 50, 75, 100],
        ticktext=['-100%', '-75', '-50', '-25', '0', '+25', '+50', '+75', '+100'],
        side='top',
        gridcolor='#F0F0F0'
    ),
    yaxis=dict(showticklabels=False, title=""),
    height=400
)

# 5. Render
st.plotly_chart(fig, use_container_width=True)
st.caption("Each dot represents one species. Outlined dots indicate statistically significant trends.")
