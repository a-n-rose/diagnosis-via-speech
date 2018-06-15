#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: airos

Does a quick check of SQL databases and tables.
Compares data by looking at each column's standard deviation, range, and inter-quartile range (if columns include floats)
Can also compare data depending on dependent variables.
Input required.

requires 'checkSQL_db.py' and 'checkSQL_UserFun.py' to be in same working directory
"""

from checkSQL_bigdata_db import Find_SQL_DB, Explore_SQL, Explore_Data, User_Input
from checkSQL_UserFun import show_options, getDataCont_Name, stop_OR_go, no_items
    
if __name__ == '__main__':
    try:
        
        #Search cwd for .db files 
        dbs = Find_SQL_DB()
        if dbs.item_list:
            while dbs.stop == False:
                
                #Presents User with Databases to choose from
                show_options(dbs)
                db_input = User_Input()
                db_name = getDataCont_Name(db_input,dbs)
                currdb = Explore_SQL(db_name)
                
                #Finds tables in the chosen Database
                tables = currdb.tables2list()
                if tables:
                    while currdb.stop == False:
                        
                        #Presents User with Tables to choose from
                        show_options(currdb)
                        table_input = User_Input()
                        table_name = getDataCont_Name(table_input,currdb)
                        colnames = currdb.get_column_names(table_name)
                        print(colnames)
                        currdb.apply_col_index(table_name,'label','depvar_label')
                        df = currdb.table2dataframe(table_name)
                        currdf = Explore_Data(df)
                        #Shows User the table columns, dependent variables, and 
                        #standard deviation, range, and inter-quartile range of columns with floats
                        currdf.print_profile(table_name)
                        
                        #If there are more than 1 dependent variables
                        if currdf.depvar_numunique == 1:
                            currdf.stop = True
                        while currdf.stop == False:
                            
                            #Ask User if they would like to look at the data of one of the variables
                            yes_no = stop_OR_go(currdf.datacont_type)
                            if 'no' in yes_no:
                                currdf.stop = True
                            else:
                                #Present User with Variables to choose from
                                show_options(currdf)
                                dv_input = User_Input()
                                dv_name = getDataCont_Name(dv_input,currdf)
                                if dv_input.stop == True:
                                    #Shows User the data pertaining to only the specified dependent variable
                                    currdf.print_profile(table_name, dv_name)        
                        
                        #If there is only 1 table in the database, exit while statement
                        if len(tables) == 1:
                                currdb.stop = True
                        else:
                            #Ask User if they would like to look at another table
                            yes_no = stop_OR_go(currdb.datacont_type)
                            if 'no' in yes_no:
                                currdb.stop = True
                #If no tables found in database, let User know
                else:
                    no_items('tables','database')
                
                #If only 1 database, exit while statement (and program)
                if len(dbs.item_list) == 1:
                    dbs.stop = True
                #Otherwise, ask User if they would like to look in another database
                else:
                    yes_no = stop_OR_go(dbs.datacont_type)
                    if 'no' in yes_no:
                        dbs.stop = True
        #If no .db files found, let User know
        else:
            no_items('databases','directory')
        #Close sqlite3 connection without committing: just to make sure no changes that might somehow be made get saved
        currdb.close_conn_NOsave()
    except Exception as e:
        print(e)
    finally:
        if currdb.conn:
            currdb.close_conn_NOsave()
            print("Database closed.")
