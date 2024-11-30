import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

st.set_page_config(layout="wide")
st.title("Streamlit AgGrid Example: Penguins")

penguins_df = pd.read_csv("./COMPONENTS_EXAMPLE/trees.csv")
response = AgGrid(penguins_df, height=500, editable=True)

df_edited = response["data"]

st.write("Edited DataFrame:")
st.dataframe(df_edited)
