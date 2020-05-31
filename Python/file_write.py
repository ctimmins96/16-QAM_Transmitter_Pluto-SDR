"""
Temporary File for writing information to a file
"""
### Import Statements
import numpy as np

### Function Definitions
def log_file_write(real_time,encoded):
	# Open Log files
	f_text = open("log.txt","w")
	f_csv = open("log.csv","w")

	header1 = 'Real Time Received Data: \n'
	header2 = 'Encoded Data Received: \n'

	# Write each string to each log file
	for i in range(len(real_time)):
		f_text.write(header1)

		# Loop through real_time data and write to text file
		for j in range(len(real_time[i])):
			f_text.write(str(real_time[i][j]))
			f_csv.write(str(real_time[i][j]))
			if (j != len(real_time[i]) - 1):
				f_text.write(',')
				f_csv.write(',')

		f_text.write('\n')
		f_csv.write('\n')

		f_text.write(header2)

		# Loop through encoded data and write to text file
		for j in range(len(encoded[i])):
			f_text.write(str(encoded[i][j]))
			f_csv.write(str(encoded[i][j]))
			if (j != len(real_time[i]) - 1):
				f_text.write(',')
				f_csv.write(',')

		f_text.write('\n')
		f_csv.write('\n')

	f_text.close()
	f_csv.close()
