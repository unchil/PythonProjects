import streamlit as st
import pandas as pd

st.title("Palmer's Penguins")
penguins_df = pd.read_csv("../Streamlit-for-Data-Science/penguin_app/penguins.csv")
st.write(penguins_df.head())
