#!/usr/bin/env python3

import sys
import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt



def main():
	operations = {"hist": hist, "record": record}
	if len(sys.argv) < 3:
		print("You need to specify an operation and a file name")
		exit(1)
	operation = sys.argv[1]
	filename = sys.argv[2]
	
	# It's magic
	operations[operation](filename) 


# Records new data to the file
def record(filename):
	data = entryloop()
	writecsv(filename, data)


# Makes a histogram from the specified file
def hist(filename):
	data = readcsv(filename)
	start = datetime.fromisoformat(data[0])
	times = []
	for thing in data:
		obj = datetime.fromisoformat(thing)
		diff = obj - start
		times.append(int(diff.total_seconds())/60)
	plt.hist(times)
	plt.xlabel("Time (minutes)")
	plt.ylabel("Number of Occurrences")
	plt.xlim(left=0)
	plt.show()


# The entry loop for data recording
def entryloop():
	data = []
	try:
		while input() == "":
			entry = datetime.now().isoformat()
			data.append(entry)
			print(quickstats(data), end="\r")
	except KeyboardInterrupt:
		print("no need to be rude about it")
	return data


# Gives a little statistical preview of the stuff
def quickstats(data):
	initial = datetime.fromisoformat(data[0])
	mrecent = datetime.fromisoformat(data[-1])
	difference = mrecent - initial
	amount = len(data)
	# Don't divide by zero
	if difference.total_seconds() == 0:
		rate = 0
	else:
		rate = amount / (difference.total_seconds() / 60) # things per minute
	string = "%3i entries, %.2f tpm" % (amount, rate)
	return string	


# Gets the contents of a csv file
def readcsv(filename):
	csvf = open(filename, "r", newline="")
	reader = csv.reader(csvf, delimiter=",")
	contents = []
	# Why u no superscriptable, [1:] would be so much better
	itsthetitle = True
	for row in reader: # Skip the title entry
		if itsthetitle:
			itsthetitle = False
			continue
		contents.append(row[0])
	csvf.close()
	return contents


# Writes to a file
def writecsv(filename, contents, mode="w"):
	if os.path.isfile(filename):
		# File exists
		print("%s already exists, should it be overwritten?" % filename)
		if input("[y/n] ").lower() != "y":
			# Choose another filename
			test = input("Write to: ")
			writecsv(test, contents, mode)
	csvf = open(filename, mode)
	writer = csv.writer(csvf, delimiter=",")
	writer.writerow(["date"])
	for row in contents:
		writer.writerow([row])
	csvf.close()
	return


if __name__ == "__main__":
	main()

