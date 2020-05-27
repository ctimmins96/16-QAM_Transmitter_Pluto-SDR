from QAM_TX import *
from QAM_RX import *
from SDR_Setup import *


if __name__ == '__main__':
	sdr = pluto_setup(True, 1e8,True,True,1e8)
	
