'''
script to get the MFCCs from all .wav files in same directory. The MFCCs will be saved to a master database.
'''

import os
import tarfile
import numpy as np
import pandas as pd
import librosa
import glob
            
def parser(file):
    X, sample_rate = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    feature = mfccs
    return feature

def get_save_mfcc(tgz_file,label):
    try:
        try:
            sp_df1 = pd.read_csv("/tmp/audio/sp_df.csv")
            print(len(sp_df1))
        except:
            columns = list((range(0,40)))
            column_str = []
            for i in columns:
                column_str.append(str(i))
            sp_df1 = pd.DataFrame([],columns = ["speaker"]+column_str+["label",])
            #print("Created new master dataframe")
        #print("Extracting tgz file: ",tgz_file)
        #extract(tgz_file, extract_path = '/tmp/audio')
        #print("Finished extracting")
        #print("Saving speaker's filename")
        filename = os.path.splitext(tgz_file)[0]
        #print("Speaker's filename saved")
        #print(filename)
        #print("Extracting MFCC / features")
        feature = parser(filename+".wav")
        #print("MFCCs have been extracted")
        #print(feature)
        #print("type of MFCC data object: ",type(feature))
        #print("Creating dataframe for the speaker's MFCC data")
        columns = list((range(0,40)))
        column_str = []
        for i in columns:
            column_str.append(str(i))
        curr_db = pd.DataFrame([feature], columns = column_str)
        curr_db.insert(0,"speaker",filename)
        curr_db["label"] = label
        #to ensure no additional columns are included (like "unnamed..."):
        sp_df = sp_df1[["speaker"]+column_str+["label"]]
        #print("Created new dataframe with extracted MFCC data")
        #print("Dimensions of current dataframe are: ", curr_db.shape)
        #print("Dimensions of master dataframe are: ", sp_df.shape)
        #print("Appending current speaker's MFCC data to master dataframe")
        sp_df_new = sp_df.append(curr_db, ignore_index=True)
        print("Successfully appended new data")
        print("Saving appended dataframe to csv")
        sp_df_new.to_csv('/tmp/audio/sp_df.csv')
        print("Successfully updated master dataframe!")
    except Exception as e:
        print(e)   

files_list = []
for wav in glob.glob('*.wav'):
    files_list.append(wav)
fl_df = pd.DataFrame(files_list)

label = input("What language category is this speech? ")
fl_df[0].apply(lambda x: get_save_mfcc(x,label))
