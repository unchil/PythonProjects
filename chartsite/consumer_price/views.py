from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
import matplotlib
from django.template.defaultfilters import safe

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from plotly.offline import plot
import plotly.express as px
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import numpy as np


pd.options.plotting.backend = "plotly"



# Create your views here.



"""
        const response = await fetch(url, {method:'GET',} );
        const data = await response.json();
        console.log("성공:", data.plot_div);
"""

def getData(question_id):
    data = pd.read_csv("static/data/소비자물가지수(지출목적별)_20240803150211.csv")
    data.index = pd.date_range(start='2018-01-01', end='2024-07-01', freq='ME')
    match question_id:
        case 1:
            return data[['음식 및 숙박','통신']]
        case 2:
            return data[['식료품 및 비주류음료','통신']]
        case 3:
            return data[['기타 상품 및 서비스','통신']]
        case 4:
            return data[['음식 및 숙박', '식료품 및 비주류음료', '기타 상품 및 서비스','통신']]
        case 5:
            return data.drop(columns='시점')
        case 6:
            return data
        case _:
            return data.drop(columns='시점')



def plotly_express(request):

    data = getData(5)
    fig = data.plot(width=1024, height=600)

    fig.update_layout(
        legend_yanchor="top",
        legend_y=0.99,
        legend_xanchor="left",
        legend_x=0.01,
        legend_bgcolor="lightgray",

    )
    fig.update_yaxes(range=[80, 130], showgrid=True, minor_showgrid=False)
    fig.update_xaxes(range=["2017-11-01", "2024-09-01"])


    plot_div = plot(fig, output_type="div")
    context = {"plot_div": plot_div}

    return render(request, "consumer_price/express.html", context)



@api_view(['GET'])
def get_chart(request, question_id):

    data = getData(question_id)

    fig = data.plot(width=1024, height=600)

    fig.update_layout(
        legend_yanchor="top",
        legend_y=0.99,
        legend_xanchor="left",
        legend_x=0.01
    )

    fig.update_yaxes(range=[80, 130], showgrid=True, minor_showgrid=False)
    fig.update_xaxes(range=["2017-11-01", "2024-09-01"])
    fig.add_vrect(
        x0="2020-09-01",
        x1="2021-01-01",
        annotation_text="통신 비이만원 지원",
        annotation_position="top left",
        annotation=dict(font_size=12, font_family="Times New Roman"),
        fillcolor="red", opacity=0.25, line_width=0
    )

    plot_div = plot(fig, output_type="div")
    context = {"plot_div": plot_div}

    return Response(context)



def index(request):

    data = getData(5)

    fig, ax = plt.subplots( figsize=(12,6))
    ax.plot(data)
    ax.legend(data.columns)
    ax.set_title("서울시 소비자 물가 지수")
    plt.savefig('static/image/consumer_price.png')
    return render(request, "consumer_price/index.html", {"data": data.to_html(), "image":"../../static/image/consumer_price.png"})




def mat_video(request):
    from matplotlib.animation import FuncAnimation

    data = getData(6)

    fig, ax = plt.subplots(figsize=(12,6))

    x = data['시점']
    def update(frame):
        """
        - frames에 따라서 매번 업데이트로 그림을 그려줌.
        - frame은 FuncAnimation의 frame argument에 있는 값이 넘어가는 부분.
        """
        ax.clear() # 일단 지금 그려진 부분을 다 지우고,
        ax.set_title("서울시 소비자 물가 지수")
     #   ax.set_xticklabels(x)

        ax.set_xlim(0,77)
        ax.set_ylim(80,130)

        plt.xticks(fontsize=8, rotation=90)
      #  ax.grid(True)


        # 여기서처럼 그림을 새로 그려주면 됨.


        plt.plot(x[:frame], data[ ['음식 및 숙박', '식료품 및 비주류음료', '기타 상품 및 서비스','통신']][:frame])

    """
    - 아래 argument에서 blit가 False인 것이 중요합니다. 
    - True일 경우에는 update function에서 artist object를 넘겨줘야 합니다. 예를 들면 Line 같은 것들. 
    """


    ani = FuncAnimation(
        fig=fig,
        func=update,
        frames=77,
        interval=100,
        blit=False,
    )

    return render(request, "consumer_price/mat_video.html", {"data": ani.to_jshtml()})




"""
# Bulk Insert 

df=pd.read_csv('test_csv.txt',sep=';')

row_iter = df.iterrows()

objs = [
    Entry(
        field_1 = row['Name'],
        field_2  = row['Description'],
        field_3  = row['Notes'],
        field_4  = row['Votes']
    ) for index, row in row_iter
]

from itertools import islice

batch_size = 100

while True:
    batch = list(islice(objs, batch_size))
    if not batch:
        break
    Entry.objects.bulk_create(batch, batch_size)

"""