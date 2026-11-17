import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("earthquakes_cleaned.csv")

st.set_page_config(
    page_title= "Global Seismic Trends",
    layout="wide"
)
st.title("Global Seismic Trends Dashboard") 


# KPI SECTION

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Total Earthquakes",
        len(df)
    )

with col2:
    st.metric(
        "Maximum Magnitude",
        round(df["mag"].max(),2)
    )

with col3:
    st.metric(
        "Countries",
        df["country"].nunique()
    )

with col4:
    st.metric(
        "Tsunami Events",
        int(df["tsunami"].sum())
    )



    # COUNTRY FILTER

country = st.selectbox(
    "Select Country",
    sorted(df["country"].unique())
)

filtered_df = df[
    df["country"] == country
]


# Magnitude Histogram

fig = px.histogram(
    filtered_df,
    x="mag",
    color="mag_Category",
    title="Magnitude Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Year Trend

year_data = filtered_df.groupby(
    "year"
).size().reset_index(name="Count")

fig2 = px.line(
    year_data,
    x="year",
    y="Count",
    title="Earthquakes by Year"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# World Map

fig3 = px.scatter_geo(
    filtered_df,
    lat="latitude",
    lon="longitude",
    color="mag",
    size="mag",
    hover_name="place",
    title="Earthquake Locations"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# Depth Category Pie Chart

depth_count = filtered_df[
    "depth_category"
].value_counts()

fig4 = px.pie(
    values=depth_count.values,
    names=depth_count.index,
    title="Depth Category Distribution"
)

st.plotly_chart(fig4)


# Tsunami Analysis

tsunami_count = df["tsunami"].value_counts()

fig = px.pie(
    values=tsunami_count.values,
    names=["No Tsunami","Tsunami"],
    title="Tsunami Event Distribution"
)

st.plotly_chart(fig)