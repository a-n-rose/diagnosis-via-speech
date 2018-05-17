#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 20:29:10 2018

@author: airos
"""

import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile


sample_rate, samples = wavfile.read('H46/03_1SL/6VJ3NOS.WAV')
frequencies, times, spectogram = signal.spectrogram(samples, sample_rate)


fig=plt.figure()
ax=fig.add_subplot(1,4,1)
extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

plt.pcolormesh(times, frequencies, spectogram)
plt.axis('off')
plt.imshow(spectogram)



#plt.ylabel('Frequency [Hz]')
#plt.xlabel('Time [sec]')
#plt.show()
plt.savefig('spec2_sm3_high.png',bbox_inches=extent, pad_inches=0,transparent=True, frameon=False,dpi = 500)

 
