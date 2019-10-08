import sys
import os
from numpy.fft import fft, ifft, ifftshift
from scipy import signal
from scipy.io import wavfile
import pcmfloat as pf
import wiener as wd
from glob import glob

input_sample = 'sample02-CathedralRoom-46.wav'
fs, sample_pcm = wavfile.read(input_sample)
sample_f = pf.pcm2float(sample_pcm)

impulses = [y for x in os.walk('../impulses') for y in glob(os.path.join(x[0], '*.wav'))]
print('irs found:',len(impulses))
db_factor = -40.0
mul_factor = pow(10,(db_factor/20))
print('ir attenuation:', db_factor)
lambd_est = 1e-3
results = list()
cnt = 0
for impulse in impulses:
  name = os.path.splitext(os.path.basename(impulse))[0]
  #print('processing',name)
  fs_i, impulse_pcm = wavfile.read(impulse)
  if(fs_i != fs):
    print('fs missmatch!')
    break
  if(impulse_pcm.size > sample_pcm.size):
    #print('ir cant be shorter than sample, skipping')
    continue
  impulse_f = pf.pcm2float(impulse_pcm)
  impulse_f = impulse_f * mul_factor
  deconv_f = wd.wiener_deconvolution(sample_f, impulse_f, lambd_est)
  mse = 0.0
  for i in range(len(sample_f)):
    mse = mse + ((1/len(sample_f)) * pow((sample_f[i] - deconv_f[i]),2))
  result = (mse, name)
  results.append(result)
  cnt = cnt + 1
  #if(cnt > 10):
  #  break


print('irs processed:', len(results))
results.sort(key=lambda x: x[0])

for it in results:
  print("%10f %s" % (it[0], it[1]))


