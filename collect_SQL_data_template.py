import sqlite3
from sqlite3 import Error
import pandas as pd
from pandas.api.types import is_string_dtype
import numpy as np
import glob


def does_db_exist(db_filename):
    db_list = [db for db in glob.glob('*.db')]
    if db_filename in db_list:
        return True
    return False


class Extract_Data:
    def __init__(self,db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
    
    def get_depvar_colname(self, table):
        self.c.execute("PRAGMA table_info({})".format(table))
        cols = self.c.fetchall()
        #assumes dependent variable is the last column
        depvarcolumn = cols[-1][1]
        return(depvarcolumn)
    
    
    def does_row_exist(self,table,row_num):
        try:
            self.c.execute("SELECT * FROM {} WHERE rowid = {}".format(table,row_num))
            row = self.c.fetchall()
            if row:
                return True
            else:
                return False

        except OperationalError as oe:
            print(oe)
            print("Check your input")
           
        return None
    
    
    def does_var_exist(self,table,column,variable):
        try:
            self.c.execute("SELECT * FROM "+table+" WHERE "+column+" = '"+variable+"' LIMIT 1")
            data = self.c.fetchall()
            print(data)
            if data:
                return True
        except Error as e:
            print(e)
        return None
    
    
    def collect_data(self, table,column, variable,row_start,row_lim):
        try:
            if self.does_var_exist(table,column,variable):
                row_start = str(row_start)
                limit = str(row_lim)
                max_row = str(int(row_start)+int(row_lim))
                if self.does_row_exist(table,max_row):
                    self.c.execute("SELECT * FROM "+table+" WHERE label = '"+variable+"' LIMIT "+row_start+", "+limit)
                    data = self.c.fetchall()
                    df = pd.DataFrame(data)
                    return(df)
                else:
                    print("Error: Not sufficient number of rows.")
            else:
                print("Error: Variable not found")
        except Error as e:
            print(e)
            print("Data could not be collected")
        
        return None
    
    def reduce_df(self, df,num_cols):
        #add 1 column if first column has strings (i.e. filenames, not mfcc data)
        if is_string_dtype(df[df.columns[0]]):
            num_cols += 1
        cols_red = [i for i in range(num_cols)]
        df_red = df[cols_red]
        df_var = df[df.columns[-1]]
        df_red = pd.concat([df_red,df_var],axis=1)
        return df_red
    
    def label2int(self,df,langint_dict):
        for key in langint_dict:
            if langint_dict[key].lower() in df.iloc[0][-1].lower():
                df[df.columns[-1]] = key
                return df
        return None
    
    def prep_df(self,table,column,variable,row_start,row_lim,num_cols,langint_dict):
        if self.does_var_exist(table,column,variable):
            df = self.collect_data(table,column,variable,row_start,row_lim)
            #Note: +2 for filename and dependent variable columns
            if len(df.columns) > num_cols+2:
                df = self.reduce_df(df,num_cols)
            #turn dependent variable (i.e. last column) into integer classifier
            df = self.label2int(df,langint_dict)
            return df
        return None
        

    def get_startcol(self,matrix,include_1stMFCC):
        startcol = 0
        if isinstance(matrix[0][0],str):
            startcol += 1
        if include_1stMFCC == False:
            startcol+= 1
        return startcol
        
    
    def get_dfcols(df):
        cols = np.arange(df.shape[1])
        return cols
    
    def close_conn_NOcommit(self):
        if self.conn:
            self.conn.close()
            print('Database successfully closed')
        return None
       
    def close_conn_commit(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("Database successfully updated and closed")
        return None
