# Diagnosis-via-speech
* Short-Term Goal: to effectively apply deep learning to speech data. 
* Long-term Goal: to diagnose various speech disorders from speech input via mobile app.  


## Phase 1: general speech - experiment with neural networks
* Experiment with how neural networks learn from speech data. Collect a lot of speech data and extract relevant features.

Downloaded English and German speech from Voxforge (several other languages available as well): 

1) write the following commands in (Linux) commandline (in the directory you want the speech data):  

wget -r -A.tgz http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Original/48kHz_16bit/s

there are several folders with speech data: the above folder is "48kHz_16bit". Other folders include "16kHz_16bit/","32kHz_16bit/","44.1kHz_16bit/","8kHz_16bit/". Just exchange the text and you will get the files in the other folders as well.

this will download all of the individual speaker files in .tgz format. 

2) run "extract_tgz_wav_concat_MFCC.py" in same directory as the .tgz file(s). This will save a new .csv in  Root/tmp/audio directory. This .csv will include columns for the speaker/filename, MFCCs, and language/label (English). IF kept in this directory, the data from other languages, i.e. German (below) will be added.

3) Downloaded German speech from: http://www.voxforge.org/home/forums/other-languages/german/open-speech-data-corpus-for-german

This has been structured so that if the zipfile is extracted, tons of memory will be used up. Unzip file somewhere with sufficient memory

4) run get_MFCC_wav.py script in directory with .wav files of German speech (in test and dev directories) to save MFCCs from this data to the database with the English MFCCs (but with the label of "German" of course)

* Learn how to apply neural networks to speech of various languages, men vs women (if possible), adults vs children, differnt emotions, etc.
** run the .py script (which will ask for language category, i.e. English) which will extract the .wav files one by one to the Root/tmp directory, deleting the extracted files once the MFCCs have been calculated. The MFCCs of all the speakers will be saved into a .csv which will also be in the Root/tmp directory.
* Develop simple, fun mobile applications based on the models

## Phase 2: clinical speech - maximize model performance!!!
* (Try to) find enough clinical speech data... 
* Overcome challenges of limited data --> make apps that could collect speech data? Write research institutions and ask for their data?
* Apply deep learning to speech data and work to maximize model performance. Need to consider Type I and Type II errors - better to have a false alarm than miss a diagnosis.
* Given available data, plan mobile application for that population (i.e. speech data of people with aphasia --> develop app for that population; speech dataa of children with SLI (keep dreaming....) --> develop app for children; etc.) 

## Phase 3: medical app - game development?
* For adults and children, try to present the app as a game. Create game with Unity/Blender? 
* Develop mobile app that takes in the user's speech and can diagnose what kind of aphasia they have or if they have a language development disorder like SLI or dyslexia!!!! (Or... that they speak English with a German accent... we'll see!)
