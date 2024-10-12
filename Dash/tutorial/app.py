import dash
import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Input, Output, ClientsideFunction, Patch, ctx
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio
import dash_bootstrap_components as dbc

load_figure_template(["minty",  "minty_dark", 'cyborg', 'cyborg_dark'])



color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

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

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[ dbc.themes.BOOTSTRAP, dbc_css, dbc.icons.FONT_AWESOME])

data1 = getData(6).melt(id_vars=[ "시점"], ignore_index=False)

figure_bar = px.bar(
    data1,
    x="variable",
    y="value",
    color="variable",
    title="서울 소비자 물가 지수",
    animation_frame="시점",
    range_y=[80, 125],
    height= 600,
    template='minty'
)

data2 = getData(0)
figure_line = px.line(
    data2,
    x= data2.index,
    y=data2.columns,
    title="서울 소비자 물가 지수",
    height=800,
    template='minty'
)

figure_line.update_layout(
    yaxis_range=[80,125],
    legend_yanchor="top",
    legend_y=0.99,
    legend_xanchor="left",
    legend_x=0.01,
)

figure_line.update_xaxes(
    dtick="M3",
    tickformat="%b\n%Y",
    ticklabelmode="period",
    rangeslider_visible=True
)

figure_line.add_vrect(
    x0='2020-08-31',
    x1='2020-12-31',
    annotation_text="통신비이만",
    annotation_position="top left",
    annotation=dict(font_size=12),
    fillcolor="red",
    opacity=0.25,
    line_width=0
)

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='graph-1', figure=figure_bar)
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='graph-2', figure=figure_line),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dash_table.DataTable(data=getData(5).to_dict('records'), page_size=15 ),
        ],
        className="dbc"
    ),
    className="mt-3",
)

app.layout = html.Div(
    [
        html.Div(
            ["소비자 물가 지수"],
            id='title_div',
            style={'padding':'10px'},
        ),
        color_mode_switch,

        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Animation Bar Chart", tab_id="tab-1"),
                dbc.Tab(tab2_content, label="Line Chart", tab_id="tab-2"),
                dbc.Tab(tab3_content, label="Data Sheet", tab_id="tab-3"),
            ],
            id="tabs",
            active_tab="tab-1"
        ),

    ],
    id='root_container',
    className='container'
)





@app.callback(
    Output("graph-1", "figure"),
    Output("graph-2", "figure"),
    Input("color-mode-switch", "value"),
)
def update_chart_template(value):

    figure_bar = Patch()
    figure_line = Patch()
    template = pio.templates["minty"] if value else pio.templates["minty_dark"]
    figure_bar["layout"]["template"] = template
    figure_line["layout"]["template"] = template
    return figure_bar, figure_line


app.clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='change_template'
    ),
    Output("root_container", "id"),
    Input("color-mode-switch", "value"),
)


if __name__ == '__main__':
    app.run(port=7777, debug=False)