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
# We use 'Significant' directly for the logic
df['Color'] = df['Percent_Change'].apply(lambda x: '#E67E22' if x < -15 else ('#7D9452' if x > 15 else '#D5D8DC'))

# 3. Create the Plot
# We use 'category_orders' to ensure the colors map correctly
fig = px.strip(
    df, 
    x='Percent_Change', 
    hover_name='Species',
    color='Color',
    color_discrete_map="identity",
    stripmode='overlay'
)

# 4. Correct way to handle multiple traces for border widths
# We loop through each trace (Orange, Grey, Green) and apply styling
for trace in fig.data:
    # Get the species names for this specific trace
    trace_species = trace.hovertext
    # Filter original dataframe to find if these species are 'Significant'
    trace_df = df[df['Species'].isin(trace_species)]
    
    # Set the marker properties
    trace.marker.size = 9
    trace.marker.opacity = 0.9
    trace.marker.line.color = 'black'
    # Map the border width list only for the items in this trace
    trace.marker.line.width = [1.5 if s else 0 for s in trace_df['Significant']]

# 5. Formatting the Layout
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
    height=400,
    showlegend=False
)

# 6. Render
st.plotly_chart(fig, use_container_width=True)
st.caption("Each dot represents one species. Outlined dots indicate statistically significant trends.")
