"""
File: QAM-keying.py

Author: Chase Timmins
Create Date: May 19, 2020

Description:

Classes:
- InvalidBitsError

Methods:
- bits2sine
"""
### Import Statements
import adi
import numpy as np
import sys
import traceback
from QAM_CONST import *



### Function Definitions

########################################################################
# Creating Sine Wave from Bit Stream
#
# Method: bits2sine
#
# Description:
# ------------
# Create QAM-keyed sine wave from bit sequence
#
# Parameters:
# -----------
# tx_bits
# - Type: int[]
# - Description: integer array of bits to be converted to sine wave. Must be multiples of 4 bits (16-QAM)
# - Note: MSB is at index 0, LSB is at the last index
# fc
# - Type: double
# - Description: Carrier frequency of sinusoid
# fs
# - Type: double
# - Description: Sampling Freqency for Pluto SDR
#
# Return:
# -------
# tx
# - Type: double[]
# - Description: Sinusoid of generated QAM bits
#
# Dependencies:
# - KEY_16QAM
########################################################################
def bits2sine(tx_bits,fc,fs,complex_out = True):
	if (len(tx_bits) % 2 ~= 0):
		# Group bits into groups of 8 (bytes); each index is a nibble
		raise InvalidBitsError
		return 0
	else:
		# Create initial variables
		N = round(fs/fc)
		tx = range(N*len(tx_bits))

		# Loop through tx_bits variable and generate sinusoid
		if (complex_out):
			for i in range(len(tx_bits)):
				# Get complex variable from specified bit
				cplx_bit = KEY_16QAM[tx_bits[i]]

				# Convert complex variable to sinusoid
				amp = abs(cplx_bit)
				pha = np.arctan2(cplx_bit.imag,cplx_bit.real)

				# Use for loop to generate sinusoid
				for k in range(N):
					tx[k + N*i] = amp*(np.sin(2*np.pi*fc*k/fs + pha) + 1j*np.cos(2*np.pi*fc*k/fs + pha))
		else:
			for i in range(len(tx_bits)):
				# Get complex variable from specified bit
				cplx_bit = KEY_16QAM[tx_bits[i]]

				# Convert complex variable to sinusoid
				amp = abs(cplx_bit)
				pha = np.arctan2(cplx_bit.imag,cplx_bit.real)

				# Use for loop to generate sinusoid
				for k in range(N):
					tx[k + N*i] = amp*np.sin(2*np.pi*fc*k/fs + pha)

		return tx



### Class Definitions

########################################################################
# InvalidBitsError
#
# Class Name: InvalidBitsError
#
# Description:
# ------------
# Exception to be raised when an invalid number of bits is converted
#
# Parameters:
# -----------
# message
# - Type: String
# - Description: message to be printed to the console when the error is raised
########################################################################

class InvalidBitsError(Exception):
	def __init__(self, message):
		self.message = message
		print("InvalidBitsError Raised: " + self.message)
		traceback.print_exc(file=sys.stdout)
