import sys
from scipy.io import wavfile
from scipy import signal
import pcmfloat as pf

if(len(sys.argv)!=5):
  print('usage: (input file) (ir file) (attenuation in dB) (output file)')
  sys.exit(0)

input_f = str(sys.argv[1])
ir_f = str(sys.argv[2])
db_factor = int(sys.argv[3])
output_f = str(sys.argv[4])

fs, input_pcm = wavfile.read(input_f)
fs_dummy, impulse_pcm = wavfile.read(ir_f)

input_f = pf.pcm2float(input_pcm)
impulse_f = pf.pcm2float(impulse_pcm)

mul_factor = pow(10,(db_factor/20))
impulse_f = impulse_f * mul_factor

convoluted_input_f = signal.convolve(impulse_f, input_f)
convoluted_input_pcm = pf.float2pcm(convoluted_input_f)

#limits the length to match the source
wavfile.write(output_f, fs, convoluted_input_pcm[:len(input_f)])
#wavfile.write(output_f, fs, convoluted_input_pcm)

#print(output_f)



