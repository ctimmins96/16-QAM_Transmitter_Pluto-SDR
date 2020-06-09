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

def pluto_setup(tx = True,fc_tx=1e9,cyclic = False,rx=True,fc_rx=1e9):
	# Create device interface
	sdr = adi.Pluto('ip:192.168.2.1')

	# Configure properties
	# Check to see if tx or rx are asserted
	if (tx):
		# Configure Tx property
		sdr.tx_lo = int(fc_tx)
		sdr.tx_cyclic_buffer = cyclic
		sdr.tx_hardwaregain_chan0 = 0
		sdr.tx_rf_bandwidth = int(sdr.sample_rate)

	if (rx):
		# Configure Rx properties
		sdr.rx_lo = int(fc_rx)
		sdr.rx_rf_bandwidth = int(sdr.sample_rate)

	return sdr
