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

samples_paths = [y for x in os.walk('../samples') for y in glob(os.path.join(x[0], '*.wav'))]
samples_paths.sort()
for curr_sample_path in samples_paths:
	fs, data = wavfile.read(curr_sample_path)
	N = len(data)
	sample_name = os.path.splitext(ntpath.basename(curr_sample_path))[0]
	print(sample_name + ".wav", end = '')
	#print("length: %i" % N)
	xcorr_full = signal.correlate(data, data, mode='full', method='fft')
	xcorr = xcorr_full[:N//2] #its symetric, cut the usable half
	peaks_pos = dp.detect_peaks(xcorr, mph=0, mpd=0, show=False);
	print(" peaks: %i" % len(peaks_pos))


