import streamlit as st
import time
import numpy as np

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

for i in range(1, 101):
	status_text.text("%i%% Complete" %i)
	progress_bar.progress(i)
	time.sleep(0.05)
progress_bar.empty()

st.button("Re-run")


