from QAM_TX import *
from QAM_RX import *
from SDR_Setup import *


if __name__ == '__main__':
	sdr = pluto_setup(True, 1e8,True,True,1e8)

	# Set Sample rate and carrier frequency for the QAM (TX/RX)_LO already set
	fs = sdr.sample_rate
	fc = fs / 100

	# Create bit sequency to be transmitted
	
