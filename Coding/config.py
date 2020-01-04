from influxdb import DataFrameClient

## Database information
DB_HOST = 'localhost'
DB_PORT = 8086
DB_DBNAME = 'meteorology'
stations = ['mythenquai', 'tiefenbrunnen']

print(DB_HOST +":"+str(DB_PORT))

### Import Data_API (data import)
client = DataFrameClient(host = DB_HOST, port = DB_PORT, database = DB_DBNAME)
days_delta = 365

start_time = '2019-10-01T00:00:00+00:00'
end_time = '2019-11-28T00:00:00+00:00'

### Prediction.py (Prediction-file)
prediction_file_path = "./influxdb-1.7.8-1/data/messwerte_mythenquai_2007-2018.csv"

### Vis.py (Visualization Parameters)
wind_data_days = 7
table_update_seconds = 600



class connection:

    def __init__(self, name):
        self.name = name

    def change_name(self, new_name):
        self.name = new_name

"""
class connection:

    def __init__(self, name):
        self.name = name
    def __init__(self, DB_HOST, DB_PORT, DB_DBNAME, stations):
        self.df = df

    def change_name(self, new_name):
        self.name = new_name

class indexing:

    def __init__(self, df):
        self.df = df

    def rowindex_as_col(self, df):
        "add row index(time) to new column. df = dataframe, name_col = new column name"
        df.index.name = "time"
        df = df.reset_index(inplace = False)
        df = pd.DataFrame(df)
        return df

    def add_time_column(self, df):
        while True:
            try:
                df = rowindex_as_col(df)
                # show it worked!
                # df.info()

                return df
                break
            except ValueError:
                return print("The column time already exists!")
                break

class time:

    def __init__(self, df):
        self.df = df

    def select_timedelta(self, time_delta_in_days):
        "Make a Select Statement on pass over to new df a certain timedelta from NOW / double_output!: Output1, Output2 = func() /
        example: time_delta_in_days = 10"
        # Set time relative to now for Query (today: 00:00:00)
        now = datetime.datetime.today()
        past = now - datetime.timedelta(days=time_delta_in_days)

        # Set start and end time
        end_time = now.strftime("%Y-%m-%d %H:%M:%S")
        start_time = past.strftime("%Y-%m-%d %H:%M:%S")

        # NoSQL Query  (to be added: timezone adjusting)
        query = "SELECT * FROM \"{}\",\"{}\" WHERE time >= '{}' AND time <= '{}' " \
            .format(config.stations[0], config.stations[1], start_time, end_time)
        df_temp = client.query(query)

        # to create pandas df, use only one dicitonary part (mythenquai, tiefenbrunnen)
        df_mythenquai = pd.DataFrame(df_temp['mythenquai'])
        df_tiefenbrunnen = pd.DataFrame(df_temp['tiefenbrunnen'])

        df_mythenquai, df_tiefenbrunnen = add_time_column(df_mythenquai, df_tiefenbrunnen)

        # show it actually added the time column
        df_mythenquai.info()
        df_mythenquai.info()

        return df_mythenquai, df_tiefenbrunnen
        
"""