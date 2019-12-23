#dynamic host
#DB_HOST = subprocess.getoutput('hostname')
import pandas as pd
DB_HOST = 'localhost'
DB_PORT = 8086
DB_DBNAME = 'meteorology'
stations = ['mythenquai', 'tiefenbrunnen']

print(DB_HOST +":"+str(DB_PORT))

days_delta = 365

start_time = '2019-10-01T00:00:00+00:00'
end_time = '2019-11-28T00:00:00+00:00'


class connection:

    def __init__(self, name):
        self.name = name

    def change_name(self, new_name):
        self.name = new_name