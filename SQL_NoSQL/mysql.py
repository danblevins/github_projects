#!/usr/bin/env python3
"""
The purpose of mysql.py is to connect to a MySQL database using Python.

:: Functions ::
    mysql(username, password)
        - username: Username for database
        - password: Password for database

Author(s): Dan Blevins
"""

import pymysql
import pandas as pd

def mysql(username, password):
    con = pymysql.connect(host='IP ADDRESS',
                            port=3306,
                            user=username,
                            password=password,
                            db='DB_NAME')

    sql = ("select * "
    "from table")

    return pd.read_sql(sql, con)

df = mysql('username', 'password')