### Import Statements
from QAM_CONST import *
import numpy as np

### Function Definitions

########################################################################
# Nearest Neighbor Approximation
#
# Method: near_neighbor
#
# Description:
# ------------
# Uses the nearest neighbor approximation on a given partition to determine phase delay and magnitude (bit mask)
#
# Parameters:
# -----------
# part
# - Type: double[]
# - Description: Partition of transmitted variable
#
# Dependencies
# ------------
# - KEY_16QAM
# - norm_xcorr
########################################################################

def near_neighbor(part):
	N = len(part)
	f_amp = max(part)
	f_pha = 0
	max_corr = 0
	tst_wav = [0]*N

	bit = '0'
	bits = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

	for i in range(N):
		for j in range(N):
			tst_wav(j) = np.sin(2*np.pi*(j + i)/N)

		tmp = norm_xcorr(part,tst_wav)
		if (tmp > max_corr):
			max_corr = tmp
			f_pha = 2*np.pi*(i/N)

	f_z = f_amp*(np.cos(f_pha) + 1j*np.sin(f_pha))
	dist = 100
	for k in range(len(bits)):
		if (abs(f_z - KEY_16QAM[bits[k]]) < dist):
			dist = abs(f_z - KEY_16QAM[bits[k]])
			bit = bits[k]

	return bit 

########################################################################
# Normalized Cross Correlation Function
#
# Method: norm_xcorr
#
# Description:
# ------------
# Computes the normalized cross-correlation between two double arrays
#
# Parameters:
# -----------
# x1
# - Type: double[]
# - Description: First xcorr variable
# x2
# - Type: double[]
# - Description: Second xcorr variable
#
########################################################################

def norm_xcorr(x1,x2):
	# Compute the energy of x1 and x2
	e1 = 0
	for i in range(len(x1)):
		e1 += x1(i)**2

	e2 = 0
	for i in range(len(x2)):
		e2 += x2(i)**2

	# Create Temporary xcorr value
	xcorr_val = 0;

	# Create a padded version of x2
	x2_p = [0]*(len(x1) - 1) + x2 + [0]*(len(x1) - 1)

	for i in range(len(x1) + len(x2) - 1):
		tmp = x2_p[i:(i + len(x1))]
		xsum = 0
		for j in range(len(tmp)):
			xsum += tmp(j)*x1(j)/((e1*e2)**0.5)

		if (xsum > xcorr_val):
			xcorr_val = xsum

	return xcorr_val
