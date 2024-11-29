from dash import Dash, dcc, html, Input, Output, dash_table, clientside_callback, ClientsideFunction

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Dropdown(
            options=[
                {
                    "label": "Car-sharing data",
                    "value": "https://raw.githubusercontent.com/plotly/datasets/master/carshare_data.json",
                },
                {
                    "label": "Iris data",
                    "value": "https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json",
                },
            ],
            value="https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json",
            id="data-select",
        ),
        html.Br(),
        dash_table.DataTable(id="my-table-promises", page_size=10),
    ]
)


app.clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='async_fetch'
    ),
    Output("my-table-promises", "data"),
    Input("data-select", "value"),
)

if __name__ == "__main__":
    app.run(port=7788, debug=False)
