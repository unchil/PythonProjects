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
    icons={"left":"fa fa-moon", "right":"fa fa-sun"},
    themes=[dbc.themes.MINTY, dbc.themes.CYBORG],
)

def make_country_figure(df, country):
    filter_df = df[df["country"] == country]
    fig = px.line(
        filter_df,
        x="year",
        y="lifeExp",
        title=country,
        width=500,
        height=300,
        template='minty_dark'
    )

    return fig


df = px.data.gapminder().query('continent == "Asia"')
df2 = df.groupby("country")[["lifeExp", "gdpPercap", "pop"]].mean().reset_index()
df2["graph"] = df2["country"].apply(lambda country: make_country_figure(df, country))


columnDefs = [
    {"field": "country",},
    {"field": "gdpPercap",
     "type": "rightAligned",
     "valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
     },
    {"field": "pop",
     'headerName':'Population',
     "type": "rightAligned",
     "valueFormatter": {"function": 'd3.format("(,.0f")(params.value)'},
     },
    {
        "field": "lifeExp",
        "headerName": "Avg. Life Expectancy (1952-2007)",
        "type": "rightAligned",
        "valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
        "tooltipField": "graph",
        "tooltipComponent": "CustomTooltipGraph",
    },
]

grid = dag.AgGrid(
    rowData=df2.to_dict("records"),
    columnSize="autoSize",
    columnDefs=columnDefs,
    dashGridOptions={
        "tooltipShowDelay": 0,
        "tooltipInteraction": True,
        "popupParent": {"function": "setBody()"}
    },


)


app.layout = (
    dbc.Container(
        html.Div([
                html.Div(
                    ["Gap Minder"],
                    id='title_div',
                    style={'padding':'10px'},
                ),
                color_mode_switch,
                grid,
            ],
            className="dbc dbc-ag-grid",
        ),
        id='root_container',
    )
)




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

