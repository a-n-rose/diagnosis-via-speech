'''
Script to extract .wav file from all .tgz in a directory(with a folder in it called 'wav'!!!), one at a time, 
to the Root/tmp/audio directory.

Input required: which language the speech data is.

Program will concatenate all .wav from one speaker (if there are multiple .wav files for one speaker)
Then will extract MFCC from that .wav

the MFCCs will be saved to a master database

the extracted files will then be deleted
'''

import os, sys, tarfile
import numpy as np
import pandas as pd
import librosa
import glob
from pydub import AudioSegment
import shutil
from shutil import rmtree


#'.' below means current directory
def extract(tar_url, extract_path='.'):
    print(tar_url)
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])
            
def parser(file):
    X, sample_rate = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    feature = mfccs
    return feature

    
def get_save_mfcc(tgz_file,label):
    try:
        try:
            sp_df1 = pd.read_csv("/tmp/audio/sp_df.csv")
        except:
            columns = list((range(0,40)))
            column_str = []
            for i in columns:
                column_str.append(str(i))
            sp_df1 = pd.DataFrame([],columns = ["speaker"]+column_str+["label",])
            print("Created new master dataframe")
        extract(tgz_file, extract_path = '/tmp/audio')
        filename = os.path.splitext(tgz_file)[0]
        wav_list = []
        for wav in glob.glob('/tmp/audio/'+filename+'/wav/*.wav'):
            wav_list.append(AudioSegment.from_wav(wav))
        if len(wav_list)>=1:
            comb_wav = sum(wav_list)
            comb_wav.export("/tmp/audio/"+filename+"/comb_wav.wav", format="wav")
        feature = parser("/tmp/audio/"+filename+"/comb_wav.wav")
        columns = list((range(0,40)))
        column_str = []
        for i in columns:
            column_str.append(str(i))
        curr_db = pd.DataFrame([feature], columns = column_str)
        curr_db.insert(0,"speaker",filename)
        curr_db["label"] = label
        #to ensure no additional columns are included (like "unnamed..."):
        sp_df = sp_df1[["speaker"]+column_str+["label"]]
        sp_df_new = sp_df.append(curr_db, ignore_index=True)
        sp_df_new.to_csv('/tmp/audio/sp_df.csv')
        print("Successfully updated master dataframe with ", filename)
        print("New dimensions of the master dataframe: ", sp_df_new.shape)        
        shutil.rmtree('/tmp/audio/'+filename)
        print("Extracted file "+filename+" removed!")
    except Exception as e:
        print(e)
    
#save all .tgz files to a list and turn into dataframe
#can apply my function to them much faster and effectively than with "for loop":
#.apply(lambda x: function(x))
files_list = []
for wav in glob.glob('*.tgz'):
    files_list.append(wav)
fl_df = pd.DataFrame(files_list)


label = input("What language category is this speech? ")
fl_df[0].apply(lambda x: get_save_mfcc(x,label))
