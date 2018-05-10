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
    try:
        dbs = Find_SQL_DB()
        dbs_list = dbs.db_list
        if dbs_list:
            database_entry = False
            while database_entry == False:
                print("\n Available Databases: \n",dbs.db_names,"\n")
                db_name = input("Which database would you like to explore? ")
                if db_name in dbs_list:
                    currdb = Explore_SQL(db_name)
                    database_entry = True
                else:
                    print()
                    print("!! Database not found. Please choose from one of the available databases.")
            tables = currdb.tables2list()
            if tables:
                table_entry = False
                while table_entry == False:
                    print()
                    print("Available tables: \n")
                    currdb.print_tables()
                    table_name = input("Which table would you like to explore?: ")
                    if table_name in tables:
                        df = currdb.table2dataframe(table_name)
                        currdf = Explore_Data(df)
                        table_entry = True
                    else:
                        print()
                        print("!! Table does not exist.")
                print()
                print('#'*80,'\n')
                print("SQL table '",table_name,"' profile: \n")
                print("Columns: \n", currdf.columns)
                currdf.explore_depvar()
                print()
                print("Dependent Variable type: \n", currdf.depvar_type,"\n")
                print("Number of dependent variables: \n", currdf.depvar_numunique,"\n")
                print("Dependent Variable(s): \n",currdf.depvar,"\n")
                print("Standard deviation of applicable columns: \n",currdf.calc_std(),"\n")
                print("Range of applicable columns: \n", currdf.calc_range(),"\n")
                print("Inter-quartile Range of applicable columns: \n",currdf.calc_iqr(),"\n")
                print('#'*80)
            else:
                print()
                print("!! No tables found in database")
        else:
            print()
            print("!! No databases found")
    except Exception as e:
        print(e)
