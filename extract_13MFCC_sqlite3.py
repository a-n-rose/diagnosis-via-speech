'''
This script is suited to exctract features from .wav files that are in one or more folders within the cwd.  

There are 13 MFCCs collected, which have 25ms window frames with 10ms shifts.

The MFCCs will be saved to a database in the cwd via SQLite3 

note: to distinguish the differences of the files between the folders, the "label" (i.e. the input provided by the user) 
is combined with the file's folder name and saved in the database under the "label" column.

The number of MFCCs reflect the number of columns in the database, plus 2 for the filename and the label.
'''


 
import os, sys, tarfile
import numpy as np
import pandas as pd
import librosa
import glob
import sqlite3


def parser(file,num_mfcc):
    y, sr = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=num_mfcc,hop_length=int(0.010*sr),n_fft=int(0.025*sr))
    return mfccs

def get_save_mfcc(tgz_file,label,dirname,num_mcff):
    label = label+"_"+dirname
    try:
        filename = os.path.splitext(tgz_file)[0]
        print("Filename documented")
        print(filename)
        print("Extracting MFCC / features")
        feature = parser(filename+".wav",num_mcff)
        print("MFCCs have been extracted")
        print("Creating dataframe for the speaker's MFCC data")
        columns = list((range(0,num_mfcc)))
        column_str = []
        for i in columns:
            column_str.append(str(i))
        feature_df = pd.DataFrame(feature)
        curr_db = pd.DataFrame.transpose(feature_df)
        curr_db.columns = column_str
        curr_db.insert(0,"file_name",filename)
        curr_db["label"] = label
        x = curr_db.as_matrix()
        num_cols = 2+num_mfcc
        print(num_cols)
        col_var = ""
        for i in range(num_cols):
            if i < num_cols-1:
                col_var+=' ?,'
            else:
                col_var+=' ?'
        print()
        c.executemany(' INSERT INTO mfcc VALUES (%s) ' % col_var,x)
        conn.commit()   
        print("The mfccs were sucessfully saved to the database")
    except Exception as e:
        print(e)



#initialize database
conn = sqlite3.connect('sp_mfcc.db')
c = conn.cursor()


label = input("Which category is this speech? ")

#specify number of mfccs --> reflects the number of columns
num_mfcc = 13
columns = list((range(0,num_mfcc)))
column_type = []
for i in columns:
    column_type.append('"'+str(i)+'" real')

try:    
    c.execute(''' CREATE TABLE IF NOT EXISTS mfcc_13(filename  text, %s, label text) ''' % ", ".join(column_type))
    c.commit()
except Exception as e:
    print(e)


  
dir_list = []
for dirname in glob.glob('*/'):
    dir_list.append(dirname)


try:
    for directory in dir_list:
        os.chdir(directory)
        dirname = directory[:-1]
        print("Now processing wave files in the directory: "+dirname)
        files_list = []
        for wav in glob.glob('*.wav'):
            files_list.append(wav)
        fl_df = pd.DataFrame(files_list)
        print("Number of wave files to process: ",len(fl_df))
        fl_df[0].apply(lambda x: get_save_mfcc(x,label,dirname,num_mfcc))
        os.chdir("..")
        print("The Wave files in the "+ directory + " directory have been processed successfully")
except Exception as e:
    print(e)

try:
    conn.commit()
    conn.close()
    print("MFCC data has been successfully saved!")
    print("All wave files have been processed")
except Exception as e:
    print(e)
