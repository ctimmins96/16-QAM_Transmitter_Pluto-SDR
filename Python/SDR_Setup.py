"""
File: SDR_Setup.py

Author: Chase Timmins
Create Date: May 20, 2020

Purpose:
Setup the Pluto-SDR to prepare for transmission

Methods:
- pluto_setup
"""
import lib.adi as adi
import numpy as np

"""
Method: pluto_setup(tx,fc_tx,rx,fc_rx)

Parameters:
-------------------------------------------------------------------------
|Name 			|Type 			|Description 							|
-------------------------------------------------------------------------
|tx 			|boolean 		|Determines whether or not to setup the |
 								|tx portion of the sdr 					|
|fc_tx 			|double 		|Local oscillator frequency for tx 		|
								|hardware 								|
|rx 			|boolean 		|Determines whether or not to setup the |
 								|rx portion of the sdr 					|
|fc_rx 			|double 		|Local oscillator frequency for rx 		|
								|hardware 								|
-------------------------------------------------------------------------

Output:
sdr
 -Type: adi.Pluto
 -Description: Symbolic object for the ADALM-Pluto sdr
"""

def pluto_setup(tx = True,fc_tx=1e9,rx=True,fc_rx=1e9):
	# Create device interface
	sdr = adi.Pluto()

	# Configure properties
	# Check to see if tx or rx are asserted
	if (tx):
		# Configure Tx property
		sdr.tx_lo = fc_tx
		sdr.tx_cyclic_buffer = False
		sdr.tx_hardwaregain_chan0 = 0

	if (rx):
		# Configure Rx properties
		sdr.rx_lo = fc_rx
		sdr.rx_rf_bandwidth = 1e6

	return sdr
