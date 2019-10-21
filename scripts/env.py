from scipy.io import wavfile
import scipy.fftpack as fft
#from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy.signal import butter, lfilter, freqz

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

fs, data = wavfile.read('../samples/sample01.wav')

gs = gridspec.GridSpec(4, 1)

fig = plt.figure()

ax1 = fig.add_subplot(gs[0,0]);
ax1.plot(data);

powd = np.abs(data);
cutoff = 10 #hz
order = 2
lp_data = butter_lowpass_filter(powd, cutoff, fs, order);

ax2 = fig.add_subplot(gs[1,0]);
ax2.plot(powd);

ax3 = fig.add_subplot(gs[2,0]);
ax3.plot(lp_data);

ax4 = fig.add_subplot(gs[3,0]);

ax4.plot(data)
ax4.plot(lp_data, 'r');

plt.show();

