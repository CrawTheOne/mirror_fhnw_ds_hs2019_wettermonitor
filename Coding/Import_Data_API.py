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
    # Set time relative to now for Query (today: 00:00:00)
    now = datetime.datetime.today()
    start = now
    past = now - datetime.timedelta(minutes = 1)

    # Set start and end time
    end_time = start.strftime("%Y-%m-%d %H:%M:%S")
    start_time = past.strftime("%Y-%m-%d %H:%M:%S")

    # NoSQL Query  (to be added: timezone adjusting)
    query = "SELECT * FROM \"{}\",\"{}\" WHERE time >= '{}' AND time <= '{}' LIMIT 1" \
        .format(config.stations[0], config.stations[1], start_time, end_time)
    df_temp = client.query(query)

    # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
    df_mythenquai = pd.DataFrame(df_temp['mythenquai'])
    df_tiefenbrunnen = pd.DataFrame(df_temp['tiefenbrunnen'])

    df_mythenquai = pd.DataFrame(df_mythenquai)
    df_tiefenbrunnen = pd.DataFrame(df_tiefenbrunnen)

    return df_mythenquai, df_tiefenbrunnen

