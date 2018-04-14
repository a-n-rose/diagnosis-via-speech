'''
If you downloaded the .tgz files with wget
change your directory to: 

$ cd www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Original

This will collect all the folder names, and within each folder, extract one by one each .tgz file in /tmp/audio, get MFCCs in 25ms frames with window shifts of 10ms, save them to database in the directory where this script is, then delete the extracted files in the tmp dir.
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
    y, sr = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=13,hop_length=int(0.010*sr),n_fft=int(0.025*sr))
    return mfccs
    
def get_save_mfcc(tgz_file,label):
    try:
        try:
            sp_df1 = pd.read_csv("../sp_df.csv")
            print(len(sp_df1))
        except:
            columns = list((range(0,13)))
            column_str = []
            for i in columns:
                column_str.append(str(i))
            sp_df1 = pd.DataFrame([],columns = ["file_name"]+column_str+["label"])
            print("Created new master dataframe")
        print("Extracting tgz file: ",tgz_file)
        extract(tgz_file, extract_path = '/tmp/audio')
        print("Finished extracting")
        print("Saving filename")
        filename = os.path.splitext(tgz_file)[0]
        print("Filename saved")
        print(filename)
        #concatenate .wav files to one (one .wav file per speaker)
        print("Concatenating speaker's .wav files")
        wav_list = []
        for wav in glob.glob('/tmp/audio/'+filename+'/wav/*.wav'):
            wav_list.append(AudioSegment.from_wav(wav))
        if len(wav_list)>=1:
            print("Speaker's .wav files have been prepared for concatenation")
            #print(wav_list)
            comb_wav = sum(wav_list)
            #print(comb_wav)
            print(".wav files have been Concatenated")
            comb_wav.export("/tmp/audio/"+filename+"/comb_wav.wav", format="wav")
            print("Speaker's .wav file has been exported")
            print("Extracting MFCC / features")
            feature = parser("/tmp/audio/"+filename+"/comb_wav.wav")
            print("MFCCs have been extracted")
            print(feature)
            print(feature.shape)
            print("type of MFCC data object: ",type(feature))
            print("Creating dataframe for the file's MFCC data")
            columns = list((range(0,13)))
            column_str = []
            for i in columns:
                column_str.append(str(i))
            print("column names are:")
            print(column_str)
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
            print("Appending current file's MFCC data to master dataframe")
            sp_df_new = sp_df.append(curr_db, ignore_index=True)
            print("Successfully appended new data")
            print("Saving appended dataframe to csv")
            sp_df_new.to_csv("../sp_df.csv")
            print("Successfully updated master dataframe!")
            print("Removing extracted directory")
            shutil.rmtree('/tmp/audio/'+filename)
            print("Directory removed!")
    except Exception as e:
        print(e)


label = input("Which category are these speech files? ")

dir_list = []
for dirname in glob.glob('*/'):
    dir_list.append(dirname)

for directory in dir_list:
    os.chdir(directory)
    dirname = directory[:-1]
    files_list = []
    for tgz in glob.glob('*.tgz'):
        files_list.append(tgz)
    fl_df = pd.DataFrame(files_list)
    fl_df[0].apply(lambda x: get_save_mfcc(x,label))
    os.chdir("..")
