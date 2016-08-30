#!/usr/bin/env python
import os
import sys
import fileinput

def read_meta_file(filename, tag):
    retval = None
    for line in fileinput.input(filename):
        if tag == line.strip().split(':')[0].strip():
            retval = line.strip().split(':')[1].strip()
            break
    fileinput.close()
    return retval

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def printValidRuns(directory):
	for line in sorted(os.listdir(directory)):
		print(line)

def checkRun(runDir, colNum):
	resultFileName = os.path.join(runDir, "RES")
	if not os.path.isfile(resultFileName):
		print("Results file not found!")
		return
	resultFile = open(resultFileName)
	medianFilterSuccess = False
	collarFound = False
	leastsq_itr = -1
	leastsq_term = -1
	failureMode = None
	for line in resultFile:
		if ('Collar %d:' % colNum) in line:
			if ('Estimated location is') in line:
				medianFilterSuccess = True
			if 'Saving estimation...' in line:
				collarFound = True
			if 'iterations' in line:
				lineSplit = line.split()
				leastsq_itr = int(lineSplit[2])
			if ': ier' in line:
				lineSplit = line.split()
				leastsq_term = int(lineSplit[3].strip(';'))
			if 'No collars detected!' in line:
				failureMode = 'Limited detections'
			if 'No matches!' in line:
				failureMode = 'No matches'
			if 'Not enough variation' in line:
				failureMode = 'Not enough variation'
			if 'Collar model is invalid!' in line:
				failureMode = 'Invalid model'
	resultFile.close()
	return (medianFilterSuccess, collarFound, leastsq_itr, leastsq_term, failureMode)

def runAll(rct_data_dir):
	outputFile = open("./results.csv", 'w')
	outputFile.write("Run,Collar,Collar Present,Median Filter Success,Found Collar,Failure Mode,leastsq iterations,leastsq Termination,Good Estimation,Score\n")
	for run_dir in sorted(os.listdir(rct_data_dir)):
		if os.path.isdir(run_dir):
			run_num = int(os.path.basename(run_dir).split('_')[1])
			collarDefinitionFile = os.path.join(run_dir, 'COL')
			if not os.path.isfile(collarDefinitionFile):
				print("Collar definitions not found!")
				continue
			num_Collars = file_len(collarDefinitionFile)
			for collarNumber in xrange(1, num_Collars + 1):
				results = checkRun(run_dir, collarNumber)

				groundTruth = read_meta_file(os.path.join(run_dir, 'TRUTH'), str(collarNumber))
				# Run Number, collar number, ground truth, medianFilter, CollarFound
				outputFile.write('%d,%d,%s,' % (run_num, collarNumber, groundTruth))
				if results[0]:
					outputFile.write('1,')
				else:
					outputFile.write('0,')
				if results[1]:
					outputFile.write('1,')
				else:
					outputFile.write('0,')
				if results[1]:
					# empty, leastsq iterations, leastsq term
					outputFile.write(',%d,%d,,' % (results[2], results[3]))
				else:
					# Failure mode
					outputFile.write('%s,,,,' % (results[4]))
				outputFile.write('\n')
	outputFile.close()

if __name__ == '__main__':
	while True:
		rct_data_dir = "."
		run_num_str = raw_input("Enter run number, or 0 to exit: ")
		if run_num_str == "":
			continue
		if run_num_str == "ls":
			printValidRuns(rct_data_dir)
			continue
		if run_num_str == "all":
			runAll(rct_data_dir)
			break
		run_num = int(run_num_str)
		if run_num == 0:
			break
		run_dir = os.path.join(rct_data_dir, 'RUN_%06d' % run_num)
		collarDefinitionFile = os.path.join(run_dir, 'COL')
		if not os.path.isfile(collarDefinitionFile):
			print("Collar definitions not found!")
			continue
		num_Collars = file_len(collarDefinitionFile)
		collarNumberStr = raw_input("Enter collar number, from 1 to %d, or 0 to exit: " % num_Collars)
		collarNumber = int(collarNumberStr)
		if collarNumber == 0:
			break
		if collarNumber < 1 or collarNumber > num_Collars:
			print("Invalid entry!")
			continue
		results = checkRun(run_dir, collarNumber)
		print("Median Filter: %s" % results[0])
		print("Collar Found: %s" % results[1])
		if results[4] is not None:
			print("Failure Mode: %s" % results[4])
		if results[2] != -1:
			print("leastsq iterations: %d" % results[2])
		if results[3] != -1:
			print("leastsq termination: %d" % results[3])
		print("")
