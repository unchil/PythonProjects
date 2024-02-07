import streamlit as st # web development
import numpy as np # np mean, np random
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop
import plotly.express as px
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="",
    layout="wide",
)

st.title("Real-Time / Live Data Science Dashboard")

dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()

job_filter = st.selectbox("Select the Job", pd.unique(df['job']))

placeholder = st.empty()

df = df[df['job']==job_filter]

#  for seconds in range(200):
#while True:
df['age_new'] = df['age'] * np.random.choice(range(1,5))
df['balance_new'] = df['balance'] * np.random.choice(range(1,5))

avg_age = np.mean(df['age_new'])

count_married = int(df[(df["marital"]=='married')]['marital'].count() + np.random.choice(range(1,30)))

balance = np.mean(df['balance_new'])

with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(label="Age ⏳", value=round(avg_age), delta= round(avg_age) - 10)
    kpi2.metric(label="Married Count 💍", value= int(count_married), delta= - 10 + count_married)
    kpi3.metric(label="A/C Balance ＄", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)


    time.sleep(1)

    #placeholder.empty()

