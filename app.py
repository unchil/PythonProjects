# -*- coding: utf8 -*-
import matplotlib
import streamlit as st
from matplotlib import pyplot as plt
from plotly.figure_factory import np
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@st.cache_data
def load_data():
    df = sns.load_dataset("tips")
    return df

def main():

    st.title("Chart Test")

    tips= load_data()
    m_tips = tips.loc[tips['sex'] == 'Male']
    f_tips = tips.loc[tips['sex'] == 'Female']

    fig= make_subplots(rows=1,
                       cols=2,
                       subplot_titles=('Male','Female'),
                       shared_xaxes=True,
                       shared_yaxes=True,
                       x_title='Total Bill($)'
                       )
    fig.add_trace(go.Scatter(x=m_tips['total_bill'],y=m_tips['tip'],
                             mode='markers'),row=1,col=1)
    fig.add_trace(go.Scatter(x=f_tips['total_bill'],y=f_tips['tip'],
                             mode='markers'),row=1,col=2)

    fig.update_yaxes(title_text="Tip($)",row=1,col=1)
    fig.update_xaxes(range=[0,60])
    fig.update_layout(showlegend=False)

    fig.show()

    st.plotly_chart(fig, use_container_width=True)

    df = pd.DataFrame(np.random.randn(4,4))
    df.plot(kind='barh')

    st.dataframe(df)

    matplotlib.rc('font', family='AppleGothic')
    matplotlib.rcParams['axes.unicode_minus'] = False

    fig, axes_list = plt.subplots(3, 2, figsize=(8,5))

    axes_list[0][0].plot([1,2,3,4], 'ro-')
    axes_list[0][0].set_title('title')
    axes_list[0][0].grid(True)
    axes_list[0][0].set_xlabel('X 축')
    axes_list[0][0].set_ylabel('Y 축', labelpad=10, rotation= 0 )

    axes_list[0][1].plot(np.random.randn(4, 10), np.random.randn(4,10), 'bo--')

    axes_list[1][0].plot(np.linspace(0.0, 5.0), np.cos(2 * np.pi * np.linspace(0.0, 5.0)))

    axes_list[1][1].plot([3,5], [3,5], 'bo:')
    axes_list[1][1].plot([3,7], [5,4], 'kx')

    plt.subplots_adjust(hspace=0.7, wspace=0.5)
    plt.show()

    st.pyplot(fig)

if __name__ == "__main__":
    main()