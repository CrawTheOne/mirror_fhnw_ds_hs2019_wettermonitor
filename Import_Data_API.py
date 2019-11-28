# import the modules
import pandas as pd
from influxdb import DataFrameClient, InfluxDBClient

#add pandas version control 0.24

from DB_Fill import DB_HOST, DB_PORT, DB_DBNAME

client = InfluxDBClient(host = DB_HOST, port = DB_PORT)

db_name = 'meteorology'
protocol = 'line'

print("Created Mythenquai DataFrame")
df_1 = pd.read_csv('./data/messwerte_mythenquai_2019.csv')
df_1.info()

print("Created Tiefenbrunnen DataFrame")
df_2 = pd.read_csv('./data/messwerte_tiefenbrunnen_2019.csv')
df_2.info()

client.get_list_database()