#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 20:29:10 2018

@author: airos
"""

import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import glob
import os



###################################
#for all files in a directory
###################################
os.chdir('./chunks/')
wav_list = [db for db in glob.glob('*.wav')]
samplerate_samples = [wavfile.read(filename) for filename in wav_list]
freq_times_spec = [signal.spectrogram(samples,sample_rate) for sample_rate, samples in iter(samplerate_samples)]

os.chdir('..')
count = 0
for freq, times, spectrogram in freq_times_spec:
    if spectrogram.shape[0] == freq.shape[0] and spectrogram.shape[1] == times.shape[0]:        
        fig=plt.figure()
        ax=fig.add_subplot(1,4,1)
        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        plt.pcolormesh(times,freq,spectrogram)
        plt.imshow(spectrogram)
        #plt.show()
        count+=1
        plt.savefig('images/wav2image_{}.png'.format(count),bbox_inches=extent, pad_inches=0,transparent=True, frameon=False,dpi = 500)



##################################
#for a single file:
##################################

#filename = '2015-02-09-14-43-17_Kinect-Beam.wav'
#sample_rate, samples = wavfile.read(filename)
#frequencies, times, spectogram = signal.spectrogram(samples, sample_rate)
#
#
#
##fig=plt.figure()
##ax=fig.add_subplot(1,4,1)
##extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
#
#plt.pcolormesh(times, frequencies, spectogram)
#plt.imshow(spectogram)
#plt.axis('off')
#plt.show()



#plt.ylabel('Frequency [Hz]')
#plt.xlabel('Time [sec]')
#plt.show()
#plt.savefig('spec2_sm3_high.png',bbox_inches=extent, pad_inches=0,transparent=True, frameon=False,dpi = 100)

 
