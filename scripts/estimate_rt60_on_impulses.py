import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

import os
from glob import glob

import sma
import pcmfloat as pf
import wiener as wd

smaFactor = 5000
impulse_paths = [y for x in os.walk('../impulses') for y in glob(os.path.join(x[0], '*.wav'))]

#impulse_paths = [
#'../impulses/voxengo/DirectCabinetN1.wav',
#'../impulses/voxengo/DirectCabinetN2.wav'
#]

print('impulses found: %i' % len(impulse_paths))
print('sma factor: %i' % smaFactor)

print('----------------------')
for i in impulse_paths:
  print(i)
  fs, data_raw = wavfile.read(i)
  data = pf.pcm2float(data_raw)
  impulseLength = len(data) / float(fs/1000) #ms
  print('impulse length: %i ms' % impulseLength) 

  analyticSignal = signal.hilbert(data)
  amplitudeEnvelope = np.abs(analyticSignal)

  if(smaFactor >= len(data)):
    print('impulse length smaller then SMA factor, skipping this sample!')
    continue

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
  print('estimated RT60: %i ms' % estimatedLength)
  if(not found):
    print('interection not found, using argmin as end point!')
  print('----------------------')

  #plt.plot(filteredEnvelope)
  #plt.axvline(x=maxValuePosition, color='r', label='begin')
  #plt.axvline(x=intersectionValuePosition, color='b', label='end')
  #plt.axhline(y=intersectionValue, color='k', label='intersection value')
  #plt.legend()
  #plt.show()
