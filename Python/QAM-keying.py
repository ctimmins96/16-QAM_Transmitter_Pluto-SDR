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

### Function Definitions

########################################################################
# Creating Sine Wave from Bit Stream
#
# Method: bits2sine
#
# Description:
# Create QAM-keyed sine wave from bit sequence
#
# Parameters:
# tx_bits
# - Type: integer array
# - Description: integer array of bits to be converted to sine wave. Must be multiples of 4 bits (16-QAM)
# fc
# - Type: double
# - Description: Carrier frequency of sinusoid
# fs
# - Type: double
# - Description: Sampling Freqency for Pluto SDR
#
# Dependencies:
# - key_16qam
########################################################################
def bits2sine(tx_bits,fc,fs):
	if (len(tx_bits) % 4 ~= 0):
		raise InvalidBitsError

	# Group bits into groups of 4 (nibbles)

### Class Definitions

########################################################################
# InvalidBitsError
#
# Class Name: InvalidBitsError
#
# Description:
# Exception to be raised when an invalid number of bits is converted
#
# Parameters:
# message
# - Type: String
# - Description: message to be printed to the console when the error is raised
########################################################################

class InvalidBitsError(Exception):
	def __init__(self, message):
		self.message = message
		print("InvalidBitsError Raised: " + self.message)
		traceback.print_exc(file=sys.stdout)
