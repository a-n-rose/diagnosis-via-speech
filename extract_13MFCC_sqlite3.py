'''
This script is suited to exctract features from .wav files that are in one or more folders within the cwd.  

There are 13 MFCCs, with 25ms window frames and 10ms shifts that are extracted.

The MFCCs will be saved to a database in the cwd via SQLite3. The progress is printed by tqdm.

note: to distinguish the differences of the files between the folders, the "label" 
(i.e. the input provided by the user) is combined with the file's folder name and saved in the database.
'''


 
import os, sys, tarfile
import numpy as np
import pandas as pd
import librosa
import glob
import sqlite3

from tqdm import tqdm, tqdm_pandas


def parser(file,num_mfcc):
    y, sr = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=num_mfcc,hop_length=int(0.010*sr),n_fft=int(0.025*sr))
    return mfccs

def get_save_mfcc(tgz_file,label,dirname,num_mcff,tot_wav):
    label = label+"_"+dirname
    try:
        filename = os.path.splitext(tgz_file)[0]
        feature = parser(filename+".wav",num_mcff)
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
        col_var = ""
        for i in range(num_cols):
            if i < num_cols-1:
                col_var+=' ?,'
            else:
                col_var+=' ?'
        print()
        c.executemany(' INSERT INTO mfcc VALUES (%s) ' % col_var,x)
        conn.commit()   
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


#collect directory names:
dir_list = []
for dirname in glob.glob('*/'):
    dir_list.append(dirname)
if len(dir_list) > 0:
    print("The directories found include: ", dir_list)
else:
    print("No directories found")


try:
    for directory in dir_list:
        os.chdir(directory)
        dirname = directory[:-1]
        print("Now processing the directory: "+dirname)
        files_list = []
        for wav in glob.glob('*.wav'):
            files_list.append(wav)
        fl_df = pd.DataFrame(files_list)
        tot_wav = len(fl_df)
        if tot_wav == 0:
            print("No wave files found in ",dirname)
        print("Number of wave files to process: ",tot_wav)
        print("Progress:")
        tqdm.pandas(ncols=1)
        fl_df[0].progress_apply(lambda x: get_save_mfcc(x,label,dirname,num_mfcc,tot_wav))
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
