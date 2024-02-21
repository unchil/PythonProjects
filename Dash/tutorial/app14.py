import random

import dash
import plotly.io as pio
from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback, ClientsideFunction, State, MATCH, ALLSMALLER, ctx

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px

load_figure_template(["minty",  "minty_dark", 'cyborg', 'cyborg_dark'])

app = Dash(
    __name__,
    external_stylesheets=[ dbc.themes.MINTY, dbc.themes.CYBORG ,dbc.icons.FONT_AWESOME]
)

color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

df = px.data.iris()

def get_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return f"rgb({red}, {green}, {blue})"


fig = px.scatter(
    df, title="Updating Title Color", x="sepal_length", y="sepal_width",
    symbol="species",
    color_discrete_sequence=['crimson', 'royalblue', 'darkorange'],
    color='species',
    template='minty_dark'
)

fig.update_layout(
    title_x =0.5,
    title_y = 0.9,
    title_xanchor = "center",
    title_yanchor = "middle"
)


app.layout =  dbc.Container(
    [
        html.Div(
            ["Partial Property Updates"],
            id='title_div',
            style={'padding':'20px'},
        ),
        color_mode_switch,
        html.Div(
            [
                dbc.Button(
                    "Update Graph Color",
                    id="update-color-button",
                    n_clicks=0,
                    outline=True,
                    color="info",
                    style={'margin-bottom':'20px'}
                ),
                dcc.Graph(id="update-color-fig", figure=fig),
            ]
        ),
    ],
    id='root_container',
    className='container'
)


@app.callback(
    Output("update-color-fig", "figure"),
    inputs={
        'input_dict':{
            'btn_textcolor': Input("update-color-button", "n_clicks"),
            'switch_template': Input("color-mode-switch", "value")
        }
    },
    prevent_initial_call=True
)
def update_figure(input_dict):
    patched_figure = Patch()

    inputs = ctx.args_grouping.input_dict

    if inputs.btn_textcolor.triggered:
        patched_figure['layout']['title']['font']['color'] = get_color()
    elif inputs.switch_template.triggered:
        patched_figure["layout"]["template"] = pio.templates["minty"] if inputs.switch_template.value else pio.templates["minty_dark"]

    return patched_figure



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
