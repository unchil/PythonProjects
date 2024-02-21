from dash import Dash, html, dcc, Input, Output, Patch, callback, ctx
import plotly.express as px
import random
import dash_bootstrap_components as dbc


app = Dash(__name__,  external_stylesheets=[dbc.themes.DARKLY])


df = px.data.election()[:20]
# Create figure based on data
fig = px.bar(df,   x="district",  template="plotly_dark",  width=800, height= 600)


app.layout = html.Center(
    [   html.P(),
        html.Div(
            [
                dcc.Dropdown(
                    options= ["Coderre", "Joly", "Bergeron"],
                    id="candidate-select",
                    value="Joly",
                    className='dropdown-dark'
                ),
            ],
            style={'width':800},
        ),
        html.P(),
        dcc.Graph(figure=fig, id="new-data-graph"),
    ]
)

@callback(Output("new-data-graph", "figure"), Input("candidate-select", "value"))
def update_figure(value):
    patched_fig = Patch()
    patched_fig["data"][0]["y"] = df[value].values
    return patched_fig



if __name__ == '__main__':
    app.run(port=7777, debug=True)