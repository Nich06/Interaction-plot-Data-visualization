import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# WEB PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Students Performance Analysis", layout="wide")
st.title("Students Performance Analysis")
st.markdown("Use the controls below to explore factors that influence final grades.")

# ==========================================
# DATA LOADING & CLEANING
# ==========================================
# The @st.cache_data decorator prevents reloading data every time the dropdown changes
@st.cache_data
def load_data():
    path = "student-mat.csv" 
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")
    df = pd.read_csv(path, sep=';')
    selected_columns = ['sex', 'studytime', 'freetime', 'goout', 'absences', 'activities', 'romantic', 'internet', 'G3']
    df_clean = df[selected_columns].copy()
    
    # Normalize output variables
    df_clean['sex'] = df_clean['sex'].replace({'F': 'female', 'M': 'male'})
    studytime_order = ['<2 hours', '2-5 hours', '5-10 hours', '>10 hours']
    time_scale_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']

    df_clean['studytime'] = df_clean['studytime'].replace({
        1: '<2 hours',
        2: '2-5 hours',
        3: '5-10 hours',
        4: '>10 hours'
    }).astype(pd.CategoricalDtype(categories=studytime_order, ordered=True))
    df_clean['freetime'] = df_clean['freetime'].replace({
        1: 'Very Low',
        2: 'Low',
        3: 'Medium',
        4: 'High',
        5: 'Very High'
    }).astype(pd.CategoricalDtype(categories=time_scale_order, ordered=True))
    df_clean['goout'] = df_clean['goout'].replace({
        1: 'Very Low',
        2: 'Low',
        3: 'Medium',
        4: 'High',
        5: 'Very High'
    }).astype(pd.CategoricalDtype(categories=time_scale_order, ordered=True))
    df_clean['G3_100'] = df_clean['G3'] * 5
    
    return df_clean

df_clean = load_data()

# ==========================================
# INTERACTIVE WIDGETS
# ==========================================
# Use two columns for a cleaner dropdown layout
col1, col2 = st.columns(2)

x_axis_labels = {
    'studytime': 'Study Time',
    'freetime': 'Free Time',
    'goout': 'Hang Out',
    'absences': 'Absences'
}
split_by_labels = {
    'romantic': 'Romantic Relationship',
    'sex': 'Gender',
    'internet': 'Internet Access',
    'activities': 'Extracurricular Activities'
}

with col1:
    x_var = st.selectbox(
        "Choose X Axis (Main Variable):",
        ['studytime', 'freetime', 'goout', 'absences'],
        format_func=lambda x: x_axis_labels[x]
    )

with col2:
    split_by = st.selectbox(
        "Choose Color Category:",
        ['romantic', 'sex', 'internet', 'activities'],
        format_func=lambda x: split_by_labels[x]
    )

# ==========================================
# PLOTLY GRAPH CREATION
# ==========================================
category_orders = {
    'studytime': ['<2 hours', '2-5 hours', '5-10 hours', '>10 hours'],
    'freetime': ['Very Low', 'Low', 'Medium', 'High', 'Very High'],
    'goout': ['Very Low', 'Low', 'Medium', 'High', 'Very High']
}

fig = px.box(
    df_clean,
    x=x_var,
    y='G3_100',
    color=split_by,
    points='all',
    labels={
        'G3_100': 'Final Grade (Scale 100)',
        'sex': 'Gender'
    },
    color_discrete_sequence=px.colors.qualitative.Pastel,
    category_orders={x_var: category_orders.get(x_var, [])},
    title='Final Grade Distribution by Category'
)

# Add safe target reference line
fig.add_hline(
    y=80,
    line_dash='dash',
    line_color='red',
    annotation_text='Safe Target (>80)',
    annotation_position='bottom right'
)

# Clean up visual appearance
fig.update_layout(
    xaxis_title=x_axis_labels[x_var],
    yaxis_title='Final Grade',
    plot_bgcolor='white'
)
fig.update_yaxes(gridcolor='lightgrey')

# Render the chart on the page
st.plotly_chart(fig, width='stretch')