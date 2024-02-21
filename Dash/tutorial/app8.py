
import dash_bootstrap_components as dbc
from dash import  Dash, Input, Output, html,  callback,  dcc, Patch, ctx
import plotly.express as px
import json
import traceback



df = px.data.gapminder()
df= df.drop(columns=['iso_alpha','iso_num'])
df = df.groupby(['continent','country','year']).mean().reset_index()

def custom_error_handler(err):
    msg = f"""
    Message: {err}\n\n
    Traceback info: {traceback.format_exc()}\n\n
    Input info: {json.dumps(ctx.triggered)}
    """
    print(msg)

app = Dash(external_stylesheets=[dbc.themes.DARKLY],)




init_continent_list = df.continent.unique()
init_country_list= df[ df.continent == init_continent_list[0] ].country.unique()
item_list = ["lifeExp", "pop", "gdpPercap"]


fig = px.bar(
    df[ (df.continent == init_continent_list[0]) & (df.country == init_country_list[0])],
    x='year',
    y= item_list[0],
    template="plotly_dark",
    title=f'{init_continent_list[0]}/{init_country_list[0]}/{item_list[0]}',
    height=600
)



app.layout =html.Div( [
        html.Div(
            [
                dcc.Dropdown(
                    id="dropdown-input1",
                    options=init_continent_list,
                    value=init_continent_list[0],
                ),
                dcc.Dropdown(
                    id="dropdown-input2",
                    options=init_country_list,
                    value=init_country_list[0],
                ),
                dcc.Dropdown(
                    id="dropdown-input3",
                    options=item_list,
                    value=item_list[0],
                ),
            ],

        ),
        dcc.Graph(id="graph-output", figure=fig),
    ],
    className='dropdown-dark',
)

@app.callback(
    [
        Output("dropdown-input2", "options"),
        Output("dropdown-input2", "value"),
     ],
    Input("dropdown-input1", "value"),
    on_error=custom_error_handler,
    prevent_initial_call=True,
)
def update_country(continent):
    patched_dropdown = Patch()
    options = df[ df.continent == continent ].country.unique()
    value = df[ df.continent == continent ].country.unique()[0]
    patched_dropdown.clear()
    patched_dropdown.update(dict(zip(options,options)))
    return [patched_dropdown, value]


@app.callback(
    Output("graph-output", "figure"),
    Input("dropdown-input1", "value"),
    Input("dropdown-input2", "value"),
    Input("dropdown-input3", "value"),
    on_error=custom_error_handler,
)
def update_graph(continent, country,  item):
    data = df[ (df.continent == continent) & (df.country == country)]
    fig = px.bar(
        data,
        x='year',
        y=item,
        template="plotly_dark",
        title=f'{continent}/{country}/{item}',
        height= 600
    )
    return fig


if __name__ == "__main__":
    app.run(port=7777, debug=False)