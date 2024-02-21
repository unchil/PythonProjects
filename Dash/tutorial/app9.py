
from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback, ClientsideFunction
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template(["minty",  "minty_dark", 'cyborg', 'cyborg_dark'])

app = Dash(
    __name__,
   prevent_initial_callbacks=True,
   external_stylesheets=[dbc.themes.MINTY, dbc.themes.CYBORG ,dbc.icons.FONT_AWESOME]
)

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)



df = px.data.gapminder()
df = df.drop(columns=['iso_alpha','iso_num'])

fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    log_x=True,
    size_max=60,
    template="minty",
)



app.layout = dbc.Container(
    [
        html.Div(
            [
             "Bootstrap Light Dark Color Modes Demo"
            ],
            id='title_div',
            style={'padding':'20px'},
        ),
        color_mode_switch,
        dcc.Graph(id="graph", figure= fig, className="border"),

    ],
    id='root_container',
    className='container'

)



@app.callback(
    Output("graph", "figure"),
    Input("color-mode-switch", "value")
)
def update_figure_template(switch_on):
    # When using Patch() to update the figure template, you must use the figure template dict
    # from plotly.io  and not just the template name
    template = pio.templates["cyborg"] if switch_on else pio.templates["cyborg_dark"]

    patched_figure = Patch()
    patched_figure["layout"]["template"] = template
    return patched_figure




"""
@app.callback(
    Output("root_container", "style"),
    Input("color-mode-switch", "value"),
)
def change_template(switch_on):
    style = {'background-color':'white'} if switch_on else {'background-color': 'rgb(25, 25, 25)' }
    return style
"""

clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='change_template'
    ),
    Output("root_container", "id"),
    Input("color-mode-switch", "value"),
)

if __name__ == "__main__":
    app.run_server(port=7777, debug=True)