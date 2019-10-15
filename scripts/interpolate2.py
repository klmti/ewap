import sys
import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

import os
from glob import glob
import matplotlib.gridspec as gridspec
import sma
import pcmfloat as pf
import wiener as wd

path = '../impulses/airwindows/PrimeMed.wav'
#path = '../impulses/airwindows/RoomMedium.wav'
smaFactor = 5000

fs, data_raw = wavfile.read(path)
data = pf.pcm2float(data_raw)
impulseLength = len(data) / float(fs/1000) #ms
#print('impulse length: %i ms' % impulseLength) 

analyticSignal = signal.hilbert(data)
amplitudeEnvelope = np.abs(analyticSignal)

if(smaFactor >= len(data)):
  print('impulse length smaller then SMA factor!')
  sys.exit(0)

filteredEnvelope = sma.filter(amplitudeEnvelope, smaFactor)  
maxValuePosition = np.argmax(filteredEnvelope)  
intersectionDecibelLevel = -60.0
intersectionValue = pow(10,(intersectionDecibelLevel/20))
intersectionValuePosition = maxValuePosition  




gs = gridspec.GridSpec(2,1)

fig = plt.figure()
ax1 = fig.add_subplot(gs[0,0]);
ax1.plot(data);

ax2 = fig.add_subplot(gs[1,0]);
#ax2.plot(xfft, 2.0/N * np.abs(yfft[:N//2]));
ax2.plot(amplitudeEnvelope, color='r')
ax2.plot(filteredEnvelope, color='b')
plt.show()

#plt.plot(amplitudeEnvelope, color='r')
#plt.plot(filteredEnvelope, color='b')
#plt.scatter(xdatanp, ydatanp, color='orange');

#plt.axhline(y=intersection_value, color='m')
#plt.axvline(x=intersection_pos, color='m')

#plt.show();