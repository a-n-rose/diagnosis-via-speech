'''
file to extract .wav file from all .tgz in a directory(with a folder in it called 'wav'!!!), one at a time, to the Root/tmp/audio directory.
program will concatenate all .wav from one speaker
then will extract MFCC from that .wav

the MFCCs will be saved to a master database

the extracted files will then be deleted

Note: several notifications are availale via print() but are mostly commented out
The ones that aren't commented out are to show that the algorithm has successfully completed extracting (.wav and MFCC), saving, and finally deleting the file(s).
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
            #print("Created new master dataframe")
        #print("Extracting tgz file: ",tgz_file)
        extract(tgz_file, extract_path = '/tmp/audio')
        #print("Finished extracting")
        #print("Saving speaker's filename")
        filename = os.path.splitext(tgz_file)[0]
        #print("Speaker's filename saved")
        #print(filename)
        #concatenate .wav files to one (one .wav file per speaker)
        #print("Concatenating speaker's .wav files")
        wav_list = []
        for wav in glob.glob('/tmp/audio/'+filename+'/wav/*.wav'):
            wav_list.append(AudioSegment.from_wav(wav))
        if len(wav_list)>=1:
        #    print("Speaker's .wav files have been prepared for concatenation")
            #print(wav_list)
            comb_wav = sum(wav_list)
            #print(comb_wav)
         #   print(".wav files have been Concatenated")
            comb_wav.export("/tmp/audio/"+filename+"/comb_wav.wav", format="wav")
           # print("Speaker's .wav file has been exported")
        #print("Extracting MFCC / features")
        feature = parser("/tmp/audio/"+filename+"/comb_wav.wav")
        #print("MFCCs have been extracted")
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
        #print("Successfully appended new data")
        #print("Saving appended dataframe to csv")
        sp_df_new.to_csv('/tmp/audio/sp_df.csv')
        print("Successfully updated master dataframe!")
        print("Successfully updated master dataframe with ", filename)
        print("New dimensions of the master dataframe: ", sp_df_new.shape)        
        #print("Removing extracted directory")
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



    
    
    
    

    
