"""
Functions to import both class and results folder files
"""


import os, data, csv

"""    Gets the location of the folder with the aggregated outputs"""
def getList(folder):
	return os.listdir(folder)
    
"""    Reads each GWAS output from the folder"""
def loadFile(folder, thisFile, seper):
	return data.Data(folder + "/" + thisFile, seper, skiprow=False)

"""    Reads the SNPs and effect sizes from the known-truth file"""
def loadKT(thisFile, seper):
	return data.Data(thisFile, seper, skiprow=True)

"""    Defines the known truth list"""
def trueFalse(currentSnp, ktSnps):
	if currentSnp in ktSnps:
		return True
	else:
		return False

"""    Writes the Winnow output file once analysis is complete"""
def writeCSV(filename, keepToWrite, method="wb", exportDelimiter=","):
	with open(filename + ".txt", method) as openFile:
		openFileWriter = csv.writer(openFile, delimiter=exportDelimiter)
		if method == "wb":
			openFileWriter.writerow(keepToWrite[0])
		currentRow = list()
		for item in keepToWrite[1]:
			currentRow.append(item)
		openFileWriter.writerow(currentRow)