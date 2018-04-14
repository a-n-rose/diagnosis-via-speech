'''
This script is suited to exctract features from .wav files that are in one or more folders within the cwd.  

There are 13 MFCCs, with 25ms window frames and 10ms shifts that are extracted.

The MFCCs will be saved to a master database in a pickel file first and then to a .csv in the cwd

note: to distinguish the differences of the files between the folders, the "label" (i.e. the input) is 
combined with the file's folder name and saved in the database.
'''


 
import os, sys, tarfile
import numpy as np
import pandas as pd
import librosa
import glob
from pydub import AudioSegment


import _pickle as cpickle

#necessary information to discern between languages:
# 1) filename
# 2) label of speech (English/German; female/male; etc)


def load(path = None):
    if path:
        df = cpickle.load( open(path+"sp_df.pkl","rb"))
    else:
        df = cpickle.load( open("sp_df.pkl","rb"))
    return df

def update(df, path = None):
    if path: 
        cpickle.dump(df, open(path+"sp_df.pkl","wb"))
    else:
        cpickle.dump( df, open("sp_df.pkl","wb"))  

            
def parser(file):
    y, sr = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=13,hop_length=int(0.010*sr),n_fft=int(0.025*sr))
    return mfccs

    
def get_save_mfcc(tgz_file,label,dirname):
    sp_df1 = load('../')
    label = label+"_"+dirname
    try:
        filename = os.path.splitext(tgz_file)[0]
        print("Filename saved")
        print(filename)
        print("Extracting MFCC / features")
        feature = parser(filename+".wav")
        print("MFCCs have been extracted")
        print("Creating dataframe for the speaker's MFCC data")
        columns = list((range(0,13)))
        column_str = []
        for i in columns:
            column_str.append(str(i))
        feature_df = pd.DataFrame(feature)
        curr_db = pd.DataFrame.transpose(feature_df)
        curr_db.columns = column_str
        curr_db.insert(0,"file_name",filename)
        curr_db["label"] = label
        #to ensure no additional columns are included (like "unnamed..."):
        sp_df = sp_df1[["file_name"]+column_str+["label"]]
        print("Created new dataframe with extracted MFCC data")
        print("Dimensions of current dataframe are: ", curr_db.shape)
        print("Dimensions of master dataframe are: ", sp_df.shape)
        print("Appending current speaker's MFCC data to master dataframe")
        sp_df_new = sp_df.append(curr_db, ignore_index=True)
        print("Successfully appended new data")
        print("Saving appended dataframe to pickel file")
        update(sp_df_new,'../')
        print("Successfully updated master dataframe!")
    except Exception as e:
        print(e)

label = input("Which category is this speech? ")
    
dir_list = []
for dirname in glob.glob('*/'):
    dir_list.append(dirname)

try:
    sp_df1 = pd.read_csv("sp_df.csv")
    print("here is the length of the dataframe: ", len(sp_df1))
    update(sp_df1)
except:
    columns = list((range(0,13)))
    column_str = []
    for i in columns:
        column_str.append(str(i))
    sp_df1 = pd.DataFrame([],columns = ["file_name"]+column_str+["label"])
    print("Created new master dataframe")
    update(sp_df1)

try:
    for directory in dir_list:
        os.chdir(directory)
        dirname = directory[:-1]
        print(dirname)
        files_list = []
        for wav in glob.glob('*.wav'):
            files_list.append(wav)
        fl_df = pd.DataFrame(files_list)
        fl_df[0].apply(lambda x: get_save_mfcc(x,label,dirname))
        os.chdir("..")
except Exception as e:
    print(e)

try:
    df = load()
    print("data has been collected. Now saving to .csv")
    df.to_csv('sp_df.csv')
    print("data has been successfully saved!")
except Exception as e:
    print(e)
