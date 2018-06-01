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
import datetime
import random
import soundfile as sf
import logging

import add_noise


logging.basicConfig(filename='addnoise_mfcc40.log',level=logging.INFO,format='%(levelname)s:%(message)s')

def get_date():
    time = datetime.datetime.now()
    time_str = "{}".format(str(time.year)+'_'+str(time.day)+'_'+str(time.hour)+'_'+str(time.minute)+'__'+str(time.second))
    return(time_str)

def user_ready(action):
    user_input = input("Please press Y {}".format(action))
    if 'y' in user_input.lower():
        return True
    else:
        user_ready(action)

    return None

def parser(file,num_mfcc,env_noise):
    y, sr = librosa.load(file, res_type= 'kaiser_fast')
    y = add_noise.normalize(y)
    
    #at random apply varying amounts of environment noise
    rand_scale = random.choice([0.0,0.25,0.5,0.75,1.0,1.25])
    if rand_scale:
        #apply *known* environemt noise to signal
        total_length = len(y)/sr
        envnoise_normalized = add_noise.normalize(env_noise)
        envnoise_scaled = add_noise.scale_noise(envnoise_normalized,rand_scale)
        envnoise_matched = add_noise.match_length(envnoise_scaled,sr,total_length)
        y += envnoise_matched
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=num_mfcc,hop_length=int(0.010*sr),n_fft=int(0.025*sr))
    return mfccs, sr

def get_save_mfcc(tgz_file,label,dirname,num_mfcc,env_noise):
    label = label+"_"+dirname
    try:
        filename = os.path.splitext(tgz_file)[0]
        feature, sr = parser(filename+".wav",num_mfcc,env_noise)
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

#collect environment noise to be added to training data
print("We will record your environment for several seconds; please stay quiet")
#recording = False
#while recording == False:
    #user_input = input("If you are ready to start recording, press Y: ")
    #if "y" in user_input.lower():
        #recording = True
print("Now recording...")


sr = 22050
env_noise = add_noise.rec_envnoise_mult(5,3,sr)
print("Finished! \n")

#simply for documenation, save the environmental noise recorded
time_str = get_date()
env_filename = 'envnoise_'+time_str+'.wav'
sf.write(env_filename,env_noise,sr)




#label = input("Which category is this speech? ")
label = 'animals_noise2'
prog_start = time.time()
logging.info(label)
logging.info(prog_start)
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
        logging.info(dirname)
        print("Now processing the directory: "+dirname)
        files_list = []
        for wav in glob.glob('*.wav'):
            files_list.append(wav)
        if len(files_list) != 0:
            for i in range(len(files_list)):
                logging.info(files_list[i])
                get_save_mfcc(files_list[i],label,dirname,num_mfcc,env_noise)
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

