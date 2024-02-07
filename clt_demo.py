import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

perc_heads = st.number_input(label = 'Change of Coins Landing on Heads',
                             min_value= 0.0, max_value=1.0, value=.5 )

binom_dist = np.random.binomial(1, .5, 1000)
list_of_means = []

for i in range(0, 1000):
    list_of_means.append(np.random.choice(binom_dist, 100, replace=True).mean())

fig, axes_list = plt.subplots()

axes_list = plt.hist(list_of_means, range=[0,1])


st.pyplot(fig)