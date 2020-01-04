import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import datetime
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import Import_Data_API as ImpData
import config as cfg

### Set all parameters
wind_data_days = cfg.wind_data_days
table_update_seconds = cfg.table_update_seconds

### Get all relevant data
df_latest_data = ImpData.get_latest_data()


## Format data
app = dash.Dash(__name__,external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
colors = {'text': '##b4c4de'}


app.layout = html.Div(
    children = [
            html.H1(
                "Willkommen am Pier!", style={'textAlign': 'center',
                                          'color': colors['text']
                                          }
                ),
            html.Div(id='live-update-text',
                style={'font-size': '15px'}),
            dcc.Interval(
                id='interval-component',
                interval= table_update_seconds*1000, # in milliseconds
                n_intervals=0
            ),
            html.Div([
                html.Div([
                    dcc.Dropdown(id = "wind_input", options = [
                                {"label":"Windgeschwindigkeit", "value": "wind_speed_avg_10min"},
                                {"label":"Windkraft", "value":"wind_force_avg_10min"},
                                {"label":"Windböen", "value":"wind_gust_max_10min"}],
                                value = "wind_speed_avg_10min"
                    ),
                    dcc.Graph(
                        id = "Wind_Chart"
                    ),
                    dcc.Interval(
                        id='wind_update',
                        interval = table_update_seconds * 1000,  # in milliseconds
                        n_intervals = 0
                    )
                ],
                    className= "six columns"
                ),
                html.Div(
                    [
                    html.Div(
                        dash_table.DataTable(
                            id='df_latest_data',
                            columns=[{"name": i, "id": i} for i in df_latest_data.columns],
                            data = df_latest_data.to_dict('records'),
                            style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                            },
                            style_cell_conditional=[
                                    {'if': {'column_id': ''},
                                    'width': '50%'},
                                    {'if': {'column_id': 'Werte'},
                                    'width': '50%'}
                            ],
                        )
                    ),
                        dcc.Interval(
                            id='interval_component_table',
                            interval = table_update_seconds * 1000,  # in milliseconds
                            n_intervals = 0
                        ),
                        html.H5(
                            "Windrichtung in Grad°",
                            style={
                                'textAlign': 'center',
                                'color': colors['text']
                            }
                        ),
                        html.Label(
                            "0° ist Norden",
                            style={
                                'textAlign': 'center',
                                'color': colors['text']
                            }
                        ),
                        dcc.Graph(
                            id="wind-direction",
                            figure=dict(
                                layout=dict(
                                plot_bgcolor="white",
                                paper_bgcolor="grey",
                                )
                            )
                        ),
                        dcc.Interval(
                            id='wind_direction_update',
                            interval = table_update_seconds * 1000,  # in milliseconds
                            n_intervals = 0
                        )
                    ], className="six columns"
                    )
                    ])
                ]
            )



@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_date(n):

    date_now = datetime.datetime.now()
    date_now = datetime.datetime.strftime(date_now, format = "%Y-%m-%d %H:%M")

    return [html.P('Last updated: {} '.format(date_now))]


@app.callback(dash.dependencies.Output("Wind_Chart", "figure"),
              [dash.dependencies.Input("wind_input", "value"),
               dash.dependencies.Input("wind_update", "n_intervals")])
def update_wind(input_value, n):
    ### Define Plots

    update_wind, update_wind2 = ImpData.get_wind_data(wind_data_days)
    update_wind, update_wind2 = update_wind.iloc[::10], update_wind2.iloc[::10]

    wind_data1 = go.Scatter(x=update_wind.index,
                           y=update_wind[input_value],
                           name="Mythenquai", line=dict(color="#69c1ff"))
    wind_data2 = go.Scatter(x=update_wind2.index,
                           y=update_wind2[input_value],
                           name="Tiefenbrunnen", line=dict(color="#ff9869"))

    plot_wind = [wind_data1, wind_data2]

    if "wind_speed" in input_value:
        layout_wind = dict(title="Windgeschwindigkeit in (m/s)")
    if "wind_force" in input_value:
        layout_wind = dict(title = "Windkraft nach Belfort")
    if "wind_gust" in input_value:
        layout_wind = dict(title = "Windböen (m/s)")


    figure = dict(data=plot_wind, layout = layout_wind)

    return figure


@app.callback(
        dash.dependencies.Output('df_latest_data', 'data'),
        [dash.dependencies.Input('interval_component_table', 'n_intervals')]
        )
def updateTable(n):
     """
     calling the get data function
     """
     updated_data = ImpData.get_latest_data()

     return updated_data.to_dict('records')




@app.callback(
    Output("wind-direction", "figure"),
    [Input("wind_direction_update", "n_intervals")]
)
def gen_wind_direction(interval):
    """
    Generate the wind direction graph.
    :params interval: update the graph based on an interval
    """

    wind_direction_mq, wind_direction_tb = ImpData.get_last_wind_direction()

    val = wind_direction_mq.iloc[0, 1] * 3.6

    direction = [0, (wind_direction_mq.iloc[0,0] - 20), (wind_direction_mq.iloc[0,0] + 20), 0]

    traces_scatterpolar = [
        {"r": [0, val, val, 0], "fillcolor": "#084E8A"},
        {"r": [0, val * 0.65, val * 0.65, 0], "fillcolor": "#B4E1FA"},
        {"r": [0, val * 0.3, val * 0.3, 0], "fillcolor": "#EBF5FA"},
    ]

    data = [
        dict(
            type="scatterpolar",
            r=traces["r"],
            theta=direction,
            mode="lines",
            fill="toself",
            fillcolor=traces["fillcolor"],
            line={"color": "rgba(32, 32, 32, .6)", "width": 1},
        )
        for traces in traces_scatterpolar
    ]

    layout = dict(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={"color": "black"},
        autosize=False,
        polar={
            "bgcolor": "white",
            "radialaxis": {"range": [0, 45], "angle": 45, "dtick": 10},
            "angularaxis": {"showline": False, "tickcolor": "white"},
        },
        showlegend=False,
    )

    return dict(data=data, layout=layout)



if __name__ == '__main__':
    app.run_server(debug=True)

