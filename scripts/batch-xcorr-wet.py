from scipy.io import wavfile
import scipy.fftpack as fft
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import detect_peaks as dp
import os
from glob import glob
import ntpath

sample = 'sample12-30db-'
found_samples_path = []
samples_paths = [y for x in os.walk('../temp/') for y in glob(os.path.join(x[0], '*.wav'))]
for curr_sample_path in samples_paths:
	if(sample in curr_sample_path):
		found_samples_path.append(curr_sample_path)

found_samples_path.sort()
print('found matching: %i' % len(found_samples_path))



for curr_sample_path in found_samples_path:
	fs, data = wavfile.read(curr_sample_path)
	N = len(data)
	sample_name = os.path.splitext(ntpath.basename(curr_sample_path))[0]
	sample_name = sample_name.replace(sample, '')
	#print(sample_name, end = '')
	#print(sample_name)
	#print("length: %i" % N)
	xcorr_full = signal.correlate(data, data, mode='full', method='fft')
	xcorr = xcorr_full[:N//2] #its symetric, cut the usable half
	peaks_pos = dp.detect_peaks(xcorr, mph=0, mpd=0, show=False);
	#print(" peaks: %i" % len(peaks_pos))
	print(len(peaks_pos))


