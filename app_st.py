import streamlit as st # web development
import numpy as np # np mean, np random
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop
import plotly.express as px
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


st.title("Real-Time / Live Data Science Dashboard")

dataset_url = "https://github.com/unchil/PythonProjects/blob/main/penguins.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()



st.markdown("### Detailed Data View")
st.dataframe(df)
