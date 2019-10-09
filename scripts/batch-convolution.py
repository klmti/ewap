import sys
from scipy.io import wavfile
from scipy import signal
import pcmfloat as pf
import ntpath
import os
from glob import glob
from rt60 import calc_rt60

output_folder = '../temp/'
samples_paths = [y for x in os.walk('../samples') for y in glob(os.path.join(x[0], '*.wav'))]
impulses_paths = [y for x in os.walk('../impulses') for y in glob(os.path.join(x[0], '*.wav'))]
ir_db_factor = -30.0
mul_factor = pow(10,(ir_db_factor/20))
print('samples found: %i' % len(samples_paths))
print('impulses found: %i' % len(impulses_paths))
output_elements = len(samples_paths) * len(impulses_paths)

counter = 0

for curr_sample_path in samples_paths:
	fs_sample, sample_pcm = wavfile.read(curr_sample_path)
	sample_float = pf.pcm2float(sample_pcm)
	for curr_impulse_path in impulses_paths:
		fs_impulse, impulse_pcm = wavfile.read(curr_impulse_path)
		impulse_float = pf.pcm2float(impulse_pcm)
		rt60 = calc_rt60(impulse_float, fs_impulse)
		if(fs_sample!=fs_impulse):
			print('fs missmatch, skip')
			continue;
		if(rt60 == 0):
			print('cannot compute rt60, skip')
		impulse_float = impulse_float * mul_factor
		convoluted_float = signal.convolve(sample_float, impulse_float)
		convoluted_pcm = pf.float2pcm(convoluted_float)
		sample_name = os.path.splitext(ntpath.basename(curr_sample_path))[0]
		impulse_name = os.path.splitext(ntpath.basename(curr_impulse_path))[0]
		output_name = sample_name + '-' + str(abs(int(ir_db_factor))) + 'db-' + impulse_name + '-' + str(rt60) + 'ms.wav'
		wavfile.write(output_folder+output_name, fs_sample, convoluted_pcm[:len(sample_pcm)])
		print('processing %i/%i:' % (counter, output_elements))
		counter = counter + 1
		print(output_name)
		#print(sample_name)
		#print(impulse_name)
		#print(rt60)
		#print('-------------------')