# -*- coding: utf8 -*-

import streamlit as st
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@st.cache_data
def load_data():
    df = sns.load_dataset("tips")
    return df


st.title("streamlit with plotly")

tips= load_data()

    #데이터 가공
m_tips = tips.loc[tips['sex'] == 'Male']
f_tips = tips.loc[tips['sex'] == 'Female']

#시각화 차트
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



st.plotly_chart(fig, use_container_width=True)




