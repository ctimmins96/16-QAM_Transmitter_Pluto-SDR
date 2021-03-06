from QAM_TX import *
from QAM_RX import *
from SDR_Setup import *
from file_write import *

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

	# Attempt to receive data
	M = 4 								# Number of trials
	rx_buf1 = [[0]*len(tx)]*M			# Raw Data buffer
	rx_buf2 = [['']*N*len(tx_bits)]*M 	# Encoded Data buffer
	k = 0;

	# Make sure rx buffer is large enough to receive data
	sdr.rx_buffer_size = N*(len(tx_bits))*2

	# Transmit sinewave
	sdr.tx(tx)
        
	while(k < M):

		# Receive sinewave
		tmp = abs(sdr.rx())
		#tmp *= 2*(2**0.5)/max(tmp)

		rx_buf1[k] = tmp
		# TODO: FIR Filter input for noise

		# Extract Message by cross correlating with KEY_START_BITS
		start_idx = norm_xcorr2(xcorr_start,tmp)
		end_idx = norm_xcorr2(xcorr_end,tmp[start_idx:])

		tmp2 = tmp[start_idx:(start_idx + end_idx + N - 1)]

		# Partition tmp2 and convert into bits
		rx_bits = ['']*len(tx_bits)

		for j in range(len(tx_bits)):
			part = tmp2[(j*N):(j+1)*N - 1]
			rx_bits[j] = near_neighbor(part)


		print('Transmitted bits: ' + arr2str(tx_bits))
		print('Received bits: ' + arr2str(rx_bits))

		# Store received data into rx_buf2
		rx_buf2[k] = rx_bits

		k += 1

	log_file_write(rx_buf1,rx_buf2)

	# Release SDR
	sdr.release()

