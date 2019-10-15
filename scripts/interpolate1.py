from pathlib import Path
from scipy.io import wavfile
import pcmfloat as pf
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz
from scipy.optimize import curve_fit
import numpy as np
import detect_peaks as dp

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def func1(x, b):
    y = np.power( (1.0-b) , x );
    return y

def func2(x, a, b):
    y = a * np.power( (1.0-b) , x );
    return y

def func3(x, a, b, c):
    y = a * np.power( (1.0-b) , x ) + c;
    return y

#for filename in Path('../impulses/').glob('**/*.wav'):
#    print(filename)

fs, data = wavfile.read('../impulses/airwindows/RoomHuge.wav')
data = abs(data);


cutoff = 10
order = 2
old_max = max(data)
#data = butter_lowpass_filter(data, cutoff, fs, order);
#data = data/max(data);
#data = data * old_max

peaks = dp.detect_peaks(data, mph=0, mpd=1000, show=False);
peaks_val = []
for i in range(0, len(peaks)):
  peaks_val.append(data[peaks[i]]);

xdata = []
ydata = []
for i in range(0, len(data), int(len(data)/100)):
  ydata.append(data[i]);
  xdata.append(i);
  #print("data[%i]: %f" % (i, data[i]))
#print(xdata)
xdatanp = np.array(xdata) 
ydatanp = np.array(ydata)
#xdatanp = np.array(xdata[0:10]) 
#ydatanp = np.array(ydata[0:10])

xdatanp = np.array(peaks) 
ydatanp = np.array(peaks_val)



#param_bounds=([1, 1][0.00001,0.0001][1, 1])
#popt, pcov = curve_fit(func, xdata, ydata, bounds=param_bounds);
popt, pcov = curve_fit(func2, xdatanp, ydatanp, p0=(1, 1e-6));
#popt, pcov = curve_fit(func2, xdatanp, ydatanp, p0=(1, 1e-6, 1), bounds=([0,0,0], [5,1,5]));
print(popt)
fitted=[]
for i in range(0, len(data)):
  fitted.append(func2(i, popt[0], popt[1] ))




db_factor = -60.0
intersection_value_float = pow(10,(db_factor/20))
intersection_value = (2^16-1) * intersection_value_float 

print(intersection_value_float)

print(intersection_value)

intersection_pos = 0;
for i in range(0, len(fitted)):
  #print("x")
  if(fitted[i] <= intersection_value):
    intersection_pos = i;
    break;

plt.plot(data)
plt.plot(fitted, color='r')

plt.scatter(xdatanp, ydatanp, color='orange');

plt.axhline(y=intersection_value, color='m')
plt.axvline(x=intersection_pos, color='m')

plt.show();
