import sqlite3
from sqlite3 import Error
import pandas as pd
import time 
import numpy as np
import glob
import os
import tarfile

##what I would like to be able to get from a class method
#self.list_tables(done)
#self.depvar_type
#self.depvar_numunique
#self.columns (done)
#self.indvar_type 
#self.calc_std (done)
#self.calc_iqr (done)
#self.calc_range (done)

class Explore_SQL:
    def __init__(self,db_name):
        self.database = db_name
        self.conn = sqlite3.connect(db_name)
        self.c = sqlite3.connect(db_name).cursor()
        self.tables = "Not yet defined"
        
    def list_tables(self):
        try:
            self.c.execute("SELECT * FROM sqlite_master WHERE type='table';")
            return(self.c.fetchall())
        except Error as e:
            print(e)
            
        return None
    
    def table2dataframe(self,table,lim=None):
        try: 
            if lim:
                limit = str(lim)
                self.c.execute("SELECT * FROM "+table+" LIMIT " + limit)
            else:
                self.c.execute("SELECT * FROM "+table)
            data = self.c.fetchall()
            df = pd.DataFrame(data)
            return(df)
        except Error as e:
            print(e)
        
        return None
    
class Explore_Data:
    def __init__(self,df):
        self.dataframe = df
        self.columns = df.columns.get_values()
        self.num_rows = len(df)
        self.depvar_type = "Not yet defined"
        self.depvar_numunique = "Not yet defined"
        
    def calc_std(self):
        data_std = [(col,np.std(self.dataframe[col])) for col in range(len(self.columns)) if isinstance(self.dataframe[col][0],float)]
        return(data_std)
        
    def calc_range(self):
        data_range = [(col,(max(self.dataframe[col])-min(self.dataframe[col]))) for col in range(len(self.columns)) if isinstance(self.dataframe[col][0],float)]
        return(data_range)
    
    def calc_iqr(self):
        data_iqr = [(col,np.subtract(*np.percentile(self.dataframe[col],[75,25]))) for col in range(len(self.columns)) if isinstance(self.dataframe[col][0],float)]
        return(data_iqr)
                     
                                
            
curr_db = Explore_SQL('sp_mfcc.db')
curr_db.database
curr_db.depvar_type
curr_db.depvar_numunique




tables = curr_db.list_tables()
table1 = tables[0][1]
table2 = tables[1][1]
tab1 = curr_db.table2dataframe(table1,lim=100)
tab2 = curr_db.table2dataframe(table2,lim=100)
tab1
tab2



tab1_df = Explore_Data(tab1)
tab1_df.dataframe
tab1_df.calc_std()
tab1_df.calc_range()
tab1_df.calc_iqr()
tab2_df = Explore_Data(tab2)
tab2_df.dataframe
tab2_df.calc_std()
tab2_df.calc_range()
tab2_df.calc_iqr()
