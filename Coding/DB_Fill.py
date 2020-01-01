import config as cfg
import os
import subprocess
from fhnw_ds_hs2019_weatherstation_api import data_import as weather

# define the database connection string
#DB and CSV config
config = weather.Config()
subprocess.Popen("./influxdb-1.7.8-1/influxd.exe")
subprocess.Popen("./influxdb-1.7.8-1/influx.exe")
#dynamisch anpassen des Datenpfads
os.chdir("./influxdb-1.7.8-1")
#define CSV path
config.historic_data_folder='.'+os.sep+'data'
#set batch size for DB inserts (decrease for raspberry pi)
config.historic_data_chunksize=10000
#define DB host
cfg.db_host='localhost'


def DB_connect():
    # connect to DB
    weather.connect_db(config)

def DB_clean():
    # clean DB
    weather.clean_db(config)

def DB_import_data():
    weather.import_historic_data(config)
    # import latest data (delta between last data point in DB and current time)
    weather.import_latest_data(config, True, True)

