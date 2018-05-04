 
'''
script to see what databases are available, what tables those databases have, and get an idea of the data inside 
''' 

import sqlite3
from sqlite3 import Error
import pandas as pd
import time 
import numpy as np
import glob
import os
import tarfile

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


def table2dataframe(c,table,lim = None):
    try:
        if lim:
            limit = str(lim)
            c.execute("SELECT * FROM "+table+" LIMIT " + limit)
            data = c.fetchall()
            df = pd.DataFrame(data)
        else:
            c.execute("SELECT * FROM "+table)
            data = c.fetchall()
            df = pd.DataFrame(data)
        return df
    except Error as e:
        print(e)
    
    return None

db_list = []
for db in glob.glob('*.db'):
    db_list.append(db)
    
print("Available databases include: ", db_list)
database = input("Which database would you like to access? ")
if '.db' in database:
    database = database
else:
    database = database+'.db'
print("Connecting to database ",database)
conn = create_connection(database)
c = create_cursor(conn)
tables = list_tables(c)
print("The tables in this database include: ", tables)
table = input("In which table would you like to explore data? ")
print("How many rows would you like extracted? ")    
num_rows = input("Please insert an integer or 'all' if you don't want a limit: ")
#print("At which row would you like to start?") 
#row_start = input("Enter an integer (enter 0 to start from the top row): ")
if 'l' in num_rows:
    num_rows = None
df = table2dataframe(c,table,num_rows)
num_columns = df.shape[1]
realnum_cols = []
for col in range(num_columns):
    coltyp = str(type(df[col][0]))
    if 'float' in coltyp:
        realnum_cols.append(col)
class_col = input("Does the last column classify groups for the data? (yes, no): ")
if 'y' in class_col.lower():
    sep_classes = input("Would you like to apply data comparisons for each of these classes? (yes, no): ")
    if 'y' in sep_classes.lower():
        classes = list(set(df[num_columns-1]))
    else:
        classes = ['all data']
else:
    classes = ['all data']
if num_rows == None:
    num_rows = df.shape[0]
print("Data over the first ", num_rows, " rows in table ",table," from database ", database)    
print()
df_copy = df.copy()
df_copy2 = df_copy.copy()
for item in classes:
    stds = []
    ranges = []
    iqrs = []
    if item != 'all data':
        df_copy = df_copy2[df_copy2[num_columns-1]==item]
        print("Data from the class ",item)
    for column in realnum_cols:
        allcols = len(realnum_cols)
        stds.append((column,np.std(df_copy[column])))
        ranges.append((column,(max(df_copy[column])-min(df_copy[column]))))
        iqrs.append((column,np.subtract(*np.percentile(df_copy[column],[75,25]))))
    print("Standard deviation across each applicable column: ",stds)
    print("Range across each applicable column: ",ranges)
    print("Inter-quartile range across each applicable column: ",iqrs)
    print()
