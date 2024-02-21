from dash import (
    Dash, dcc, html, Input, Output, ALL, Patch, callback,
    ClientsideFunction, State, MATCH, ALLSMALLER
)
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


import plotly.express as px
df = px.data.gapminder()

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
            ["Pattern-Matching Callbacks ALLSMALLER"],
            id='title_div',
            style={'padding':'20px'},
        ),
        color_mode_switch,
        html.Div(
            [
                dbc.Button(
                    "ADD FILTER",
                    id="add-filter-ex3-btn",
                    n_clicks=0,
                    outline=True,
                    color="info",
                    style={'margin-bottom':'20px'}
                ),
                html.Div(id="container-ex3-div", children=[]),
            ],
            className='dropdown-dark',
        )
    ],
    id='root_container',
    className='container'
)


@app.callback(
    Output('container-ex3-div', 'children'),
    Input('add-filter-ex3-btn', 'n_clicks')
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    new_element = html.Div(
        [
            dcc.Dropdown(
                df['country'].unique(),
                df['country'].unique()[n_clicks],
                id={
                    "type": "filter-dd-ex3",
                    "index": n_clicks
                },
                style={'margin-bottom':'10px'}
            ),
            html.Div(
                id={
                    'type': 'output-div-ex3',
                    'index': n_clicks
                }
            )
        ],
        style={'margin-bottom':'20px'}
    )
    patched_children.append(new_element)
    return patched_children



@app.callback(
    Output({'type': 'output-div-ex3', 'index': MATCH}, 'children'),
    Input({'type': 'filter-dd-ex3', 'index': MATCH}, 'value'),
    Input({'type': 'filter-dd-ex3', 'index': ALLSMALLER}, 'value'),
)
def display_output(matching_value, previous_values):
    previous_values_in_reversed_order = previous_values[::-1]
    all_values = [matching_value] + previous_values_in_reversed_order

    dff = df[df['country'].str.contains('|'.join(all_values))]
    avgLifeExp = dff['lifeExp'].mean()

    # Return a slightly different string depending on number of values
    if len(all_values) == 1:
        return html.Div('{:.2f} is the life expectancy of {}'.format(
            avgLifeExp, matching_value
        ))
    elif len(all_values) == 2:
        return html.Div('{:.2f} is the average life expectancy of {}'.format(
            avgLifeExp, ' and '.join(all_values)
        ))
    else:
        return html.Div('{:.2f} is the average life expectancy of {}, and {}'.format(
            avgLifeExp, ', '.join(all_values[:-1]), all_values[-1]
        ))







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
