import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.title("SF Trees Map")

@st.cache_data
def load_data():
    return pd.read_csv("./COMPONENTS_EXAMPLE/trees.csv")

trees_df = load_data()
trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df = trees_df.head(n=100)
lat_avg = trees_df["latitude"].mean()
lon_avg = trees_df["longitude"].mean()


map = folium.Map(
    location=[lat_avg, lon_avg],
    zoom_start=12
)

for _, row in trees_df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
    ).add_to(map)

event = st_folium(map)

if event["last_object_clicked"] != None:
    lat = round(event["last_object_clicked"]["lat"], 5)
    lon = round(event["last_object_clicked"]["lng"], 5)

    selected_data = trees_df.loc[
        (round(trees_df['latitude'], 5) == lat) & (round(trees_df['longitude'],5) == lon)
        ]
    st.dataframe(selected_data)


