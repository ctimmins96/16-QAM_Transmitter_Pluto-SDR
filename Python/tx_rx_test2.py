from QAM_TX import *
from QAM_RX import *
from SDR_Setup import *
from FILE_WRITE import *
import numpy as np

# Array to String
def arr2str(arr):
        final = ''

        for i in range(len(arr)):
                final += str(arr[i])
                if (i != len(arr) - 1):
                        final += ','

        return final

if __name__ == '__main__':
	# Create initial variables to be used later
	# Create SDR object
	sdr = pluto_setup(True, 1e9,True,True,1e9)

	# Set Sample rate and carrier frequency for the QAM (TX/RX)_LO already set
	N = 10
	fs = sdr.sample_rate
	fc = fs / N

	# Create cross correlation arrays for start and end bits (these are used to find the beginning and end of a message)
	xcorr_start = bits2sine(KEY_START_BITS,fc,fs)
	xcorr_end = bits2sine(KEY_END_BITS,fc,fs)


	# Create bit sequency to be transmitted
	tx_bits = KEY_START_BITS + ['1','0','C','4','9','B','2','E'] + KEY_END_BITS

	# Create Sinewave from bits
	tx = bits2sine(tx_bits,fc,fs)

	# Pad Either Side with zeros
	tx = [0]*int(0.5*len(tx)) + tx + [0]*int(0.5*len(tx))

	# Attempt to receive data
	M = 1 								# Number of trials
	rx_buf1 = [[0]*len(tx)]*M			# Raw Data buffer
	rx_buf2 = [['']*N*len(tx_bits)]*M 	# Encoded Data buffer
	k = 0;

	# Make sure rx buffer is large enough to receive data
	sdr.rx_buffer_size = N*(len(tx_bits))*4

	# Transmit sinewave
	sdr.tx(tx)

	while(k < M):

		# Receive sinewave
		tmp = (sdr.rx())
		#tmp *= 2*(2**0.5)/max(tmp)

		rx_buf1[k] = tmp
		# TODO: FIR Filter input for noise

		k += 1

	mat_file_write(rx_buf1,"")

	# Release SDR
	
