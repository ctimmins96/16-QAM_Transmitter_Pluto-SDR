"""
Temporary File for writing information to a file
"""

def log_file_write(data):
	# Open Log files
	f_text = open("log.txt","w")
	f_csv = open("log.csv","w")

	# Write each string to each log file
