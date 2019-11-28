#dynamic host
#DB_HOST = subprocess.getoutput('hostname')
DB_HOST = 'localhost'
DB_PORT = 8086
DB_DBNAME = 'meteorology'
stations = ['mythenquai', 'tiefenbrunnen']

print(DB_HOST +":"+str(DB_PORT))