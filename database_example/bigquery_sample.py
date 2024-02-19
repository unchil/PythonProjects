import streamlit as st
from streamlit_plotly_events import plotly_events
import plotly.express as px

st.set_page_config(layout="centered")
st.title("BigQuery App sample using streamlit")
st.subheader("Daily download count of selected projects")

"""
Create Client:
"""
with st.echo():
    from google.oauth2 import service_account
    from google.cloud import bigquery

    @st.cache_resource
    def get_bigquery_client():
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["bigquery_service_account"]
        )
        return bigquery.Client(credentials=credentials)

client = get_bigquery_client()

selected_project = st.sidebar.multiselect(
    label='ProjectName',
    options=['streamlit', 'dash', 'jupyter'],
    default=['streamlit', 'dash', 'jupyter']
)

days_lookback = st.sidebar.slider(
    label="How many days of data do you want to see?",
    min_value=1, max_value=30, value=5
)

"""
Make Query and Execute: 
"""
with st.echo():
    @st.cache_data
    def get_result(selected_project, days_lookback):
        query = """
        SELECT
            CAST(timestamp AS DATE ) as date,
            file.project as project,
            count(*) as count
        FROM `bigquery-public-data.pypi.file_downloads`
        WHERE file.project IN UNNEST(@projects)
        AND timestamp < DATETIME_TRUNC(current_timestamp(), DAY) 
        AND timestamp >= timestamp_add( DATETIME_TRUNC(current_timestamp(), DAY) , INTERVAL -(@lookback) DAY )
        GROUP BY date, project
        ORDER BY date DESC , project ASC
    """
        job_config = bigquery.QueryJobConfig(
            use_query_cache=True,
            query_parameters=[
                bigquery.ArrayQueryParameter("projects", "STRING", selected_project ),
                bigquery.ScalarQueryParameter("lookback", "INT64", days_lookback),
            ]
        )
        return client.query(query=query, job_config=job_config).to_dataframe()


results = get_result(selected_project, days_lookback)

st.write(f"Query Result: Days[{days_lookback}], Projects{selected_project}")
st.dataframe(results, height=200)

st.subheader("Show results in charts")

st.write("streamlit line chart:")
st.line_chart(results, x='date', y='count', color='project')

st.write("streamlit_plotly_events line chart:")
color_map = {'streamlit':'red', 'dash':'blue', 'jupyter':'orange'}
fig1 = px.line(
    data_frame=results,
    x="date",
    y="count",
    symbol="project",
    color="project",
    color_discrete_map=color_map,
    markers=True
)
plotly_events(fig1, click_event=False)

st.write("streamlit_plotly_events area chart:")
fig2 = px.area(
    data_frame=results,
    x="date",
    y="count",
    symbol="project",
    color="project",
    color_discrete_map=color_map,
    markers=True
)
event2 = plotly_events(fig2, click_event=True)

st.subheader("Receive mark click event on area chart")

if(len(event2) == 0):
    st.stop()
else:
    st.write("Area chart event:")
    st.write(event2)


