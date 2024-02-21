from dash import Dash, html, dcc, Input, Output, Patch, callback
import plotly.express as px
import random
import dash_bootstrap_components as dbc


app = Dash(__name__,  external_stylesheets=[dbc.themes.DARKLY])

df = px.data.iris()

fig = px.scatter(
    df, x="sepal_length", y="sepal_width", color="species", title="Updating Title Color",  template="plotly_dark",
    width=800, height= 600
)

fig.update_layout(
    title = {
        'y':0.9,         'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'

    }
)

app.layout = html.Center(

    html.Div(
        [
            html.P(),
            dbc.Button("Update Graph Color", id="update-color-button-2",  outline=True, color="info", style={'background-color': 'rgb(25, 25, 25)'}),
            html.P(),
            dcc.Graph(figure=fig, id="my-fig"),
        ],
    ),

)


@callback(Output("my-fig", "figure"), Input("update-color-button-2", "n_clicks"))
def my_callback(n_clicks):
    # Defining a new random color
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    new_color = f"rgb({red}, {green}, {blue})"

    num = 0 if n_clicks == None else n_clicks

    def getPosition():
        match (num%3):
            case 0:
                return 'left'
            case 1:
                return 'right'
            case _:
                return 'center'


    # Creating a Patch object
    patched_figure = Patch()

    patched_figure.layout.title.font.color = new_color
    patched_figure.layout.title.xanchor = getPosition()

    return patched_figure



if __name__ == '__main__':
    app.run(port=7777, debug=True)