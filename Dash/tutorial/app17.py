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
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(
                    "A button", id="dropdown-button1", n_clicks=0
                ),
                dbc.DropdownMenuItem(
                    "Internal link", id="dropdown-button2", n_clicks=0
                ),
                dbc.DropdownMenuItem(
                    "External Link", id="dropdown-button3", n_clicks=0
                ),
                dbc.DropdownMenuItem(
                    "External relative", id="dropdown-button4", n_clicks=0
                ),
            ],
            label="Menu",
            id='dbc_dropdown',
        ),
        html.P(id="item-clicks", className="mt-3"),
    ]
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
    Output("dbc_dropdown", "label"),
    Input("dropdown-button1", "n_clicks"),
    Input("dropdown-button2", "n_clicks"),
    Input("dropdown-button3", "n_clicks"),
    Input("dropdown-button4", "n_clicks"),
    State("dropdown-button1", "children"),
    State("dropdown-button2", "children"),
    State("dropdown-button3", "children"),
    State("dropdown-button4", "children"),
)
def count_clicks(n1, n2, n3, n4, s1, s2, s3, s4):
    id = ctx.triggered_id
    if id == 'dropdown-button1':
        return s1, s1
    elif id == 'dropdown-button2':
        return s2, s2
    elif id == 'dropdown-button3':
        return s3, s3
    elif id == 'dropdown-button4':
        return s4, s4
    else:
        return "Select Item", "Select Item"


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
