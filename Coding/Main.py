#!/usr/bin/env
## See Shebang in Wikipedia!

import DB_Fill
import time
import Import_Data_API

if __name__ == '__main__':

    DB_Fill.DB_connect()
    DB_Fill.DB_clean()
    time.sleep(5)
    DB_Fill.DB_import_data()

