import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="NFHS Dashboard", layout="wide")

st.title("📊 National Family Health Survey Dashboard")

# Load Data
@st.cache_data
def load_data():
    file_path = "/mnt/data/All India National Family Health Survey1.xlsx"
    df = pd.read_excel(file_path)
    return df

df = load_data()

# Show raw data option
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

st.sidebar.header("Filter Options")

# Select State (if available in data)
if "State" in df.columns:
    selected_state = st.sidebar.selectbox("Select State", df["State"].unique())
    df = df[df["State"] == selected_state]

# Select Indicator (numerical columns)
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

selected_indicator = st.sidebar.selectbox(
    "Select Indicator",
    numeric_columns
)

# KPI Display
st.subheader(f"📌 {selected_indicator} Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Average", round(df[selected_indicator].mean(), 2))
col2.metric("Maximum", round(df[selected_indicator].max(), 2))
col3.metric("Minimum", round(df[selected_indicator].min(), 2))

# Bar Chart (if District column exists)
if "District" in df.columns:
    fig = px.bar(
        df,
        x="District",
        y=selected_indicator,
        title=f"{selected_indicator} by District",
    )
    st.plotly_chart(fig, use_container_width=True)

# Line Chart (if Year column exists)
if "Year" in df.columns:
    fig2 = px.line(
        df,
        x="Year",
        y=selected_indicator,
        title=f"{selected_indicator} Trend Over Years",
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

st.success("Dashboard Loaded Successfully ✅")
