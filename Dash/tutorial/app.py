import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import psutil

import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Input, Output
import plotly.express as px

df_data = pd.read_csv("../../chartsite/static/data/소비자물가지수(지출목적별)_20240803150211.csv")
df_data.index = pd.date_range('2018-01-01', '2024-07-01',freq='ME' )

cpu_data = []

def getData(question_id):
    match question_id:
        case 0:
            return df_data.drop(columns='시점')
        case 1:
            return df_data[['통신', '음식 및 숙박']]
        case 2:
            return df_data[['통신', '식료품 및 비주류음료']]
        case 3:
            return df_data[['통신', '기타 상품 및 서비스']]
        case 4:
            return df_data[['통신', '음식 및 숙박', '식료품 및 비주류음료', '기타 상품 및 서비스']]
        case 5:
            return df_data
        case 6:
            return df_data[['시점', '통신', '음식 및 숙박', '식료품 및 비주류음료', '기타 상품 및 서비스']]
        case _:
            return df_data

def realtimeData(question_id, n):
    size = 12

    match question_id:
        case 0:
            return df_data.drop(columns='시점')[n:size+n]
        case 1:
            return df_data[['통신', '음식 및 숙박']][n:size+n]
        case 2:
            return df_data[['통신', '식료품 및 비주류음료']][n:size+n]
        case 3:
            return df_data[['통신', '기타 상품 및 서비스']][n:size+n]
        case 4:
            return df_data[['통신', '음식 및 숙박', '식료품 및 비주류음료', '기타 상품 및 서비스']][n:size+n]
        case 5:
            return df_data[n:size+n]
        case _:
            return df_data[n:size+n]

app = Dash()

data = getData(6).melt(id_vars=[ "시점"], ignore_index=False)

figure_bar = px.bar(
    data,
    x="variable",
    y="value",
    color="variable",
    title="서울 소비자 물가 지수",
    animation_frame="시점",
    range_y=[80, 125],
    height= 600
)



app.layout = [
    html.H1(
        className='app-header',
        children=[
            html.Div('소비자 물가 지수', className="app-header--title")
        ]
    ),
    #dcc.Graph( id='cpu-graph',figure={} ),
   # dcc.Graph( id='realtime-graph', figure={}),
    dcc.Loading(dcc.Graph(id='animation_bar', figure=figure_bar), type='cube'),
    dcc.Graph(id='live-update-graph',figure={} ),
    html.Div(
        className='data-table',
        children=dash_table.DataTable(data=getData(5).to_dict('records'), page_size=10, ),
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
]



@callback(
    Output('cpu-graph', 'figure'),
    Input('interval-component', 'n_intervals'))
def realtime_graph(n):

    if len(cpu_data) == 60:
        cpu_data.pop(0)
        cpu_data.append(psutil.cpu_percent())
    else:
        cpu_data.append(psutil.cpu_percent())

    fig = px.line(
        cpu_data,
        title="cpu",
        width=600,
        height=300
    )

    fig.update_layout(
        yaxis_range=[0,100],
    )

    return fig



@callback(
    Output('realtime-graph', 'figure'),
    Input('interval-component', 'n_intervals'))
def realtime_graph(n):

    data = realtimeData(0, n)

    fig = px.line(
        data,
        x= data.index,
        y=data.columns,
        title="서울 소비자 물가 지수",
        width=1000,
        height=600
    )

    fig.update_layout(
        yaxis_range=[80,125],
    )

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period",
        rangeslider_visible=False
    )

    return fig



@callback(
    Output('live-update-graph', 'figure'),
    Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    data = getData(n % 5)

    fig = px.line(
        data,
        x= data.index,
        y=data.columns,
        title="서울 소비자 물가 지수",
        height=800
    )



    fig.update_layout(
        yaxis_range=[80,125],
        legend_yanchor="top",
        legend_y=0.99,
        legend_xanchor="left",
        legend_x=0.01,
    )

    fig.update_xaxes(
        dtick="M3",
        tickformat="%b\n%Y",
        ticklabelmode="period",
        rangeslider_visible=True
    )

    fig.add_vrect(
        x0='2020-08-31',
        x1='2020-12-31',
        annotation_text="통신비이만",
        annotation_position="top left",
        annotation=dict(font_size=12, font_family="Times New Roman"),
        fillcolor="red",
        opacity=0.25,
        line_width=0
    )

    return fig

if __name__ == '__main__':
    app.run(port=7777, debug=False)