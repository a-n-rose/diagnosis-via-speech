'''
script to see what tables are in the database of interest, as well as the first several rows in whichever tables
'''

import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None

def create_cursor(conn):
    try:
        return conn.cursor()
    except Error as e:
        print(e)

def list_tables(c):
    try:
        c.execute("SELECT * FROM sqlite_master WHERE type='table';")
        return(c.fetchall())
    except Error as e:
        print(e)
        
    return None


def table2dataframe(c,table,lim = 10):
    try:
        limit = str(lim)
        c.execute("SELECT * FROM "+table+" LIMIT " + limit)
        data = c.fetchall()
        df = pd.DataFrame(data)
        return df
    except Error as e:
        print(e)
    
    return None

conn = create_connection('sp_mfcc.db')
c = create_cursor(conn)
tables = list_tables(c)
print(tables)
df_eng = table2dataframe(c,'mfcc13_English',15)
df_germ = table2dataframe(c,'mfcc_13',15)
print(df_eng)
print(df_germ)
