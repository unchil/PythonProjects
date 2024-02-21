from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback, ClientsideFunction
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template(["minty",  "minty_dark"])

app = Dash(
    __name__,
    external_stylesheets=[ dbc.themes.MINTY ,dbc.icons.FONT_AWESOME]
)

color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)


app.layout = dbc.Container(
    [
        html.Div(
            ["Pattern-Matching Callbacks ALL"],
            id='title_div',
            style={'padding':'20px'},
        ),
        color_mode_switch,
        html.Div(
            [
                dbc.Button(
                    "ADD FILTER",
                    id="add-filter-btn",
                    n_clicks=0,
                    outline=True,
                    color="info",
                    style={'margin-bottom':'20px'}
                ),
                html.Div(id="dropdown-container-div", children=[]),
                html.Div(id="dropdown-container-output-div"),
            ],
            className='dropdown-dark',
        )
    ],
    id='root_container',
    className='container'
)

@app.callback(
    Output('dropdown-container-div', 'children'),
    Input('add-filter-btn', 'n_clicks')
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    new_dropdown = dcc.Dropdown(
        ['ANYANG','SEOUL',"NYC", "MTL", "LA", "TOKYO"],
        id={"type": "city-filter-dropdown", "index": n_clicks},
        style={'margin-bottom':'10px'}
    )
    patched_children.append(new_dropdown)
    return patched_children


@app.callback(
    Output("dropdown-container-output-div", "children"),
    Input({"type": "city-filter-dropdown", "index": ALL}, "value"),
)
def display_output(values):
    return html.Div(
        [ html.Div(f"Dropdown {i + 1} = {value}") for (i, value) in enumerate(values) ]
    )






app.clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='change_template'
    ),
    Output("root_container", "id"),
    Input("color-mode-switch", "value"),
)





if __name__ == "__main__":
    app.run_server(port=7777, debug=True)