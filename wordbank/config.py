# config.py

import os
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Pranjal'
    MYSQL_DB = 'wordbank_db'
    SECRET_KEY = os.urandom(24)
