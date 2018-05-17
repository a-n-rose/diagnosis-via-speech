#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:43:52 2018

@author: airos
"""

from pydub import AudioSegment
from pydub.utils import make_chunks
import glob


##################################
#for a single file:
##################################
#filename = '2015-02-09-14-43-17_Kinect-Beam.wav'
#
#myaudio = AudioSegment.from_file(filename , "wav") 
#chunk_length_ms = 1000 # pydub calculates in millisec
#chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec
#
##Export all of the individual chunks as wav files
#
#for i, chunk in enumerate(chunks):
#    chunk_name = "chunk{0}.wav".format(i)
#    print("exporting", chunk_name)
#    chunk.export(chunk_name, format="wav")
#    
    
    
###################################
#for all files in a directory
###################################
wav_list = [db for db in glob.glob('*.wav')]

audio_coll = [AudioSegment.from_file(wave,"wav") for wave in wav_list]
chunk_length_ms = 500
chunks_list = [make_chunks(aud, chunk_length_ms) for aud in audio_coll]

for j, chunks in enumerate(chunks_list):
    for i, chunk in enumerate(chunks):
            chunk_name = "chunks/chunk{0}.wav".format(str(j)+'_'+str(i))
            print("exporting", chunk_name)
            chunk.export(chunk_name, format="wav")