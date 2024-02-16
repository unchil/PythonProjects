import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_penguin = load_lottieurl(
    "https://assets9.lottiefiles.com/private_files/lf30_lntyk83o.json"
)
st_lottie(lottie_penguin, height=200)

st.title("Streamlit Plotly Events + Lottie Example: Penguins")


df = pd.read_csv("./COMPONENTS_EXAMPLE/penguins.csv")
df.dropna(inplace=True)

color_map = {'Adelie':'red', 'Gentoo':'blue', 'Chinstrap':'orange'}

fig = px.scatter(
    df, x='bill_length_mm', y='bill_depth_mm',
    color='species',
    color_discrete_map=color_map,
    width=1000,
    symbol='species',
)

selected_point = plotly_events(fig, click_event=True)

st.write("Selected point:")

if len(selected_point) == 0:
    st.stop()
else:
    df_selected = pd.DataFrame()
    for data in selected_point:
        selected_data = df.loc[
            (df['bill_length_mm'] == data["x"]) & (df['bill_depth_mm'] == data["y"])
        ]
        df_selected = pd.concat([df_selected, selected_data])
    st.dataframe(df_selected)







