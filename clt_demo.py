import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

binom_dist = np.random.binomial(1, .5, 1000)

list_of_means = []

for i in range(0, 1000):
    list_of_means.append(np.random.choice(binom_dist, 100, replace=True).mean())

fig, axes_list = plt.subplots(2, 2, figsize=(8,5))

#fig1, ax1 = plt.subplots()

axes_list[0][0].plot(list_of_means)
#st.pyplot(fig1)

#fig2, ax2 = plt.subplots()
#axes_list[0][1] = plt.hist(np.ones(4))
axes_list[0][1].plot(np.ones(4))

plt.show()
st.pyplot(fig)