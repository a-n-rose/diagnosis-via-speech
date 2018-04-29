'''
This script is suited to exctract features from .wav files that are in one or more folders within the cwd.  

There are 40 MFCCs, with 25ms window frames and 10ms shifts that are extracted.

The MFCCs will be saved to a database in the cwd via SQLite3 

note: to distinguish the differences of the files between the folders, the "label" (i.e. the input provided by the user) is combined with the file's folder name and saved in the database.

To go through all the 'dev', 'train', and 'test' folders, it took this program 36004.13554787636 seconds (10.001148763298989 hours) 

'''


 
import os, sys, tarfile
import numpy as np
import pandas as pd
import librosa
import glob
import sqlite3
import time



def parser(file,num_mfcc):
    y, sr = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=num_mfcc,hop_length=int(0.010*sr),n_fft=int(0.025*sr))
    return mfccs, sr

def get_save_mfcc(tgz_file,label,dirname,num_mfcc):
    label = label+"_"+dirname
    try:
        filename = os.path.splitext(tgz_file)[0]
        feature, sr = parser(filename+".wav",num_mfcc)
        columns = list((range(0,num_mfcc)))
        column_str = []
        for i in columns:
            column_str.append(str(i))
        feature_df = pd.DataFrame(feature)
        curr_db = pd.DataFrame.transpose(feature_df)
        curr_db.columns = column_str
        curr_db.insert(0,"file_name",filename)
        label = label+"_"+str(sr)
        curr_db["label"] = label
        x = curr_db.as_matrix()
        num_cols = 2+num_mfcc
        col_var = ""
        for i in range(num_cols):
            if i < num_cols-1:
                col_var+=' ?,'
            else:
                col_var+=' ?'
        c.executemany(' INSERT INTO mfcc_40 VALUES (%s) ' % col_var,x)
        conn.commit()   
    except Exception as e:
        print(e)



#initialize database
conn = sqlite3.connect('sp_mfcc.db')
c = conn.cursor()


label = input("Which category is this speech? ")
prog_start = time.time()
#specify number of mfccs --> reflects the number of columns
num_mfcc = 40
columns = list((range(0,num_mfcc)))
column_type = []
for i in columns:
    column_type.append('"'+str(i)+'" real')

try:    
    c.execute(''' CREATE TABLE IF NOT EXISTS mfcc_40(filename  text, %s, label text) ''' % ", ".join(column_type))
    conn.commit()
except Exception as e:
    print(e)


#collect directory names:
dir_list = []
for dirname in glob.glob('*/'):
    dir_list.append(dirname)
if len(dir_list) > 0:
    print("The directories found include: ", dir_list)
else:
    print("No directories found")


try:
    for j in range(len(dir_list)):
        directory = dir_list[j]
        os.chdir(directory)
        dirname = directory[:-1]
        print("Now processing the directory: "+dirname)
        files_list = []
        for wav in glob.glob('*.wav'):
            files_list.append(wav)
        if len(files_list) != 0:
            for i in range(len(files_list)):
                get_save_mfcc(files_list[i],label,dirname,num_mfcc)
                print("Progress: ", ((i+1)/(len(files_list)))*100,"%  (",dirname,": ",j+1,"/",len(dir_list)," directories)")
        else:
            print("No wave files found in ", dirname)
        os.chdir("..")
        print("The wave files in the "+ dirname + " directory have been processed successfully")
except Exception as e:
    print(e)

try:
    conn.commit()
    conn.close()
    print("MFCC data has been successfully saved!")
    print("All wave files have been processed")
    elapsed_time = time.time()-prog_start
    print("Elapsed time in seconds: ", elapsed_time)
except Exception as e:
    print(e)

