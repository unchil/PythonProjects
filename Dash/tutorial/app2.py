import ssl

import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objs as go

import datetime
from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df_setellite = pd.DataFrame( columns=['time','Latitude', 'Longitude','Altitude'])


app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-collection',
            interval=20*1000,
            n_intervals=0
        ),

        dcc.Interval(
            id='interval-component',
            interval=60*1000,
            n_intervals=0
        )
    ])
)



@callback(Output('live-update-text', 'children'),
          Input('interval-collection', 'n_intervals'))
def update_metrics(n):

    global df_setellite
    time = datetime.datetime.now()
    lon, lat, alt = satellite.get_lonlatalt( time )
    df_new = pd.DataFrame([[time, lat, lon, alt]], columns=['time','Latitude', 'Longitude','Altitude']  )
    df_setellite = pd.concat([df_setellite, df_new], ignore_index=True)

    style = {'padding': '5px', 'fontSize': '16px'}

    return [
        html.Div( time, style=style),


        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]



@callback(Output('live-update-graph', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_graph_live(n):


    projection_list = ['equirectangular', 'mercator', 'orthographic', 'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area', 'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel']

    fig = px.scatter_geo(
        data_frame=df_setellite,
        lon='Longitude',
        lat='Latitude',
        hover_name='time',
        #projection= 'natural earth',
        projection=projection_list[2],
        title='TERRA Satellite Track',
     #   animation_frame='time',
        height=600
    )



    return fig

if __name__ == '__main__':
    app.run(port=7777, debug=False)