#!/usr/bin/env
## See Shebang in Wikipedia!
import DB_Fill
import time

if __name__ == '__main__':

    DB_Fill.DB_connect()
    DB_Fill.DB_clean()
    #time.sleep(10)
    DB_Fill.DB_import_historic_data()
    DB_Fill.DB_import_latest_data()



