import dash
from dash import Dash, dcc, html, callback, Input, Output, ClientsideFunction, Patch, ctx, State, set_props
import pandas as pd
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO, ThemeChangerAIO,template_from_url
import plotly.graph_objects as go
import numpy as np
from dash.exceptions import PreventUpdate


load_figure_template(["minty",  "minty_dark", 'cyborg', 'cyborg_dark'])
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

url = 'http://127.0.0.1:8000/SD/one_hr/'
title = '현재 전력 수급 현황'
columns = ['기준일시', '공급능력', '현재수요', '예측수요', '공급예비력', '공급예비율', '운영예비력', '운영예비율']

df = pd.read_json(url)
df.columns = columns

option_presentation_data_range = ['Current1Hr', 'Current2Hr', 'Current1Day', 'Last1DayBefore']


def change_data(api_url, current_mode):
    data = pd.read_json(api_url)
    data.columns = columns
    set_props("simple_grid_layout", {'rowData': data[::-1].to_dict('records')})
    return [make_figure(data, current_mode), make_figure_rate(data, current_mode),  make_figure_paper(data, current_mode)]

def refresh_data(data_range, current_mode):
    match data_range:
        case 'Current1Hr':
            return change_data('http://127.0.0.1:8000/SD/one_hr/', current_mode)
        case 'Current2Hr':
            return change_data('http://127.0.0.1:8000/SD/two_hr/', current_mode)
        case 'Current1Day':
            return change_data('http://127.0.0.1:8000/SD/current_one_day/', current_mode)
        case 'Last1DayBefore':
            return change_data('http://127.0.0.1:8000/SD/one_day/', current_mode)
        case _:
            return change_data('http://127.0.0.1:8000/SD/one_hr/', current_mode)


def make_figure_paper(df_data, value):
    df_data2 = df_data[['공급예비율', '운영예비율']]
    df_data2.index = pd.to_datetime(df_data.기준일시, format='%Y%m%d%H%M%S')
    ydata = np.array([df_data['공급예비율'], df_data['운영예비율']])
    labels = df_data2.columns
    colors = ['rgb(189,189,189)', 'rgb(49,130,189)']
    mode_size = [round(df_data2.iloc[-1]['공급예비율'] / 10 )*2 , round(df_data2.iloc[-1]['운영예비율'] / 10 )*2 ]
    line_size = [round(df_data2.iloc[-1]['공급예비율'] / 10 ) , round(df_data2.iloc[-1]['운영예비율'] / 10 ) ]

    fig = go.Figure()

    for i in range(0, 2):
        fig.add_trace(
            go.Scatter(
                x=df_data2.index,
                y=df_data2[df_data2.columns[i]],
                mode='lines',
                name=labels[i],
                line=dict(color=colors[i], width=line_size[i]),
                connectgaps=True,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[ df_data2.index[0], df_data2.index[-1] ],
                y=[ df_data2.iloc[0][df_data2.columns[i]], df_data2.iloc[-1][df_data2.columns[i]] ],
                mode='markers',
                name=labels[i],
                marker=dict(color=colors[i], size=mode_size[i])
            )
        )

    annotations = []

    for y_trace, label, color in zip(ydata, labels, colors):

        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                xanchor='right', yanchor='middle',
                                text=label + ' {}%'.format(round(y_trace[0],2)),
                                font=dict(family='Arial', size=16),
                                showarrow=False))

        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[-1],
                                xanchor='left', yanchor='middle',
                                text='{}%'.format(round(y_trace[-1],2)),
                                font=dict(family='Arial', size=16),
                                showarrow=False))



    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.2,
                            xanchor='left', yanchor='bottom',
                            text='현재 전력 수급 예비율',
                            font=dict(family='Arial',size=22, color='rgb(150,150,150)'),
                            showarrow=False))

    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.2,
                            xanchor='center', yanchor='top',
                            text='Source: 공공데이터포털 [https://www.data.go.kr]',
                            font=dict(family='Arial',size=12, color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(
        template='minty' if value else 'minty_dark',
        annotations=annotations,
        autosize=True,
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),

        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        showlegend=False,
        margin=dict(
            autoexpand=False,
            l=120,
            r=60,
            t=100,
        ),
    )
    return fig


def update_template(value):
    figure = Patch()
    template = pio.templates["minty"] if value else pio.templates["minty_dark"]
    figure["layout"]["template"] = template
    return [figure, figure, figure]


def make_figure(df_data, value):
    data = df_data[['공급능력', '현재수요', '공급예비력', '운영예비력']]
    data.index = pd.to_datetime(df_data.기준일시, format='%Y%m%d%H%M%S')
    fig = px.line(
        data,
        x=data.index,
        y=data.columns,
        markers=False,
    )
    fig.update_layout(
        title="현재 전력 수급 현황",
        xaxis_title='수집시간',
        yaxis_title='전력량(MW)',
        yaxis_range=[0, 120000],
       # legend=dict(title='항목', y=0.99, x=0.99, yanchor='top', xanchor='right'),
        legend=dict(title='항목'),
        template='minty' if value else 'minty_dark'
    )
    return fig


