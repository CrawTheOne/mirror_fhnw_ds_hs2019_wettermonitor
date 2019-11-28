# import the modules
import pandas as pd
from influxdb import DataFrameClient, InfluxDBClient

#add pandas version control 0.24

import config

client = DataFrameClient(host = config.DB_HOST, port = config.DB_PORT, database = config.DB_DBNAME)

#print("Created Mythenquai DataFrame")
#df_1 = pd.read_csv('./data/messwerte_mythenquai_2019.csv')
#df_1.info()

#print("Created Tiefenbrunnen DataFrame")
#df_2 = pd.read_csv('./data/messwerte_tiefenbrunnen_2019.csv')
#df_2.info()

client.get_list_database()
client.switch_database(config.DB_DBNAME)

query = "SELECT COUNT(air_temperature) FROM \"{}\",\"{}\" tz('Europe/Zurich')".format(config.stations[0], config.stations[1])
result = client.query(query)
print(result[config.stations[0]])
print(result[config.stations[1]])
