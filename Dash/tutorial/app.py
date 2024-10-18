import base64
import glob
import os

import dash
import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Input, Output, ClientsideFunction, Patch, ctx, State
import plotly.express as px
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO, template_from_url
import plotly.io as pio
import dash_bootstrap_components as dbc
import dash_ag_grid as dag



load_figure_template(["minty",  "minty_dark", 'cyborg', 'cyborg_dark'])
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

def update_template(value):
    figure_1 = Patch()
    figure_2 = Patch()
    template = pio.templates["minty"] if value else pio.templates["minty_dark"]
    figure_1["layout"]["template"] = template
    figure_2["layout"]["template"] = template
    return [figure_1, figure_2]

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

def getData(question_id):

    df_data = pd.read_csv("../../chartsite/static/data/소비자물가지수(지출목적별)_20240803150211.csv")
    df_data.index = pd.date_range('2018-01-01', '2024-07-01',freq='ME' )

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

TOT_CNT = getData(5).shape[0]
PAGESIZE = 10



figure_bar = px.bar(
    getData(6).melt(id_vars=[ "시점"], ignore_index=False),
    x="variable",
    y="value",
    color="variable",
    title="서울 소비자 물가 지수",
    animation_frame="시점",
    range_y=[80, 125],
    height= 600,
    template='minty'
)

figure_line = make_figure(0, True)

imagePath = "/Volumes/WorkSpace/PythonProjects/Dash/tutorial/assets/*"
svg_list = [file for file in glob.glob(imagePath) if file.endswith(".svg")]

carousel = dbc.Carousel(
    id="carousel",
    items=[
        {'key': i, 'src':url, 'header':url} for i, url in enumerate(svg_list)
    ],
    controls=False,
    indicators=False,
    interval=2000,
    ride="carousel",
)



tab1_content = dbc.Card([
    dbc.CardBody([
        dcc.Graph(id='graph-1', figure=figure_bar)],
        className="dbc"
    ),],


)

tab2_content = dbc.Card([
    dbc.CardBody([
        dcc.Graph(id='graph-2', figure=figure_line),],
        className="dbc"
    ),],


)

columnDefs=[{"field": i} for i in getData(5).columns]
columnDefs.insert(0, {"headerName": "Row ID", "valueGetter": {"function": "params.node.id"}})

grid = dag.AgGrid(
    id='data_table',
    rowData=getData(5).to_dict('records'),
    columnDefs=columnDefs,
    defaultColDef={"filter": True},
    dashGridOptions={"animateRows": False, 'pagination':True},
    csvExportParams={
        "fileName": "서울소비자물가지수.csv",
    },
    style={"height": 600}

)
tab3_content = dbc.Card([
    dbc.CardBody([
        dbc.Button(
            "Download CSV",
            id="download-btn",
            n_clicks=0,
            outline=True,
            color="info",
            style={'margin-bottom':'20px'}
        ),
        grid
    ],
    className="dbc dbc-ag-grid")
],)


"""tab3_content = dbc.Card([
    dbc.CardBody([
            dash_table.DataTable(
                id='data_table',
                data=getData(5).to_dict('records'),
                page_current=0,
                page_size=PAGESIZE,
                style_table={'overflowX': 'scroll'},
            ),],
            className="dbc"
        ),
    dbc.CardFooter( [
        dbc.Pagination(
            id='pagination',
            max_value=TOT_CNT/PAGESIZE,
            active_page=1,
            first_last=True,
            previous_next=True,
            fully_expanded=False
        )] ,
        style={'margin':'auto', 'background-color':'rgba(0, 0, 0, 0)'}
    )
],outline=True, color="danger")
"""




tab4_content = dbc.Card([
    dbc.CardBody([
        carousel
         ],
        className="dbc"
    ),
],  style={'margin':'auto', 'background-color':'rgba(0, 0, 0, 0)'} )


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, dbc.icons.FONT_AWESOME])


color_mode_switch = ThemeSwitchAIO(
    aio_id="theme",
    icons={"left" :"fa fa-moon", "right" :"fa fa-sun"},
    themes=[dbc.themes.MINTY, dbc.themes.CYBORG],
)
"""
color_mode_switch = html.Span([
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)
"""

app.layout = html.Div([

        html.Div(
            [
                "서울 소비자 물가 지수"
             ],
            id='title_div',
            style={'padding':'10px'},
        ),

        color_mode_switch,

        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Animation Bar Chart", tab_id="tab-1"),
                dbc.Tab(tab2_content, label="Line Chart", tab_id="tab-2"),
                dbc.Tab(tab3_content, label="Data Sheet", tab_id="tab-3"),
             #   dbc.Tab(tab4_content, label='Carousel', tab_id="tab-4"),
            ],
            id="tabs",
            active_tab="tab-1",

        ),

        dcc.Interval(
            id='interval-component',
            interval=2*1000, # in milliseconds
            n_intervals=0
        )
    ],
    id='root_container',
    className='container'
)


"""
@app.callback(
    Output("data_table", "data"),
    Input('pagination', "active_page"),
)
def change_page(page_current):
    page = page_current - 1
    return getData(5).iloc[
           page*PAGESIZE:(page + 1)*PAGESIZE
           ].to_dict('records')
"""

@callback(
    Output("data_table", "exportDataAsCsv"),
    Input("download-btn", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False




@app.callback(
    output = [Output("graph-1", "figure"),
              Output("graph-2", "figure")],
    inputs={
        'input_dict':{
            'interval': Input('interval-component', 'n_intervals'),
          #  'switch_template': Input("color-mode-switch", "value"),
            'switch_template':Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        },
        'state_dict':{
            'current_tab': State('tabs', 'active_tab'),
           # 'current_mode': State("color-mode-switch", "value"),
            'current_mode': State(ThemeSwitchAIO.ids.switch("theme"), "value"),
        }
    },
    prevent_initial_call=True
)
def update_chart(input_dict, state_dict):
    inputs = ctx.args_grouping.input_dict
    states = ctx.args_grouping.state_dict

    no_update_result = [dash.no_update, dash.no_update]

    if inputs.switch_template.triggered:
        return update_template(inputs.switch_template.value)
    elif inputs.interval.triggered:
        if states.current_tab.value == 'tab-2':
            return[dash.no_update, make_figure(inputs.interval.value, states.current_mode.value)]
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
    #Input("color-mode-switch", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)




if __name__ == '__main__':
    app.run(port=7777, debug=False)