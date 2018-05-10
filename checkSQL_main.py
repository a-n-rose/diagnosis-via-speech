#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 12:29:05 2018

@author: airos

Does a quick check of SQL databases and tables.
Can compare depending on categories (i.e. dependent variable)
Input required.

"""

from checkSQL_db import Find_SQL_DB, Explore_SQL, Explore_Data

class Error_Msg:
    def __init__(self):
        self.msg = 'ERROR!'
        self.att = "\n"+('!*'*20)+"\n"
        
def str2index(int_string,items_list):
    try:
        ind = int(int_string)-1
        if ind >= 0:
            requested_item = items_list[ind]
            return(requested_item,True)
        else:
            print("\nPlease enter an integer between 1 and "+str(len(items_list)))
    except ValueError as ve:
        print(Error_Msg().att)
        print(ve)
        print("\nValue must be an integer\n".upper())
    except IndexError as ie:
        print(Error_Msg().att)
        print(ie)
        if len(items_list) > 1:
            err_msg = "\nPlease enter an integer between 1 and "+str(len(items_list))
        else:
            err_msg = "\nPlease enter '1' if you would like to continue"
        print(err_msg.upper())
        print(Error_Msg().att)
    return None, False
        
    
    
if __name__ == '__main__':
    
    dbs = Find_SQL_DB()
    dbs_list = dbs.db_list
    if dbs_list:
        database_entry = False
        print("\nAvailable Databases:")
        for db in range(len(dbs_list)):
            print("{}) ".format(db+1), dbs_list[db])
        print("\nWhich database would you like to explore?")
        while database_entry == False:
            db_num = input("Please enter the number corresponding to the database: ")
            db_name, database_entry = str2index(db_num,dbs_list)
        currdb = Explore_SQL(db_name)
        tables = currdb.tables2list()
        if tables:
            table_entry = False
            print("\nAvailable tables:\n")
            for i in range(len(tables)):
                print("{}) ".format(i+1),tables[i])
            print("\nWhich table would you like to explore?")
            while table_entry == False:
                table_num = input("Please enter the number corresponding to the table: ")
                table_name, table_entry = str2index(table_num,tables)
            df = currdb.table2dataframe(table_name)
            currdf = Explore_Data(df)
            currdf.print_profile(table_name)
            if currdf.depvar_numunique > 1:
                cont_explore = False
                while cont_explore == False:
                    
                    examfurth = input("\nWould you like to explore data from a particular dependent variable? (yes or no): ")
                    if 'no' in examfurth.lower():
                        break
                    elif 'yes' in examfurth.lower():
                        cont_explore = True
                    else: 
                        print("\nPlease enter 'yes' or 'no'\n")           
                dv_list = list(currdf.depvar)
                pause_explore = False
                while pause_explore == False:
                    print("\nDependent variables to explore: \n")
                    for dv in range(len(dv_list)):
                        print("{}) ".format(dv+1),dv_list[dv])    
                    print("\nWhich dependent variable are you interested in?: ")
                    dv_num = input("Please enter the number corresponding to the variable: ")
                    dv_name, pause_explore = str2index(dv_num,dv_list)
                    if pause_explore == True:
                        currdf.print_profile(table_name, dv_name)
                    again = False
                    while again == False and pause_explore == True:
                        expmore = input("\nWould you like to explore another dependent variable? (yes or no): ")
                        if 'no' in expmore.lower():
                            pause_explore = True
                            break
                        elif 'yes' in expmore.lower():
                            again = True
                            pause_explore = False
                        else:
                            print("\nPlease enter 'yes' or 'no'\n")
                
        else:
            print("\n!! No tables found in database\n")
    else:
        print("\n!! No databases found\n")
