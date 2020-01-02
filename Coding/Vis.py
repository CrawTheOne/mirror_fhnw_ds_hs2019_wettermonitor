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
colors = {'text': '##b4c4de'
          }
background_image_local = "url(/assets/sailing_picture.jpg)"



app.layout = html.Div(style={"background-image": background_image_local,
                             "background-size": "1080px 1350px",
                             "background-repeat": "no-repeat"
                             },
                      children = [
    html.H1("Willkommen am Pier!", style={'textAlign': 'center',
                                          'color': colors['text']
                                          }
    ),
    html.Label(
        "Letztes Update : {}".format(datetime.datetime.strftime(datetime.datetime.now(), format = "%Y-%m-%d %H:%M")
                          )
    ),
    html.Div(
        dcc.Dropdown(id = "wind_input", options = [
                                {"label":"Windgeschwindigkeit", "value": "wind_speed_avg_10min"},
                                {"label":"Windkraft", "value":"wind_force_avg_10min"},
                                {"label":"Windböen", "value":"wind_gust_max_10min"}]

                     )
    ),
    html.Div(
        dcc.Graph(id = "Wind_Chart")
    ),
    html.Div(
        dash_table.DataTable(
            id = 'df_latest_data',
            columns = [{"name": i, "id": i} for i in df_latest_data.columns],
            data = df_latest_data.to_dict('records'),
        ),
    ),
    html.Div(
        html.Label(
            "Mast und Schotbruch!", style={'textAlign': 'center',
                                          'color': colors['text']
                                          }
            )
        )
    ]
)


@app.callback(dash.dependencies.Output("Wind_Chart", "figure"),
              [dash.dependencies.Input("wind_input", "value")])
def update_wind(input_value):
    ### Define Plots
    wind_data = go.Scatter(x=df_wind_week_mythenquai.index,
                           y=df_wind_week_mythenquai[input_value],
                           name="Winddaten", line=dict(color="#A9E2F3"))

    plot_wind = [wind_data]

    if input_value == "wind_speed_avg_10min":
        layout_wind = dict(title="Windgeschwindigkeit in km/h")
    if input_value == "wind_force_avg_10min":
        layout_wind = dict(title = "Windkraft in Newton")
    if input_value == "wind_gust_max_10min":
        layout_wind = dict(title = "Windböen")

    figure = dict(data=plot_wind, layout=layout_wind)

    return figure



if __name__ == '__main__':
    app.run_server(debug=True)


