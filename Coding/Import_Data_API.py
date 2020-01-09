# import the modules
import datetime
import config as cfg
import pandas as pd #add pandas version control 0.24


# NoSQL Query  (to be added: timezone adjusting)
def DB_query_data(start_time, end_time):
    """
    Queries data from InfluxDB with given start and end time in format YYYY-mm-dd... ('2019-11-28T00:00:00+00:00')
    returns two dataframes in pandas format for mythenquai / tiefenbrunnen
    :param start_time: '2019-11-28T00:00:00+00:00'
    :param end_time: '2019-12-28T00:00:00+00:00'
    :return: df_mythenquai, df_tiefenbrunnen
    """

    if len(cfg.stations) == 2:
        query = "SELECT * FROM \"{}\",\"{}\" WHERE time >= '{}' AND time <= '{}' " \
            .format(cfg.stations[0], cfg.stations[1], cfg.start_time, cfg.end_time)


    df_query = cfg.client.query(query)

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
    past = start - datetime.timedelta(days=time_delta_in_days)

    # Set start and end time
    end_time = start.strftime("%Y-%m-%d %H:%M:%S")
    start_time = past.strftime("%Y-%m-%d %H:%M:%S")

    # NoSQL Query  (to be added: timezone adjusting)
    if len(cfg.stations) == 2:
        query = "SELECT * FROM \"{}\",\"{}\" WHERE time >= '{}' AND time <= '{}' " \
            .format(cfg.stations[0], cfg.stations[1], start_time, end_time)

    df_temp = cfg.client.query(query)

    # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
    df_mythenquai = pd.DataFrame(df_temp[cfg.stations[0]])
    df_tiefenbrunnen = pd.DataFrame(df_temp[cfg.stations[1]])

    return df_mythenquai, df_tiefenbrunnen



def get_latest_data():
    """Make a Select Statement on pass over to new df a certain timedelta from NOW / double_output!: Output1, Output2 = func() /
    example: time_delta_in_days = 10
    Inputs: time_offset_days = 0, time_delta_in_days = 365
    """

    # NoSQL Query  (to be added: timezone adjusting)
    query1 = "SELECT LAST(*) from {},{}".format(cfg.stations[0], cfg.stations[1])

    df_temp = cfg.client.query(query1)

    # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
    df_mythenquai = pd.DataFrame(df_temp[cfg.stations[0]])
    df_tiefenbrunnen = pd.DataFrame(df_temp[cfg.stations[1]])

    df_mythenquai = df_mythenquai.iloc[:, [0, 1, 2, 4]]
    df_tiefenbrunnen = df_tiefenbrunnen.iloc[:, 4]

    df_adapt = pd.concat([df_mythenquai, df_tiefenbrunnen], axis=1)
    df_adapt.columns = ["Lufttemperatur(°C)", "Luftdruck(hPa)", "Taupunkt(°C)", "Luftfeuchtigkeit(%)", "Wassertemperatur(°C)"]
    df_adapt = df_adapt.reset_index(drop=True)
    df_adapt = df_adapt.T
    df_adapt = df_adapt.reset_index()
    df_adapt.columns = ["Messgrösse","Messwerte"]

    return df_adapt



def get_last_wind_direction():
    """ Outputs the last Wind direction measured in both stations. It is used for the dashboard
    :return: Wind direction of both stations
    """
    if len(cfg.stations) == 2:
        query1 = "SELECT LAST(*) from {},{}".format(cfg.stations[0], cfg.stations[1])

    df_temp = cfg.client.query(query1)

    # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
    df_mythenquai = pd.DataFrame(df_temp[cfg.stations[0]])
    df_tiefenbrunnen = pd.DataFrame(df_temp[cfg.stations[1]])

    df_wind_direction_mythenquai = df_mythenquai.iloc[:,[8, 11]]
    df_wind_direction_tiefenbrunnen = df_tiefenbrunnen.iloc[:,[5, 8]]

    return df_wind_direction_mythenquai, df_wind_direction_tiefenbrunnen



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



def select_timedelta_ext(time_offset_days, time_delta_in_days, client, station):
    """This functino provides data with a given timedelta for the selection.
    :parameter: time_offset_days = offset time from now / time_delta_in_days = how much days to select from offset time /
                client = database client / station = list of station to be queried
    :returns: Output: A list of Dataframes of the given client and station
    """
    df_list = []

    # Set time relative to now for Query (today: 00:00:00)
    now = datetime.datetime.today()
    start = now - datetime.timedelta(days=time_offset_days)
    past = start - datetime.timedelta(days=time_delta_in_days)

    # Set start and end time
    end_time = start.strftime("%Y-%m-%d %H:%M:%S")
    start_time = past.strftime("%Y-%m-%d %H:%M:%S")

    # NoSQL Query  (to be added: timezone adjusting)
    for station in station:
        query = "SELECT * FROM {} WHERE time >= '{}' AND time <= '{}' " .format(station, start_time, end_time)
        df_temp = client.query(query)
        df_temp = pd.DataFrame(df_temp[station])
        df_list.append(df_temp)

    return df_list



def get_latest_data_ext(client, stations):
    """This function is in order to query data with an extended datasource. The data won't be formatted as in the function with the given functions,
    because from this instant its's not clear which attributes or column names are available in the new datasource. This function queries data and
    gives back a dataframe which consists of a pandas formatted dataframe of the newest row of the source.
    :parameter
    :returns
    """
    df_list = []

    # NoSQL Query  (to be added: timezone adjusting)
    if cfg.ext_datasource == False:
        print("No external data source given which is required for this SELECT function to perform. Please make sure using the correct Stations")

    #else:
    for station in stations:
        query = "SELECT LAST(*) from {}".format(station)
        df_temp = client.query(query)
        df_temp = pd.DataFrame(df_temp[station])
        df_list.append(df_temp)

    return df_list
