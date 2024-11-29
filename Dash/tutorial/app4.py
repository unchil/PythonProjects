import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from dash import Dash, html, Input, Output, ctx, callback,clientside_callback, ClientsideFunction, dcc
import plotly.express as px
import pandas as pd
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = px.data.gapminder()

available_countries = df['country'].unique()

app.layout = html.Div([
    dcc.Graph(
        id='clientside-graph-px'
    ),
    dcc.Store(
        id='clientside-figure-store-px'
    ),
    'Indicator',
    dcc.Dropdown(
        {'pop' : 'Population', 'lifeExp': 'Life Expectancy', 'gdpPercap': 'GDP per Capita'},
        'pop',
        id='clientside-graph-indicator-px'
    ),
    'Country',
    dcc.Dropdown(available_countries, 'Canada', id='clientside-graph-country-px'),
    'Graph scale',
    dcc.RadioItems(
        ['linear', 'log'],
        'linear',
        id='clientside-graph-scale-px'
    ),
    html.Hr(),
    html.Details([
        html.Summary('Contents of figure storage'),
        dcc.Markdown(
            id='clientside-figure-json-px'
        )
    ])
])


@callback(
    Output('clientside-figure-store-px', 'data'),
    Input('clientside-graph-indicator-px', 'value'),
    Input('clientside-graph-country-px', 'value')
)
def update_store_data(indicator, country):
    dff = df[df['country'] == country]
    fig = px.scatter(dff, x='year', y=str(indicator))
    return fig


clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='create_chart'
    ),
    Output('clientside-graph-px', 'figure'),
    Input('clientside-figure-store-px', 'data'),
    Input('clientside-graph-scale-px', 'value')
)


@callback(
    Output('clientside-figure-json-px', 'children'),
    Input('clientside-figure-store-px', 'data')
)
def generated_px_figure_json(data):
    return '```\n'+json.dumps(data, indent=2)+'\n```'



if __name__ == '__main__':
    app.run(port=7788, debug=False)
