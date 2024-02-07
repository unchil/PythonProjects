import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

binom_dist = np.random.binomial(1, .5, 1000)

list_of_means = []

for i in range(0, 1000):
    list_of_means.append(np.random.choice(binom_dist, 100, replace=True).mean())

fig1, ax1 = plt.subplots()
ax1 = plt.hist(list_of_means)
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2 = plt.hist(np.ones(4))
st.pyplot(fig2)