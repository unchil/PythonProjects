import dash
from dash import Dash, dcc, html, clientside_callback, Input, Output, Patch, ctx, ClientsideFunction
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio


load_figure_template(["minty",  "minty_dark", 'cyborg', 'cyborg_dark'])


color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)


df = px.data.gapminder()

dff = px.data.gapminder().query(f"year == {np.sort(df.year.unique())[::-1][0].item()}")

fig = px.sunburst(
    dff,
    path=["continent", "country"],
    values="pop",
    color="lifeExp",
    hover_data=["iso_alpha"],
    color_continuous_scale="RdBu",
    color_continuous_midpoint=np.average(df["lifeExp"], weights=df["pop"]),
    template='minty'
)
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

fig_gapminder = px.scatter(
    dff,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    [
        html.Div(
            ["Dash Chart Tab Example"],
            id='title_div',
            style={'padding':'10px'},
        ),
        color_mode_switch,
        dcc.Tabs(
            [
                dcc.Tab(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Select year:"),
                                    dcc.Dropdown(
                                        id="year",
                                        options=df.year.unique(),
                                        value=np.sort(df.year.unique())[::-1][0].item(),
                                        clearable=False,
                                        #     className='dropdown-dark'
                                    ),
                                ],
                                width=3,
                            ),
                            dbc.Col(
                                [dcc.Graph(id="graph", figure=fig)],
                                width=9,
                            ),
                        ]
                    ),
                    label="Gapminder_Sunburst"
                ),
                dcc.Tab(
                    dcc.Graph(id='graph_scatter', figure=fig_gapminder),
                    label="Gapminder_Scatter"
                ),
            ]
        )
    ],
    id='root_container',
    className='container'
)


@app.callback(
    Output("graph", "figure"),
    Output("graph_scatter", "figure"),

    inputs={
        'input_dict':{
            'dropdown_year': Input("year", "value"),
            'switch_template': Input("color-mode-switch", "value")
        }
    },
    prevent_initial_call=True
)
def generate_graph(input_dict):

    inputs = ctx.args_grouping.input_dict

    if inputs.dropdown_year.triggered:
        dff = px.data.gapminder().query(f"year == {inputs.dropdown_year.value}")
        fig = px.sunburst(
            dff,
            path=["continent", "country"],
            values="pop",
            color="lifeExp",
            hover_data=["iso_alpha"],
            color_continuous_scale="RdBu",
            color_continuous_midpoint=np.average(df["lifeExp"], weights=df["pop"]),
            template='minty' if inputs.switch_template.value else 'minty_dark'
        )
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        return fig, dash.no_update

    elif inputs.switch_template.triggered:
        patched_figure = Patch()
        patched_figure["layout"]["template"] = pio.templates["minty"] if inputs.switch_template.value else pio.templates["minty_dark"]
        return patched_figure, patched_figure

    return (dash.no_update, dash.no_update)


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
