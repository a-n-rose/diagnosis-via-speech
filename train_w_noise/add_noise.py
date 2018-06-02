#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 18:28:19 2018

@author: airos
"""

import numpy as np
import sounddevice as sd
import librosa
import math
import random


def rec_envnoise(duration,sr):
    user_rec = sd.rec(int(duration*sr),samplerate=sr,channels=1)
    sd.wait()   
    return(user_rec)
    
def rec_envnoise_mult(num_rec,duration,sr):
    env_noise = np.array([])
    for i in range(num_rec):
       user_rec = sd.rec(int(duration*sr),samplerate=sr,channels=1,blocking=True)
       env_noise= np.append(env_noise,user_rec)
    sd.close()
    return(env_noise)

def match_length(noise,sr,desired_length):
    noise2 = np.array([])
    end_noiselength = sr*desired_length
    start_noiselength = len(noise)
    frac, int_len = math.modf(end_noiselength/start_noiselength)
    for i in range(int(int_len)):
        noise2 = np.append(noise2,noise)
    if frac:
        max_index = int(start_noiselength*frac)
        end_index = len(noise) - max_index
        rand_start = random.randrange(0,end_index)
        noise2 = np.append(noise2,noise[rand_start:rand_start+max_index])
    if len(noise2) != end_noiselength:
        diff = int(end_noiselength - len(noise2))
        if diff < 0:
            noise2 = noise2[:diff]
        else:
            noise2 = np.append(noise2,np.zeros(diff,))
    return(noise2)

def normalize(np_array):
    min_array = min(np_array)
    max_array = max(np_array)
    normed = (np_array-min_array)/(max_array-min_array)
    return(normed)

def scale_noise(np_array,factor):
    '''
    If you want to reduce the amplitude by half, the factor should equal 0.5
    '''
    return(np_array*factor)
    
    

