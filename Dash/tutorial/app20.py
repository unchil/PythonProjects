import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
from dash import Dash, html, ClientsideFunction, Input, Output, dcc, Patch, ctx, State
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO

load_figure_template(["minty", "minty_dark", 'cyborg', 'cyborg_dark'])
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

data = px.data.stocks()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, dbc.icons.FONT_AWESOME], )

color_mode_switch = ThemeSwitchAIO(
    aio_id="theme",
    themes=[dbc.themes.MINTY, dbc.themes.CYBORG],
)

columnDefs = [{"field": i, "tooltipField": i, "headerTooltip": f"This is the {i} column"} for i in
              data.columns]
columnDefs.insert(0, {"headerName": "Row ID", "valueGetter": {"function": "params.node.id"}})

data_grid = dag.AgGrid(
    id='simple_grid_layout',
    rowData=data.to_dict('records'),
    columnDefs=columnDefs,
    defaultColDef={"filter": True},
    dashGridOptions={"animateRows": True,
                     'pagination': True,
                     "tooltipShowDelay": 0,
                     "tooltipHideDelay": 3000,
                     "tooltipInteraction": True,
                     },
    csvExportParams={"fileName": "stock.csv", },
    style={"height": 460, },
)


def make_figure(stocks, switch):
    figure = px.line(data_frame=data, x="date", y=stocks)
    figure.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        yaxis_title="Price",
        xaxis_title="Date",
        template='minty' if switch else 'minty_dark'
    )
    return figure


app.layout = dbc.Container([

    html.Div([

        color_mode_switch,

        html.Div(
            ["Equity prices - Line chart and Table data"],
            id='title_div',
            style={'textAlign': 'center'},
        ),

        dbc.Button(
            "Download Table Data",
            id="btn_csv",
            n_clicks=0,
            outline=True,
            color="info",
            size='sm'
        ),

        dcc.Dropdown(
            options=data.columns[1:],
            value=data.columns[1:3],
            placeholder='Select all stocks you like!',
            multi=True,
            id="stock-dropdown",

        ),

        html.Div([
            dcc.Graph(
                id="line_chart",
                figure=make_figure(data.columns[1:3], True),
                style={'flex-basis': '90%'}
            ),
            data_grid,
        ],
            className="dbc dbc-ag-grid",
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'justify-content': 'space-between',
            },
        ),

    ],

        style={
            'display': 'flex',
            'flexDirection': 'column',
            'margin': 10,
            'height': '700px',
            'justify-content': 'space-around',
        },
        className="dbc",
    ),

], id='root_container', )


@app.callback(
    Output("line_chart", "figure"),
    Input("stock-dropdown", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    State(ThemeSwitchAIO.ids.switch("theme"), "value"),
    prevent_initial_call=True
)
def select_stocks(stocks, value, switch):
    if ctx.triggered_id == 'stock-dropdown':
        return make_figure(stocks, switch)
    elif ctx.triggered_id == ThemeSwitchAIO.ids.switch("theme"):
        figure = Patch()
        template = pio.templates["minty"] if value else pio.templates["minty_dark"]
        figure["layout"]["template"] = template
        return figure
    else:
        return dash.no_update


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
    Output("root_container", "id"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

if __name__ == '__main__':
    app.run(port=7777, debug=False)
