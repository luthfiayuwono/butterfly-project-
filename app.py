import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Butterfly Abundance Chart", layout="wide")

# 2. Sidebar Filters
st.sidebar.header("Filter Data")

# Range Slider for % Change
range_filter = st.sidebar.slider(
    "Select % Change Range:",
    min_value=-100,
    max_value=150,
    value=(-100, 150)
)

# Toggle for Significance
show_only_significant = st.sidebar.checkbox("Show only statistically significant species")

# 3. Data Generation (Keeping it consistent with previous steps)
np.random.seed(42)
n_points = 450
change_data = np.concatenate([
    np.random.normal(-65, 18, 250), 
    np.random.normal(0, 10, 80),    
    np.random.normal(60, 35, 120)   
])
change_data = np.clip(change_data, -98, 140)
jitter = np.random.uniform(-0.3, 0.3, size=len(change_data))

df = pd.DataFrame({
    'Species': [f'Species {i}' for i in range(len(change_data))],
    'Percent_Change': change_data,
    'Jitter': jitter,
    'Significant': np.random.choice([True, False], len(change_data), p=[0.4, 0.6])
})

# 4. Apply Sidebar Filters to DataFrame
filtered_df = df[
    (df['Percent_Change'] >= range_filter[0]) & 
    (df['Percent_Change'] <= range_filter[1])
]

if show_only_significant:
    filtered_df = filtered_df[filtered_df['Significant'] == True]

# 5. Define Styling Logic
def get_style(row):
    if row['Percent_Change'] < -15:
        color = '#E67E22'
    elif row['Percent_Change'] > 15:
        color = '#7D9452'
    else:
        color = '#D5D8DC'
    line_width = 1.5 if row['Significant'] else 0
    return color, line_width

if not filtered_df.empty:
    styles = filtered_df.apply(get_style, axis=1)
    filtered_df['Color'] = [s[0] for s in styles]
    filtered_df['Line_Width'] = [s[1] for s in styles]

# 6. Create Figure
fig = go.Figure()

if not filtered_df.empty:
    fig.add_trace(go.Scatter(
        x=filtered_df['Percent_Change'],
        y=filtered_df['Jitter'],
        mode='markers',
        marker=dict(
            size=10,
            color=filtered_df['Color'],
            line=dict(width=filtered_df['Line_Width'], color='black'),
            opacity=0.8
        ),
        text=filtered_df['Species'],
        hovertemplate="<b>%{text}</b><br>Change: %{x:.1f}%<extra></extra>"
    ))

# 7. Layout and Formatting
fig.update_layout(
    title={'text': "<b>Change in butterfly abundance, 2000-20</b>", 'x': 0.5, 'xanchor': 'center'},
    plot_bgcolor='white',
    xaxis=dict(
        title="", range=[-110, 150],
        tickvals=[-100, -75, -50, -25, 0, 25, 50, 75, 100],
        ticktext=['-100%', '-75', '-50', '-25', '0', '+25', '+50', '+75', '+100'],
        side='top', gridcolor='#F5F5F5', zeroline=False
    ),
    yaxis=dict(showticklabels=False, range=[-1, 1], fixedrange=True, zeroline=False),
    height=450,
    margin=dict(t=100, b=50, l=50, r=50)
)

# 8. Display
st.plotly_chart(fig, use_container_width=True)

# Metric summary
col1, col2 = st.columns(2)
col1.metric("Species Shown", len(filtered_df))
col2.metric("Significant Trends", len(filtered_df[filtered_df['Significant'] == True]))

st.caption("Each dot represents one species. Outlined dots indicate statistically significant trends.")
