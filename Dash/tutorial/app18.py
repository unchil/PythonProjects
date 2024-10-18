import json

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


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, dbc.icons.FONT_AWESOME])

color_mode_switch = ThemeSwitchAIO(
    aio_id="theme",
    icons={"left" :"fa fa-moon", "right" :"fa fa-sun"},
    themes=[dbc.themes.MINTY, dbc.themes.CYBORG],
)


df = px.data.gapminder().query('continent == "Asia"')
df2 = df.groupby("country")[["lifeExp", "gdpPercap", "pop"]].mean().reset_index()
df2["graph"] = ""

for i, r in df2.iterrows():
    filterDf = df[df["country"] == r["country"]]
    fig = px.scatter(
        filterDf,
        x="year",
        y="gdpPercap",
        size="pop",
        color="lifeExp",
        color_continuous_scale=px.colors.diverging.Tealrose_r,
        trendline="ols",
        range_color=[30, 90],

    )
    fig.update_layout(

        #showlegend=False,
        #yaxis_visible=False,
        #yaxis_showticklabels=False,
        #xaxis_visible=False,
        #xaxis_showticklabels=False,
        margin=dict(l=0, r=0, t=0, b=0),
        template="cyborg"
    )
    df2.at[i, "graph"] = fig

columnDefs = [
    {"field": "country"},
    {
        "field": "lifeExp",
        "headerName": "Avg. Life Expectancy",
        "valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
    },
    {
        "field": "gdpPercap",
        "headerName": "Avg. GPD per Capita",
        "valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
    },
    {
        "field": "pop",
        "headerName": "Avg. Population",
        "valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
    },
    {
        "field": "graph",
        "cellRenderer": "DCC_GraphClickData",
        "headerName": "GdpPerCap / Year",
        "maxWidth": 900,
        "minWidth": 500,
    }
]

data_grid = dag.AgGrid(
    id="custom-component-graph-grid",
    rowData=df2.to_dict("records"),
    columnSize="sizeToFit",
    columnDefs=columnDefs,
    defaultColDef={"filter": True, "minWidth": 125},
    dashGridOptions={"rowHeight": 200, "animateRows": False},
    style={"height": 800},
)


app.layout = html.Div([

        html.Div(
            [
                "Gap Minder"
            ],
            id='title_div',
            style={'padding':'10px'},
        ),

        color_mode_switch,

        data_grid,

    ],
    className="dbc dbc-ag-grid",
    id='root_container',

)


@callback(
    Output("custom-component-graph-output", "children"),
    Input("custom-component-graph-grid", "cellRendererData")
)
def graphClickData(d):
    return json.dumps(d)



app.clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='change_template'
    ),
    Output("root_container", "id"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)




if __name__ == '__main__':
    app.run(port=7777, debug=False)

