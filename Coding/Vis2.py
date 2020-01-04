import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input
import datetime
import plotly.graph_objects as go
import Import_Data_API as ImpData




### Set all parameters
wind_data_days = 7


### Get all relevant data
df_wind_week_mythenquai, df_wind_week_tiefenbrunnen = ImpData.get_wind_data(wind_data_days)
df_wind_week_mythenquai, df_wind_week_tiefenbrunnen = df_wind_week_mythenquai.iloc[
                                                          ::4], df_wind_week_tiefenbrunnen.iloc[::4]
df_latest_data = ImpData.get_latest_data()

### Plot Wind
### Define Plots


## Format data
app = dash.Dash(__name__,external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
colors = {'text': '##b4c4de',
          "background":"#ceddf5"
          }
background_image_local = "url(/assets/sailing_picture.jpg)"







app = dash.Dash()


app.layout = html.Div(
    style={"background-color": colors["background"],
           "background-repeat": "no-repeat"
        }
    [
    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    html.Div(
                        children=dcc.Graph(
                            id='left-graph',
                            figure={
                                'data': [{
                                    'x': [1, 2, 3],
                                    'y': [3, 1, 2],
                                    'type': 'bar'
                                }],
                                'layout': {
                                    'height': 800,
                                    'margin': {
                                        'l': 10, 'b': 20, 't': 0, 'r': 0
                                    }
                                }
                            }
                        )
                    )
                ]
            ),
            html.Div(
                className="six columns",
                children=html.Div([
                    dcc.Graph(
                        id='right-top-graph',
                        figure={
                            'data': [{
                                'x': [1, 2, 3],
                                'y': [3, 1, 2],
                                'type': 'bar'
                            }],
                            'layout': {
                                'height': 400,
                                'margin': {'l': 10, 'b': 20, 't': 0, 'r': 0}
                            }
                        }
                    ),
                    dcc.Graph(
                        id='right-bottom-graph',
                        figure={
                            'data': [{
                                'x': [1, 2, 3],
                                'y': [3, 1, 2],
                                'type': 'bar'
                            }],
                            'layout': {
                                'height': 400,
                                'margin': {'l': 10, 'b': 20, 't': 0, 'r': 0}
                            }
                        }
                    ),

                ])
            )
        ]
    )
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})