# install the modules on the OS
#!pip install influxdb

# import the modules
import pandas as pd

#add pandas version control 0.24

from influxdb import DataFrameClient, InfluxDBClient
import os
import subprocess
from fhnw_ds_hs2019_weatherstation_api import data_import as weather

# define the database connection string

#dynamic host
#DB_HOST = subprocess.getoutput('hostname')
DB_HOST = 'localhost'
DB_PORT = 8086
DB_DBNAME = 'meteorology'
stations = ['mythenquai', 'tiefenbrunnen']

print(DB_HOST +":"+str(DB_PORT))

#Datenbank starten
subprocess.Popen("./influxdb-1.7.8-1/influxd.exe")
subprocess.Popen("./influxdb-1.7.8-1/influx.exe")

os.chdir("./influxdb-1.7.8-1")

## Vorgegebener Code
# DB and CSV config
config = weather.Config()
# define CSV path
config.historic_data_folder='./'+os.sep+'data'
# set batch size for DB inserts (decrease for raspberry pi)
config.historic_data_chunksize=10000
# define DB host
config.db_host='localhost'
# connect to DB
weather.connect_db(config)

# clean DB
weather.clean_db(config)
# import historic data
weather.import_historic_data(config)
# import latest data (delta between last data point in DB and current time)
weather.import_latest_data(config, True)


client = InfluxDBClient(host = DB_HOST, port = DB_PORT)

db_name = 'meteorology'
protocol = 'line'

print("Created Mythenquai DataFrame")
df_1 = pd.read_csv('./data/messwerte_mythenquai_2019.csv')
df_1.info()

print("Created Tiefenbrunnen DataFrame")
df_2 = pd.read_csv('./data/messwerte_tiefenbrunnen_2019.csv')
df_2.info()