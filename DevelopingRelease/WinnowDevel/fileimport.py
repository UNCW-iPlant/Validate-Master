"""
Functions to import both class and results folder files
"""

import os
import data
import csv


def getList(folder):
	"""
	Returns the complete location of the folder with the aggregated outputs

	:param folder: folder to get the location of
	:return: the complete folder location
	"""
	return os.listdir(folder)
    

def loadFile(folder, thisFile, seper):
	"""
	Reads each GWAS output from a folder

	:param folder: folder to load GWAS from
	:param thisFile: file to read
	:param seper: how the data is separated
	:return: the GWAS data of the file
	"""
	return data.Data(folder + "/" + thisFile, seper, skiprow=False)

def loadKT(thisFile, seper):
	"""
	Reads the SNPs and effect sizes from the known-truth file

	:param thisFile: file to read
	:param seper: how the data is separated
	:return: the known-truth data of the file
	"""
	return data.Data(thisFile, seper, skiprow=True)

def trueFalse(currentSnp, ktSnps):
	"""
	Defines the known truth list

	:param currentSnp: current SNP
	:param ktSnps: known-truth SNPs
	:return: True is the current SNP is in the known-truth SNPs
	"""
	if currentSnp in ktSnps:
		return True
	else:
		return False

def writeCSV(filename, keepToWrite, method="wb", exportDelimiter=","):
	"""
	Writes the Winnow output file once analysis is complete

	:param filename: file name to save as
	:param keepToWrite: data to write
	:param method: writing method
	:param exportDelimiter: how data is separated
	"""
	with open(filename + ".txt", method) as openFile:
		openFileWriter = csv.writer(openFile, delimiter=exportDelimiter)
		if method == "wb":
			openFileWriter.writerow(keepToWrite[0])
		currentRow = list()
		for item in keepToWrite[1]:
			currentRow.append(item)
		openFileWriter.writerow(currentRow)

def writeSettings(datafiles, winnowargs):
	a = winnowargs['analysis']
	if winnowargs['beta'] is not None:
		a += ' with beta'
	else:
		a += ' without beta'
	with open(winnowargs['filename'] +"_settings.txt", 'wb') as openFile:
		openFileWriter = csv.writer(openFile, delimiter='\t')
		openFileWriter.writerow(('Data Files', 'Truth File', 'Results File', 'Analysis Type', 'KT Type', 'Threshold'))
		first_pass = True
		for each in datafiles:
			if first_pass:
				openFileWriter.writerow((each, winnowargs['truth'], winnowargs['filename']+'.txt', a,
										 winnowargs['kt_type'], winnowargs['threshold']))
				first_pass = False
			else:
				openFileWriter.writerow((each, '', '', '', ''))

