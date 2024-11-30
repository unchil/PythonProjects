import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker

result = date_range_picker("Select a date range")
st.write("Result:", result)

from streamlit_extras.stoggle import stoggle

stoggle(
    "Click me!",
    """ Surprise! Here's some additional content""",
)