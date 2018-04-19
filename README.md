# Diagnosis-via-speech
* Short-Term Goal: to effectively apply deep learning to speech data. 
* Long-term Goal: to diagnose various speech disorders from speech input via mobile app.  


## Phase 1: general speech - experiment with neural networks
* Experiment with how neural networks learn from speech data. Collect a lot of speech data and extract relevant features.

#### Questions/Issues
* Which speech features work best to train neural networks as I need? How many MFCCs? 13? 40? 
** helpful article: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.75.8303&rep=rep1&type=pdf

The speech I could most easily access at the moment was English (surprise!) and a bit of German. I decided to train neural networks on English and German and see if it could learn which langauge was which with new input.

I downloaded English and German speech from Voxforge (several other languages are available there as well): 

1) to batch download the English data, write the following command(s) in (Linux) commandline (in the directory you want the speech data) Note: this will save the speech in zipfiles at the following path, relative to where you call the command(s): www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Original/  If you call multiple commands from the same directory, the zipfiles will be stored in their own corresponding folder (16kHz_16bit/) (i.e. the zipfiles won't get mixed together).

wget -r -A.tgz http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Original/48kHz_16bit/s

there are several folders with speech data: the above folder is "48kHz_16bit" and has the most speech data. Other folders with varying amounts of speech data include "16kHz_16bit/","32kHz_16bit/","44.1kHz_16bit/","8kHz_16bit/". Just exchange the text and you will get the files in the other folders as well.

this will download all of the individual speaker files in .tgz format. 

2) run "MFCC13_zip_wav_sqlite3.py" in the parent directory of where the "48kHz_16bit" etc. folders are located (e.g. www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Original). This will save the wave files' MFCCs (13, at 25ms windows w 10ms shifts) to a database "sp_mfcc" in the table "mfcc_13" in the current directory, via sqlite3. Note: you will be asked for which language category the speech is. Type in "English" or whatever label you want to use for the data. This label will be combined with the wave file's directory label to keep track of which group of files it belongs to (i.e. "48kHz_16bit" vs  "8kHz_16bit" in case that is relevant to your purpose). This can be used as the dependent variable/category for training a neural network.

3) Downloaded German speech from: http://www.voxforge.org/home/forums/other-languages/german/open-speech-data-corpus-for-german

This has been structured so that if the zipfile is extracted, tons of memory will be used up. Unzip file somewhere with sufficient memory. I think it needs a total of 20GiB. 

4) run "MFCC13_wav_sqlite3.py script" in the directory where the folders "test", "dev", and "train" are located. The wave files in each directory will be processed and their MFCCs (13, with 25ms windows at 10ms shifts) will be saved to a database "sp_mfcc", in the table "mfcc_13" via sqlite3. Note: you will be asked for which language category the speech is. Type in "German" or whatever label you want to use for the data. The label will be combined with the folder name the wave file is saved in. This label can be used as the dependent variable/category the neural network will be trained on.

* Learn how to apply neural networks to speech of various languages, men vs women, adults vs children, differnt emotions, etc. 

Note: if you want to save the model to Json, need to install h5py. Can do this by typing into the commandline:
pip3 install --user --upgrade h5py

1) run "engerm_prep_ml.py" in same directory as "sp_df.csv" (the output file from the two 'get_MFCC_wav.py' and 'extract_tgz_wav_concat_MFCC.py' scripts). This will prepare the data for deep-learning. The new dataframe will be saved as "engerm_mfcc_ml.csv". Note: this script expects only 2 languages in dataset, English as well as another language. 

2) run "engerm_ann.py" in same directory as "engerm_mfcc_ml.csv". This trains an artificial neural network (ANN) on the MFCC data and requires a pretty good machine to complete. It does not work on my puny little laptop. 

* Develop simple, fun mobile applications based on the models

## Phase 2: clinical speech - maximize model performance!!!
* (Try to) find enough clinical speech data... 
* Overcome challenges of limited data --> make apps that could collect speech data? Write research institutions and ask for their data?
* Apply deep learning to speech data and work to maximize model performance. Need to consider Type I and Type II errors - better to have a false alarm than miss a diagnosis.
* Given available data, plan mobile application for that population (i.e. speech data of people with aphasia --> develop app for that population; speech data of children with SLI (keep dreaming....) --> develop app for children; etc.) 

## Phase 3: medical app - game development?
* For adults and children, try to present the app as a game. Create game with Unity/Blender? 
* Develop mobile app that takes in the user's speech and can diagnose what kind of aphasia they have or if they have a language development disorder like SLI or dyslexia!!!! (Or... that they speak English with a German accent... we'll see!)
