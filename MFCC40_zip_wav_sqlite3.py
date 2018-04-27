'''
If you downloaded the .tgz files with wget
change your directory to: 
$ cd www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Original
This will collect all the folder names, and within each folder, extract one by one each .tgz file in /tmp/audio, 
get MFCCs in 25ms frames with window shifts of 10ms, save them to database "sp_mfcc" in table
"mfcc_40", in the directory where this script is, then delete the extracted files in the tmp dir.
If you apply this to all the English folders, it will take several hours to complete.

This script allows you to see how far along the program is in each directory

This calculates 40 coefficiens (rather than 13) and will therefore create a database with 42 columns (40 coefficiencts with 
filename and label)
'''


import os, tarfile
import pandas as pd
import librosa
import glob
import shutil
import sqlite3
from sqlite3 import Error
import time





def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None

def create_cursor(conn):
    try:
        return conn.cursor()
    except Error as e:
        print(e)


#'.' below means current directory
def extract(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])
            
def parser(file,num_mfcc):
    y, sr = librosa.load(file, res_type= 'kaiser_fast')
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=num_mfcc,hop_length=int(0.010*sr),n_fft=int(0.025*sr))
    return mfccs
    
def extract_save_mfcc(tgz_file,label,dirname,num_mfcc):
    label=label+"_"+dirname
    try:
        extract(tgz_file, extract_path = '/tmp/audio')
        filename = os.path.splitext(tgz_file)[0]
        for wav in glob.glob('/tmp/audio/'+filename+'/wav/*.wav'):
            feature = parser(wav, num_mfcc)
            columns = list((range(0,num_mfcc)))
            column_str = []
            for i in columns:
                column_str.append(str(i))
            feature_df = pd.DataFrame(feature)
            curr_db = pd.DataFrame.transpose(feature_df)
            curr_db.columns = column_str
            curr_db.insert(0,"file_name",filename+"_"+wav)
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
conn = create_connection('./german-speechdata-package-v2/sp_mfcc.db')
c = create_cursor(conn)

label = input("Which category are these speech files? ")
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
 
#I added a directory "English" where the tgz files were stored; If you didn't do that as well, you don't have to change directories
#os.chdir('./English')    
    
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
        for tgz in glob.glob('*.tgz'):
            files_list.append(tgz)
        if len(files_list) == 0:
            print("No .tgz files found in ", dirname)
        for i in range(len(files_list)):
            extract_save_mfcc(files_list[i],label,dirname,num_mfcc)
            print("Progress: ", (i/(len(files_list)-1))*100,"%  (",dirname,": ",j+1,"/",len(dir_list)," directories)")
        os.chdir("..")
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
