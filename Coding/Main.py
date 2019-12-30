#!/usr/bin/env
## See Shebang in Wikipedia!


import config as cfg
import DB_Fill
import Import_Data_API

if __name__ == '__main__':

    DB_Fill.DB_start()
    DB_Fill.DB_connect()
    DB_Fill.DB_clean()
    DB_Fill.DB_import_data()



