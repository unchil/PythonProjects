from dash import (
    Dash, dcc, html, Input, Output, ALL, Patch, callback,
    ClientsideFunction, State, MATCH, ALLSMALLER, ctx
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


app.layout =  dbc.Container(
[
    html.Div(
        ["Todo App"],
        id='title_div',
        style={'padding':'20px'},
    ),
    color_mode_switch,
    html.Div(
        [
            html.Div("Dash To-Do list"),

            html.Div(
                [
                    dbc.Input(id="new-item-input",  type="text"),

                    dbc.Button(
                        "ADD",
                        id="add-btn",
                        outline=True,
                        color="info",
                        style={'margin-left':'10px'}
                    ),
                    dbc.Button(
                        children="CLEAR_DONE",
                        id="clear-done-btn",
                        outline=True,
                        color="info",
                        style={'margin-left':'10px'}
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'row'}
            ),

            html.Div(id="list-container-div", children=[]),

            html.Div(id="totals-div"),
        ],
        style={  'width':600}
    )
        ],
    id='root_container',
    className='container'
)


# Callback to add new item to list
@callback(
    Output("list-container-div", "children", allow_duplicate=True),
    Output("new-item-input", "value"),
    Input("add-btn", "n_clicks"),
    State("new-item-input", "value"),
    prevent_initial_call=True,
)
def add_item(button_clicked, value):
    patched_list = Patch()

    def new_checklist_item():
        return html.Div(
            [

                dbc.Checklist(
                    options=[{"label": "", "value": "done"}, ],
                    id={"index": button_clicked, "type": "done"},
                ),
                html.Div(
                    [value],
                  #  id={"index": button_clicked, "type": "output-str"},
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'row'}
        )

    patched_list.append(new_checklist_item())
    return patched_list, ""


# Callback to update item styling
@callback(
    Output({"index": MATCH, "type": "output-str"}, "style"),
    Input({"index": MATCH, "type": "done"}, "value"),
    prevent_initial_call=True,
)
def item_selected(input):
    if not input:
        style = {"display": "inline", "margin-right": "10px",}
    else:
        style = {
            "display": "inline",
            "margin-right": "10px",
            "textDecoration": "line-through",
            "color": "#888",
        }
    return style


# Callback to delete items marked as done
@callback(
    Output("list-container-div", "children", allow_duplicate=True),
    Input("clear-done-btn", "n_clicks"),
    State({"index": ALL, "type": "done"}, "value"),
    prevent_initial_call=True,
)
def delete_items(n_clicks, state):
    patched_list = Patch()
    values_to_remove = []
    for i, val in enumerate(state):
        if val:
            values_to_remove.insert(0, i)
    for v in values_to_remove:
        del patched_list[v]
    return patched_list


# Callback to update totals
@callback(
    Output("totals-div", "children"),
    Input({"index": ALL, "type": "done"}, "value")
)
def show_totals(done):

    count_all = len(done)
    count_done = len([d for d in done if d])
    result = f"{count_done} of {count_all} items completed"
    if count_all:
        result += f" - {int(100 * count_done / count_all)}%"
    return result






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
