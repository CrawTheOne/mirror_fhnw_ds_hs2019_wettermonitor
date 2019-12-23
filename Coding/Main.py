import DB_Fill
import Import_Data_API
import config

DB_Fill.DB_clean()
DB_Fill.DB_start()
DB_Fill.DB_connect()
DB_Fill.DB_import_data()

Import_Data_API.DB_query_data(c)
