import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns

penguins_df = pd.read_csv("../Streamlit-for-Data-Science/penguin_app/penguins.csv")

st.markdown('Use this Streamlit app to make your own scatterplot about penguins!')
selected_species = st.selectbox('What species would you likt to visualize?' , pd.unique(penguins_df['species']))
selected_x_var = st.selectbox('What do you want the x variable to be?',
                              ['pill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])
selected_y_var = st.selectbox('What do you want the y variable to be?',
                               ['pill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])


st.title("Palmer's Penguins")

st.write(penguins_df.head())