def make_figure_rate(df_data, value):
    data = df_data[['공급예비율', '운영예비율']]
    data.index = pd.to_datetime(df_data.기준일시, format='%Y%m%d%H%M%S')
    fig = px.line(
        data,
        x=data.index,
        y=data.columns,
        markers=False,
    )
    fig.update_layout(
        title="현재 전력 수급 예비율",
        xaxis_title='수집시간',
        yaxis_title='예비율(%)',
        yaxis_range=[0, 100],
        #legend=dict(title='항목', y=0.99, x=0.99, yanchor='top', xanchor='right'),
        legend=dict(title='항목'),
        template='minty' if value else 'minty_dark'
    )
    return fig


def make_grid(df_data):
    columnDefs = [{"field": i, "tooltipField": i, "headerTooltip": f"This is the {i} column"} for i in df_data.columns]
    columnDefs.insert(0, {"headerName": "Row ID", "valueGetter": {"function": "params.node.id"}})

    data_grid = dag.AgGrid(
        id='simple_grid_layout',
        rowData=df_data[::-1].to_dict('records'),
        columnDefs=columnDefs,
        defaultColDef={"filter": True},
        dashGridOptions={"animateRows": True,
                         'pagination': True,
                         "tooltipShowDelay": 0,
                         "tooltipHideDelay": 3000,
                         "tooltipInteraction": True,
                         },
        csvExportParams={"fileName": "powerSD.csv", },
        style={"height": 460, },
    )
    return data_grid


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, dbc.icons.FONT_AWESOME])

color_mode_switch = ThemeSwitchAIO(
    aio_id="theme",
    themes=[dbc.themes.MINTY, dbc.themes.CYBORG],
)

app.layout = dbc.Container([
        html.Div([
                color_mode_switch,
                html.H3(title, style={'textAlign': 'center'}),

                html.Div([

                    dcc.Dropdown(
                        id="data_range",
                        options=option_presentation_data_range,
                        value=option_presentation_data_range[0],
                        clearable=False,
                        style={'flex-basis': '20%'}
                    ),
                ],
                    style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'vertical-align': 'baseline',
                        'justify-content': 'center',
                    },
                    className='dropdown'
                ),

                html.Div([
                    dcc.Graph( id='paper_fig', figure=make_figure_paper(df, True), style={'flex-basis': '70%'}),
                ],
                    style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'justify-content': 'center',
                     #   'flex-basis': '25%'
                    },
                ),



                dcc.Graph(
                    id="chart_supplyDemand",
                    figure=make_figure(df, True),
                  #  style={'flex-basis': '50%'}
                ),

                dcc.Graph(
                    id="chart_reserveRate",
                    figure=make_figure_rate(df, True),
               #     style={'flex-basis': '48%'}
                ),








                html.Div([
                        dbc.Button(
                            "Download Table Data",
                            id="btn_csv",
                            n_clicks=0,
                            outline=True,
                            color="info",
                            size='sm'
                        ),
                        make_grid(df),
                    ],
                    className="dbc dbc-ag-grid",
                ),

            ],
            style={
                'display': 'flex',
                'flexDirection': 'column',
                'height': '2400px',
                'justify-content': 'space-around',
            },
            className="dbc",
        ),
        dcc.Interval(
            id='interval-component',
            interval=60*1000,  # in milliseconds
            n_intervals=0
        ),
    ],
    id='container'
)


@app.callback(
    output=[
        Output("chart_supplyDemand", "figure"),
        Output("chart_reserveRate", "figure"),
        Output("paper_fig", "figure"),
    ],
    inputs={
        'input_dict': {
            'switch_template': Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
            'interval': Input('interval-component', 'n_intervals'),
            'change_data_range':  Input('data_range', 'value'),
        },
        'state_dict': {
            'current_mode': State(ThemeSwitchAIO.ids.switch("theme"), "value"),
            'current_range': State('data_range', 'value')
        }
    },
  #  prevent_initial_call=True
)
def refresh(input_dict, state_dict):
    inputs = ctx.args_grouping.input_dict
    states = ctx.args_grouping.state_dict

    if inputs.switch_template.triggered:
        return update_template(inputs.switch_template.value)
    elif inputs.interval.triggered:
        return refresh_data(states.current_range.value, states.current_mode.value)
    elif inputs.change_data_range:
        return refresh_data(inputs.change_data_range.value, states.current_mode.value)
    else:
        raise PreventUpdate


@app.callback(
    Output("simple_grid_layout", "exportDataAsCsv"),
    Input("btn_csv", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False


app.clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='change_template'
    ),
    Output("container", "id"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

if __name__ == '__main__':
    app.run(port=7777, debug=False)
