'''
This script is suited to exctract features from .wav files that are in one or more folders within the cwd.  

There are 13 MFCCs, with 25ms window frames and 10ms shifts that are extracted.

The MFCCs will be saved to a database "sp_mfcc.db" in the cwd via SQLite3, in a table named "mfcc_13" 
**if the num_mfcc is changed, be sure to change the name of the table from mfcc_13 to whatever name you'd like.
**the number of columns of that table corresponds to 13 coefficients, +2 for the filename and label columns.

note: to distinguish the differences of the files between the folders, the "label" (i.e. the input provided by the user) 
is combined with the file's folder name and saved in the database.

time: to process all the Voxforge German files in the 'test','dev', and 'train' directories, it took  34523.29967880249 seconds 
(or 9.5897222222222 hours) 
'''
import os
import pandas as pd
import librosa
import glob
import sqlite3
import time

def parser(file,num_mfcc):
    y, sr = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=num_mfcc,hop_length=int(0.010*sr),n_fft=int(0.025*sr))
    return mfccs

def get_save_mfcc(file,label,dirname,num_mfcc):
    label = label+"_"+dirname
    try:
        filename = os.path.splitext(file)[0]
        feature = parser(filename+".wav",num_mfcc)
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
        c.executemany(' INSERT INTO mfcc_13 VALUES (%s) ' % col_var,x)
        conn.commit()   
    except Exception as e:
        print(e)
        
#initialize database
conn = sqlite3.connect('sp_mfcc.db')
c = conn.cursor()

label = input("Which category is this speech? ")
prog_start = time.time()
#specify number of mfccs --> reflects the number of columns
num_mfcc = 13
columns = list((range(0,num_mfcc)))
column_type = []
for i in columns:
    column_type.append('"'+str(i)+'" real')

try:    
    c.execute(''' CREATE TABLE IF NOT EXISTS mfcc_13(filename  text, %s, label text) ''' % ", ".join(column_type))
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
        if len(files_list) == 0:
            print("No wave files found in ", dirname)
        for i in range(len(files_list)):
            get_save_mfcc(files_list[i],label,dirname,num_mfcc)
            print("Progress: ", (i/(len(files_list)-1))*100,"%  (",dirname,": ",j+1,"/",len(dir_list)," directories)")
        os.chdir("..")
        print("The Wave files in the "+ dirname + " directory have been processed successfully")
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
