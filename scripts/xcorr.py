from scipy.io import wavfile
import scipy.fftpack as fft
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import detect_peaks as dp

fs_dry, data_dry = wavfile.read('../samples/sample01.wav')
N_dry = len(data_dry)

#fs_wet, data_wet = wavfile.read('../temp/sample01-30db-RoomLarge-1810ms.wav')
fs_wet, data_wet = wavfile.read('../temp/sample01-30db-3000CStreetGarageStairwell-2192ms.wav')
N_wet = len(data_wet)

print("dry length: %i" % N_dry)
print("wet length: %i" % N_wet)


xcorr_full_dry = signal.correlate(data_dry, data_dry, mode='full', method='fft')
xcorr_dry = xcorr_full_dry[:N_dry//2] #its symetric, cut the usable half
peaks_dry_pos = dp.detect_peaks(xcorr_dry, mph=0, mpd=0, show=False);
print("dry peaks: %i" % len(peaks_dry_pos))

xcorr_full_wet = signal.correlate(data_wet, data_wet, mode='full', method='fft')
xcorr_wet = xcorr_full_wet[:N_wet//2] #its symetric, cut the usable half
peaks_wet_pos = dp.detect_peaks(xcorr_wet, mph=0, mpd=0, show=False);
print("wet peaks: %i" % len(peaks_wet_pos))

gs = gridspec.GridSpec(2, 2)
fig = plt.figure()

ax1 = fig.add_subplot(gs[0,0]);
ax1.plot(data_dry);

ax2 = fig.add_subplot(gs[1,0]);
ax2.plot(xcorr_dry);

ax3 = fig.add_subplot(gs[0,1]);
ax3.plot(data_wet);

ax4 = fig.add_subplot(gs[1,1]);
ax4.plot(xcorr_wet);


plt.show()

