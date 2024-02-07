import streamlit as st
import numpy as np

binom_dist = np.random.binomial(1, .5, 100)
st.write(np.mean(binom_dist))
