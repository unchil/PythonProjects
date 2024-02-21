import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from dash import Dash, html, Input, Output, ctx, callback,clientside_callback, ClientsideFunction
import plotly.express as px
import datetime
import pandas as pd


app = Dash(prevent_initial_callbacks=True)

app.layout = html.Div(
    [
        html.Button("Button 1", id="btn-1"),
        html.Button("Button 2", id="btn-2"),
        html.Button("Button 3", id="btn-3"),
        html.Div(id="log"),
    ]
)

"""  
# serverside callback 
@callback(Output('log', 'children'),
          Input('btn-1', 'n_clicks'),
          Input('btn-2', 'n_clicks'),
          Input('btn-3', 'n_clicks'))
def update_log(btn1,btn2,btn3):
    triggered_id = ctx.triggered_id if not None else 'No clicks yet'
    return html.Div(f"triggered id:{triggered_id}")
"""

"""
# clientside callback
app.clientside_callback(
    \"""
    function(){
        console.log(dash_clientside.callback_context);
        const triggered_id = dash_clientside.callback_context.triggered_id;
        return "triggered id: " + triggered_id
    }
    \""",
    Output("log", "children"),
    Input("btn-1", "n_clicks"),
    Input("btn-2", "n_clicks"),
    Input("btn-3", "n_clicks"),
)
"""

# clientside callback using assets/.js file
app.clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='update_log'
    ),
    Output("log", "children"),
    Input("btn-1", "n_clicks"),
    Input("btn-2", "n_clicks"),
    Input("btn-3", "n_clicks"),
)



if __name__ == '__main__':
    app.run(port=7777, debug=False)