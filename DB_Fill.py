from influxdb import DataFrameClient
import os
import subprocess
from fhnw_ds_hs2019_weatherstation_api import data_import as weather

#dynamisch anpassen
os.chdir("./influxdb-1.7.8-1")

# DB and CSV config
config = weather.Config()
# define CSV path
config.historic_data_folder='.'+os.sep+'data'
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
weather.import_latest_data(config, True, True)
