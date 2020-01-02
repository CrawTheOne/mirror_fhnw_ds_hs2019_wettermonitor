# import the modules
import pandas as pd
from influxdb import DataFrameClient, InfluxDBClient
import pytz
import datetime
import config as cfg
import pandas as pd #add pandas version control 0.24

## Dataframe client used
client = DataFrameClient(host = cfg.DB_HOST, port = cfg.DB_PORT, database = cfg.DB_DBNAME)


# NoSQL Query  (to be added: timezone adjusting)
def DB_query_data(start_time, end_time):
    """
    Queries data from InfluxDB with given start and end time in format YYYY-mm-dd... ('2019-11-28T00:00:00+00:00')
    returns two dataframes in pandas format for mythenquai / tiefenbrunnen
    :param start_time: '2019-11-28T00:00:00+00:00'
    :param end_time: '2019-12-28T00:00:00+00:00'
    :return: df_mythenquai, df_tiefenbrunnen
    """
    query = "SELECT * FROM \"{}\",\"{}\" WHERE time >= '{}' AND time <= '{}' "\
        .format(cfg.stations[0], cfg.stations[1], cfg.start_time, cfg.end_time)

    df_query = client.query(query)

    # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
    df_mythenquai = pd.DataFrame(df_query['mythenquai'])

    df_tiefenbrunnen = pd.DataFrame(df_query['tiefenbrunnen'])

    return df_mythenquai, df_tiefenbrunnen


def select_timedelta(time_offset_days, time_delta_in_days):
    """Make a Select Statement on pass over to new df a certain timedelta from NOW / double_output!: Output1, Output2 = func() /
    example: time_delta_in_days = 10
    Inputs: time_offset_days = 0, time_delta_in_days = 365
    """
    # Set time relative to now for Query (today: 00:00:00)
    now = datetime.datetime.today()
    start = now - datetime.timedelta(days=time_offset_days)
    past = now - datetime.timedelta(days=time_delta_in_days)

    # Set start and end time
    end_time = start.strftime("%Y-%m-%d %H:%M:%S")
    start_time = past.strftime("%Y-%m-%d %H:%M:%S")

    # NoSQL Query  (to be added: timezone adjusting)
    query = "SELECT * FROM \"{}\",\"{}\" WHERE time >= '{}' AND time <= '{}' " \
        .format(cfg.stations[0], cfg.stations[1], start_time, end_time)
    df_temp = client.query(query)

    # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
    df_mythenquai = pd.DataFrame(df_temp['mythenquai'])
    df_tiefenbrunnen = pd.DataFrame(df_temp['tiefenbrunnen'])

    return df_mythenquai, df_tiefenbrunnen


def get_latest_data():
    """Make a Select Statement on pass over to new df a certain timedelta from NOW / double_output!: Output1, Output2 = func() /
    example: time_delta_in_days = 10
    Inputs: time_offset_days = 0, time_delta_in_days = 365
    """

    # NoSQL Query  (to be added: timezone adjusting)
    query1 = "SELECT LAST(*) from {},{}".format(cfg.stations[0], cfg.stations[1])

    df_temp = client.query(query1)

    # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
    df_mythenquai = pd.DataFrame(df_temp['mythenquai'])
    df_tiefenbrunnen = pd.DataFrame(df_temp['tiefenbrunnen'])

    df_mythenquai = df_mythenquai.iloc[:, [0, 1, 2, 4]]
    df_tiefenbrunnen = df_tiefenbrunnen.iloc[:, 4]

    df_adapt = pd.concat([df_mythenquai, df_tiefenbrunnen], axis=1)
    df_adapt.columns = ["Lufttemperatur", "Luftdruck", "Taupunkt", "Luftfeuchtigkeit", "Wassertemperatur"]
    df_adapt = df_adapt.reset_index(drop=True)
    df_adapt = df_adapt.T
    df_adapt = df_adapt

    return df_adapt


def get_wind_data(days):
    """ Selects all wind_data with given amount of days
    :param days: Amount of days for data selection
    :return: dataframes for mythenquai and tiefenbrunnen
    """
    df_mythenquai, df_tiefenbrunnen = select_timedelta(0, 7)

    df_mythenquai = pd.concat([df_mythenquai["wind_direction"], df_mythenquai["wind_force_avg_10min"],
                               df_mythenquai["wind_gust_max_10min"], df_mythenquai["wind_speed_avg_10min"]], axis=1)

    df_tiefenbrunnen = pd.concat([df_mythenquai["wind_direction"], df_mythenquai["wind_force_avg_10min"],
                                  df_mythenquai["wind_gust_max_10min"], df_mythenquai["wind_speed_avg_10min"]], axis=1)

    return df_mythenquai, df_tiefenbrunnen




