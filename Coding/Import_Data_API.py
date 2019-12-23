# import the modules
import pandas as pd
from influxdb import DataFrameClient, InfluxDBClient
import pytz
#add pandas version control 0.24
import config

## Dataframe client used
client = DataFrameClient(host = config.DB_HOST, port = config.DB_PORT, database = config.DB_DBNAME)


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
        .format(config.stations[0], config.stations[1], config.start_time, config.end_time)

    df_query = client.query(query)

    # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
    df_mythenquai = pd.DataFrame(df_query['mythenquai'])

    df_tiefenbrunnen = pd.DataFrame(df_query['tiefenbrunnen'])

    return df_mythenquai, df_tiefenbrunnen



