import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns

st.markdown('Use this Streamlit app to make your own scatterplot about penguins!')
#selected_species = st.selectbox('What species would you likt to visualize?' , pd.unique(penguins_df['species']))
selected_x_var = st.selectbox('What do you want the x variable to be?',
                              ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])
selected_y_var = st.selectbox('What do you want the y variable to be?',
                              ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])

selected_gender = st.selectbox('What gender do you want to filter for?',
                               ['all penguins', 'male penguins', 'female penguins'])

st.title("Palmer's Penguins")


penguins_df = pd.read_csv("../Streamlit-for-Data-Science/penguin_app/penguins.csv")
penguin_file = st.file_uploader("Select Your Local Penguins CSV(default provided)")
if penguin_file is not None:
    penguins_df = pd.read_csv(penguin_file)

if selected_gender == 'male penguins':
    penguins_df = penguins_df[penguins_df['sex'] == 'male']
elif selected_gender == 'female penguins':
    penguins_df = penguins_df[penguins_df['sex'] == 'female']
else:
    pass

alt_chart = (
    alt.Chart(penguins_df)
    .mark_circle()
    .encode(
        x=selected_x_var,
        y= selected_y_var,
        color="species"
    )
    .interactive()
)

st.altair_chart(alt_chart, use_container_width=True)

st.write(penguins_df.head())
