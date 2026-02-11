import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="NFHS Dashboard", layout="wide")

st.title("📊 National Family Health Survey Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey1.xlsx")
    return df

df = load_data()

# Show dataset info
st.sidebar.header("Filter Options")

# ---- Dynamic Filters ---- #

# State Filter (if exists)
if "State" in df.columns:
    state = st.sidebar.selectbox("Select State", ["All"] + list(df["State"].dropna().unique()))
    if state != "All":
        df = df[df["State"] == state]

# District Filter (if exists)
if "District" in df.columns:
    district = st.sidebar.selectbox("Select District", ["All"] + list(df["District"].dropna().unique()))
    if district != "All":
        df = df[df["District"] == district]

# Select Indicator (numeric columns only)
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

indicator = st.sidebar.selectbox("Select Indicator", numeric_cols)

# ---- KPI Section ---- #

st.subheader(f"📌 {indicator} Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Average", round(df[indicator].mean(), 2))
col2.metric("Maximum", round(df[indicator].max(), 2))
col3.metric("Minimum", round(df[indicator].min(), 2))

st.divider()

# ---- Charts Section ---- #

# Bar Chart (District wise)
if "District" in df.columns:
    st.subheader("District-wise Comparison")
    fig_bar = px.bar(
        df,
        x="District",
        y=indicator,
        title=f"{indicator} by District"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Line Chart (Year wise)
if "Year" in df.columns:
    st.subheader("Trend Over Years")
    fig_line = px.line(
        df,
        x="Year",
        y=indicator,
        markers=True,
        title=f"{indicator} Trend"
    )
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# Raw Data
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

st.success("Dashboard Loaded Successfully ✅")
