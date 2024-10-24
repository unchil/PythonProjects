import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
from dash import Dash, html, ClientsideFunction, Input, Output, dcc, Patch, ctx, State
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO

load_figure_template(["minty", "minty_dark", 'cyborg', 'cyborg_dark'])
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,  dbc_css, dbc.icons.FONT_AWESOME], )

df = px.data.wind()
df[["min_strength", "max_strength"]] = (
    df.strength.str.replace("6+", "6-7", regex=False)
    .str.split("-", expand=True)
    .astype(int)
)

dropdown_1 = dcc.Dropdown(
    ["bar", "line"],
    value='bar',
    clearable=False,
    id="dropdown",
)

range_1 = dcc.RangeSlider(
    0,
    7,
    step=1,
    value=[0, 7],
    marks={**{v: str(v) for v in range(7)}, 7: ">6"},
    id="slider"
)

graph_1 = dcc.Graph(id="graph")

blurb = (
    "차트는 방향별 풍속 분포를 보여주며, 서쪽에서 발생하는 바람에 대한 상당한 편향을 보여줍니다."
    "서풍이 두드러지게 우세한 것은 중위도 지역에서 흔히 볼 수 있는 우세한 서풍과 같은 거시적 기후 패턴의 영향을 시사합니다."
    "더 높은 풍속은 주로 서쪽 구역에 집중되어 있어 더 강한 바람 사건이 대부분 이 방향에서 온다는 것을 나타냅니다."
    "이 패턴은 지역 지형적 영향이나 서풍을 주도하는 더 큰 시놉틱 시스템을 반영할 수 있습니다."
)

color_mode_switch = ThemeSwitchAIO(
    aio_id="theme",
    themes=[dbc.themes.MINTY, dbc.themes.CYBORG],
)


app.layout = dbc.Container([

    html.Div([

        color_mode_switch,
        html.H1("Windy wind things", style={'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Windy wind things"),
                        html.P(blurb),
                        dbc.Label("Filter wind intensity"),
                        range_1,
                        dbc.Label("Select chart type"),
                        dropdown_1,
                    ],
                    width=4,
                ),
                dbc.Col(graph_1,),
            ]
        ),

    ],
        className="dbc",
    ),

], id='root_container', )


@app.callback(
    Output("graph", "figure"),
    Input("slider", "value"),
    Input("dropdown", "value")
)
def update_figure(strength_range, graph_type):

    start, stop = min(strength_range), max(strength_range)
    df_copy = df[(df.min_strength >= start) & (df.max_strength <= stop)]

    additional_args = {}
    if graph_type.lower() == "bar":
        func = px.bar_polar
    else:
        func = px.line_polar
        additional_args["line_close"] = True

    fig = func(
        df_copy,
        r="frequency",
        theta="direction",
        color="strength",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        **additional_args,
    )

    return fig


app.clientside_callback(
    ClientsideFunction(
        namespace='test',
        function_name='change_template'
    ),
    Output("root_container", "id"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

if __name__ == '__main__':
    app.run(port=7777, debug=True)
