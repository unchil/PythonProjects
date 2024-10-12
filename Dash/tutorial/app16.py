import dash
from dash import Dash, dcc, html, clientside_callback, Input, Output, Patch, ctx, ClientsideFunction, State
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio

load_figure_template(["minty",  "minty_dark", 'cyborg', 'cyborg_dark'])


color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)


df = px.data.gapminder()
dff = px.data.gapminder().query(f"year == {np.sort(df.year.unique())[::-1][0].item()}")
df_data = pd.read_csv("../../chartsite/static/data/소비자물가지수(지출목적별)_20240803150211.csv")
df_data.index = pd.date_range('2018-01-01', '2024-07-01',freq='ME' )

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

def update_template(value):
    figure_1 = Patch()
    figure_2 = Patch()
    figure_3 = Patch()
    template = pio.templates["minty"] if value else pio.templates["minty_dark"]
    figure_1["layout"]["template"] = template
    figure_2["layout"]["template"] = template
    figure_3["layout"]["template"] = template

    return [figure_1, figure_2, figure_3]

def make_figure(n, value):
    data = getData(n % 5)

    fig = px.line(
        data,
        x= data.index,
        y=data.columns,
        title="서울 소비자 물가 지수",
        height=600,
        template= 'minty' if value else 'minty_dark'
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
        annotation=dict(font_size=12),
        fillcolor="red",
        opacity=0.25,
        line_width=0
    )

    return fig



fig1 = px.sunburst(
    dff,
    path=["continent", "country"],
    values="pop",
    color="lifeExp",
    hover_data=["iso_alpha"],
    color_continuous_scale="RdBu",
    color_continuous_midpoint=np.average(df["lifeExp"], weights=df["pop"]),
    template='minty'
)
fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0))

fig2 = px.scatter(
    dff,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)


data =getData(0)

fig3 = make_figure(0, True)

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='graph-1', figure=fig1)
        ]
    ),
    className="mt-3",
)



tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='graph-2', figure=fig2)
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='graph-3', figure=fig3)
        ]
    ),
    className="mt-3",
)


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc_css, dbc.themes.BOOTSTRAP,  dbc.icons.FONT_AWESOME])

app.layout = html.Div([
    html.Div(
        ['Dash Tabs component demo'],
        id='title_div',
        style={'padding':'10px'},
    ),
    color_mode_switch,

    #dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
       # dcc.Tab(tab1_content, label='Tab One', value='tab-1-example-graph'),
       # dcc.Tab(tab2_content, label='Tab Two', value='tab-2-example-graph'),
       # dcc.Tab(tab3_content, label='Tab Three', value='tab-3-example-graph'),
    dbc.Tabs(id="tabs-example-graph", active_tab='tab-1-example-graph', children=[
        dbc.Tab(tab1_content, label='Tab One', tab_id='tab-1-example-graph'),
        dbc.Tab(tab2_content, label='Tab Two', tab_id='tab-2-example-graph'),
        dbc.Tab(tab3_content, label='Tab Three', tab_id='tab-3-example-graph'),
    ]),

    dcc.Interval(
        id='interval-component',
        interval=5*1000, # in milliseconds
        n_intervals=0
    )
],
    id='root_container',
    className='container',
   # className="dbc"
)


@app.callback(
    output = [Output("graph-1", "figure"),
        Output("graph-2", "figure"),
        Output("graph-3", "figure")],
    inputs={
        'input_dict':{
            'interval': Input('interval-component', 'n_intervals'),
            'switch_template': Input("color-mode-switch", "value"),
        },
        'state_dict':{
            'current_tab': State('tabs-example-graph', 'active_tab'),
            'current_mode': State("color-mode-switch", "value")
        }
    },
    prevent_initial_call=True
)
def update_chart(input_dict, state_dict):
    inputs = ctx.args_grouping.input_dict
    states = ctx.args_grouping.state_dict

    no_update_result = [dash.no_update, dash.no_update, dash.no_update]

    if inputs.switch_template.triggered:
        return update_template(inputs.switch_template.value)
    elif inputs.interval.triggered:
        if states.current_tab.value == 'tab-3-example-graph':
            return[dash.no_update, dash.no_update, make_figure(inputs.interval.value, states.current_mode.value)]
        else:
            return no_update_result
    else:
        return no_update_result




app.clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='change_template'
    ),
    Output("root_container", "id"),
    Input("color-mode-switch", "value"),
)


if __name__ == '__main__':
    app.run(port=8872, debug=True)

