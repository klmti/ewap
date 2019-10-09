import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

import os
from glob import glob

import sma
import pcmfloat as pf
import wiener as wd

def calc_rt60(data, fs):
  #fs, data_raw = wavfile.read(i)
  #data = pf.pcm2float(data_raw)
  smaFactor = 500
  impulseLength = len(data) / float(fs/1000) #ms
  #print('impulse length: %i ms' % impulseLength) 

  analyticSignal = signal.hilbert(data)
  amplitudeEnvelope = np.abs(analyticSignal)

  if(smaFactor >= len(data)):
    print('impulse length smaller then SMA factor, returning 0!')
    return 0;

  filteredEnvelope = sma.filter(amplitudeEnvelope, smaFactor)  
  maxValuePosition = np.argmax(filteredEnvelope)  

  intersectionDecibelLevel = -60.0
  intersectionValue = pow(10,(intersectionDecibelLevel/20))
  intersectionValuePosition = maxValuePosition  

  found = True
  for i in range(maxValuePosition, len(filteredEnvelope)):
    if(intersectionValue >= filteredEnvelope[i]):
      found = True
      intersectionValuePosition = i
      break
    if(i == len(filteredEnvelope)-1):
      found = False
      intersectionValuePosition = np.argmin(filteredEnvelope)  

  estimatedLength = round((intersectionValuePosition - maxValuePosition) / float(fs/1000)) #ms
  return int(estimatedLength)
