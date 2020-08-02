#!/usr/bin/env python3
"""
The purpose of oracle.py is to connect to a SQL Oracle database using Python.

:: Functions ::
    mysql(username, password)
        - username: Username for database
        - password: Password for database

Author(s): Dan Blevins
"""

import cx_Oracle
import pandas as pd
import numpy as np

def oracle(username, password):
    ip = 'ADDRESS'
    port = 'PORT'
    db = 'DB_NAME'
    dsn_tns = cx_Oracle.makedsn(ip, port, service_name=db)
    con = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns, encoding = "UTF-8")

    sql = ("select * "
    "from table")

    return pd.read_sql(sql, con)

df = oracle('username', 'password')