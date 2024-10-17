from dash import Dash, dcc, html, dash_table, callback, Input, Output, ClientsideFunction, Patch, ctx, State, ALL, MATCH
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio


load_figure_template(["minty",  "minty_dark", 'cyborg', 'cyborg_dark'])

color_mode_switch = html.Span([
    dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
    dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
    dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
])

dropdown = html.Div(
    [
        dcc.Dropdown(
            options=["A button", "Internal link", "External Link", "External relative"],
            value="A button",
            id='dcc_dropdown',
        ),
        html.P(id="item-clicks", className="mt-3"),
    ],
    className="dbc",
)



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,  dbc.icons.FONT_AWESOME])


app.layout =  dbc.Container(
    [
        html.Div(
            ["DBC DropDown"],
            id='title_div',
            style={'padding':'20px'},
        ),
        color_mode_switch,
        dropdown,
    ],
    id='root_container',
    className='container'
)

@app.callback(
    Output("item-clicks", "children"),
    Input("dcc_dropdown", "value"),
)
def count_clicks(value):
    return value


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
