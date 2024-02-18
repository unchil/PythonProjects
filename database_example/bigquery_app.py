import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from streamlit_plotly_events import plotly_events
import plotly.express as px
@st.cache_resource
def get_bigquery_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["bigquery_service_account"]
    )
    return bigquery.Client(credentials=credentials)

st.title("BigQuery App")

days_lookback = st.slider(
"How many days of data do you want to see?",
    min_value=1, max_value=30, value=5
)


client = get_bigquery_client()

@st.cache_data
def get_result(days_lookback):
    query = f"""
    SELECT
        CAST(timestamp AS DATE ) as date,
        file.project as project,
        count(*) as count
    FROM `bigquery-public-data.pypi.file_downloads`
    WHERE file.project in ( 'streamlit', 'dash', 'jupyter')
    AND timestamp < DATETIME_TRUNC(current_timestamp(), DAY) 
    AND timestamp >= timestamp_add( DATETIME_TRUNC(current_timestamp(), DAY) , INTERVAL -({days_lookback}) DAY )
    GROUP BY date, project
    ORDER BY date, project desc
"""
    return client.query(query).to_dataframe()

results = get_result(days_lookback)

st.write("Comparing data dashboarding tools and frameworks")

st.write(f"{days_lookback} Days Project File Downloads Count ")

st.dataframe(results, height=200)

st.write("streamlit line chart:")
st.line_chart(results, x='date', y='count', color='project')

color_map = {'streamlit':'red', 'dash':'blue', 'jupyter':'orange'}

st.write("streamlit_plotly_events line chart:")
fig1 = px.line(results, x="date", y="count", symbol="project", color="project", color_discrete_map=color_map, markers=True)
event1 = plotly_events(fig1)

st.write("streamlit_plotly_events area chart:")
fig2 = px.area(results, x="date", y="count", symbol="project", color="project", color_discrete_map=color_map, markers=True)
event2 = plotly_events(fig2, click_event=True)