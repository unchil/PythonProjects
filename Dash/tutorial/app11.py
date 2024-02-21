from dash import (
    Dash, dcc, html, Input, Output, ALL, Patch, callback,
    ClientsideFunction, State, MATCH
)
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
            ["Pattern-Matching Callbacks MATCH"],
            id='title_div',
            style={'padding':'20px'},
        ),
        color_mode_switch,
        html.Div(
            [
                dbc.Button(
                    "ADD FILTER",
                    id="dynamic-add-filter-btn",
                    n_clicks=0,
                    outline=True,
                    color="info",
                    style={'margin-bottom':'20px'}
                ),
                html.Div(id="dynamic-dropdown-container-div", children=[]),
            ],
            className='dropdown-dark',
        )
    ],
    id='root_container',
    className='container'
)

@app.callback(
    Output('dynamic-dropdown-container-div', 'children'),
    Input('dynamic-add-filter-btn', 'n_clicks')
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    new_element = html.Div(
        [
            dcc.Dropdown(
                ['ANYANG','SEOUL',"NYC", "MTL", "LA", "TOKYO"],
                id={
                    "type": "city-dynamic-dropdown",
                    "index": n_clicks
                },
                style={'margin-bottom':'10px'}
            ),
            html.Div(
                id={
                    'type': 'city-dynamic-output',
                    'index': n_clicks
                }
            )
        ],
        style={'margin-bottom':'20px'}
    )
    patched_children.append(new_element)
    return patched_children

@app.callback(
    Output({'type': 'city-dynamic-output', 'index': MATCH}, 'children'),
    Input({'type': 'city-dynamic-dropdown', 'index': MATCH}, 'value'),
    State({'type': 'city-dynamic-dropdown', 'index': MATCH}, 'id'),
)
def display_output(value, id):
    return html.Div(f"Dropdown {id['index']} = {value}")







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