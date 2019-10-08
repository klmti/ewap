# copied from
# https://gist.github.com/danstowell/f2d81a897df9e23cc1da
import numpy as np
from numpy.fft import fft, ifft, ifftshift
def wiener_deconvolution(signal, kernel, lambd):
	"lambd is the SNR"
	kernel = np.hstack((kernel, np.zeros(len(signal) - len(kernel)))) # zero pad the kernel to same length
	H = fft(kernel)
	deconvolved = np.real(ifft(fft(signal)*np.conj(H)/(H*np.conj(H) + lambd**2)))
	return deconvolved
