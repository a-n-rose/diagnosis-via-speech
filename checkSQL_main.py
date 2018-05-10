#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 12:29:05 2018

@author: airos

Does a quick check of SQL databases and tables.
Input required.

"""

from checkSQL_db import Find_SQL_DB, Explore_SQL, Explore_Data

class Error_Msg:
    def __init__(self):
        self.msg = 'ERROR!'
        self.att = "\n"+('!*'*20)+"\n"
    
if __name__ == '__main__':
    int_ValError = Error_Msg()
    int_ValError.msg = "\nValue must be an integer\n"
    index_Error = Error_Msg()
    gen_Error = Error_Msg()
    
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
            try:
                db_ind = int(db_num)-1
                db_name = dbs_list[db_ind]
                currdb = Explore_SQL(db_name)
                database_entry = True
            except ValueError as ve:
                print(int_ValError.att)
                print(ve)
                print(int_ValError.msg.upper())
            except IndexError as ie:
                print(index_Error.att)
                print(ie)
                if len(dbs_list) > 1:
                    err_msg = "\nPlease enter an integer between 1 and "+str(len(dbs_list))
                    print(err_msg.upper())
                else: 
                    err_msg = "\nPlease enter '1' if you would like to continue"
                    print(err_msg.upper())
                print(index_Error.att)
                
        tables = currdb.tables2list()
        if tables:
            table_entry = False
            print("\nAvailable tables:\n")
            for i in range(len(tables)):
                print("{}) ".format(i+1),tables[i])
            print("\nWhich table would you like to explore?")
            while table_entry == False:
                table_num = input("Please enter the number corresponding to the table: ")
                
                try:
                    table_ind = int(table_num)-1
                    table_name = tables[table_ind]
                    df = currdb.table2dataframe(table_name)
                    currdf = Explore_Data(df)
                    table_entry = True
                except ValueError as ve:
                    print(int_ValError.att)
                    print(ve)
                    print(int_ValError.msg.upper())
                except IndexError as ie:
                    print(index_Error.att)
                    print(ie)
                    if len(tables) > 1:
                        err_msg = "\nPlease enter an integer between 1 and "+str(len(tables))
                        print(err_msg.upper())
                    else: 
                        err_msg = "\nPlease enter '1' if you would like to continue"
                        print(err_msg.upper())
                    print(index_Error.att)
    
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
                while cont_explore == True:
                    print("\nDependent variables to explore: \n")
                    dv_list = list(currdf.depvar)
                    for dv in range(len(dv_list)):
                        print("{}) ".format(dv+1),dv_list[dv])    
                    print("\nWhich dependent variable are you interested in?: ")
                    dv_num = input("Please enter the number corresponding to the variable: ")
                    
                    try:
                        dv_ind = int(dv_num)-1
                        dv_name = dv_list[dv_ind]
                        currdf.print_profile(table_name,dv_name)
                        again = False
                        while again == False:
                            expmore = input("\nWould you like to explore another dependent variable? (yes or no): ")
                            if 'no' in expmore.lower():
                                cont_explore = False
                                break
                            elif 'yes' in expmore.lower():
                                again = True
                            else:
                                print("\nPlease enter 'yes' or 'no'\n")
                                
                    except ValueError as ve:
                        print(int_ValError.att)
                        print(ve)
                        print(int_ValError.msg.upper())
                    except IndexError as ie:
                        print(index_Error.att)
                        print(ie)
                        err_msg = "\nPlease enter an integer between 1 and "+str(len(dv_list))
                        print(err_msg.upper())
                        print(index_Error.att)
                
        else:
            print("\n!! No tables found in database\n")
    else:
        print("\n!! No databases found\n")
