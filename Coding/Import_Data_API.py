# import the modules
import pandas as pd
from influxdb import DataFrameClient, InfluxDBClient
import pytz
#add pandas version control 0.24

import config

client = DataFrameClient(host = config.DB_HOST, port = config.DB_PORT, database = config.DB_DBNAME)

start_time = '2019-10-01T00:00:00+00:00'
end_time = '2019-11-28T00:00:00+00:00'

client = DataFrameClient(host = config.DB_HOST, port = config.DB_PORT, database = config.DB_DBNAME)

# NoSQL Query  (to be added: timezone adjusting)
query = "SELECT * FROM \"{}\",\"{}\" WHERE time >= '{}' AND time <= '{}' "\
    .format(config.stations[0], config.stations[1], start_time, end_time)

df_air_temp = client.query(query)

# to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
mythenquai_nov_dez = pd.DataFrame(df_air_temp['mythenquai'])
mythenquai_nov_dez.info()

tiefenbrunnen_nov_dez = pd.DataFrame(df_air_temp['tiefenbrunnen'])
tiefenbrunnen_nov_dez.info()



#client.get_list_database()
#client.switch_database(config.DB_DBNAME)
#query = "SELECT COUNT(air_temperature) FROM \"{}\",\"{}\" tz('Europe/Zurich')".format(config.stations[0], config.stations[1])
#result = client.query(query)
#print(result[config.stations[0]])
#print(result[config.stations[1]])
