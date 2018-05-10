#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 12:29:05 2018

@author: airos

Does a quick check of SQL databases and tables.
Input required.

"""

from checkSQL_db import Find_SQL_DB, Explore_SQL, Explore_Data



if __name__ == '__main__':
    
    dbs = Find_SQL_DB()
    dbs_list = dbs.db_list
    if dbs_list:
        database_entry = False
        while database_entry == False:
            print("\nAvailable Databases:\n",dbs.db_names,"\n")
            db_name = input("Which database would you like to explore?: ")
            if db_name in dbs_list:
                currdb = Explore_SQL(db_name)
                database_entry = True
            else:
                print("\n!! Database not found. Please choose from one of the available databases.\n")
        tables = currdb.tables2list()
        if tables:
            table_entry = False
            while table_entry == False:
                print("\nAvailable tables:\n")
                currdb.print_tables()
                table_name = input("Which table would you like to explore?: ")
                if table_name in tables:
                    df = currdb.table2dataframe(table_name)
                    currdf = Explore_Data(df)
                    table_entry = True
                else:
                    print("\n!! Table does not exist.\n")
            currdf.print_profile(table_name)
            if currdf.depvar_numunique > 1:
                incorrect_input = True
                while incorrect_input == True:
                    examfurth = input("\nWould you like to explore the data belonging to one of the dependent variables? (yes or no): ")
                    if 'yes' or 'no' in examfurth.lower():
                        incorrect_input = False
                    else: 
                        print("\nPlease enter 'yes' or 'no'\n")
                if 'yes' in examfurth.lower():
                    cont_explore = True
                    while cont_explore == True:
                        print("\nDependent variables to explore: \n",currdf.depvar,"\n")
                        spec_dv = input("\nWhich dependent variable are you interested in?: ")
                        if spec_dv in currdf.depvar:
                            try:
                                currdf.print_profile(table_name,spec_dv)
                            except Exception as e:
                                print(e)
                            expmore = input("\nWould you like to explore another dependent variable? (yes or no): ")
                            if 'no' in expmore.lower():
                                cont_explore = False
                    else:
                        print("")
        else:
            print("\n!! No tables found in database\n")
    else:
        print("\n!! No databases found\n")
