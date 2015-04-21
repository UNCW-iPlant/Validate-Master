# WinPy -- formerly Validate.R in Python
# Author: Dustin Landers
# Contact: (770 289-8830) :: dustin.landers@gmail.com


"""Dependencies"""
from commandline import *
from fileimport import *
from checkhidden import *
from gwas import *
import numpy as np
import doctest


"""Main function and execution"""
def main():
        """    See docstrings in commandline.py and performetrics.py for additional information"""
	initializeGraphics()
	folder, analysis, truth, snp, score, beta, filename, threshold, seper, kttype, kttypeseper, severity = checkArgs()
	appOutputList = checkList(getList(folder))
	ktFile = loadKT(truth, kttypeseper)
	""">>>usage()"""
	"""   Runs the following code if the known-truth file is in OTE format: only truth and effect"""
	if kttype == "OTE":
		acquiredData = loadFile(folder, appOutputList[0], seper)
		snpColumnNo = acquiredData.header.index(snp)
		snpColumn = list()
		for each in acquiredData.data.iteritems():
			snpColumn.append(each[1][snpColumnNo])
		
		ktSnps = list()
		for each in ktFile.data.iteritems():
			ktSnps.append(each[1][0])
		ktBetas = list()
		for each in ktFile.data.iteritems():
			ktBetas.append(each[1][1])

		snpTrueFalse = list()
		for each in snpColumn:
			snpTrueFalse.append(trueFalse(each, ktSnps))
		
		if beta is not None:
			betaTrueFalse = list()
			count = 0
			for each in snpTrueFalse:
				if each is True:
					current = snpColumn[count]
					match = ktSnps.index(current)
					thisBeta = ktBetas[match]
					betaTrueFalse.append(float(thisBeta))
				else:
					betaTrueFalse.append(float(0))
				count += 1

		if severity is None:
			severity = float(len(ktSnps))/float(len(snpTrueFalse) - len(ktSnps))

	firstForHeader = True
	for each in appOutputList:
		acquiredData = loadFile(folder, each, seper)
		snpColumnNo = acquiredData.header.index(snp)
		snpColumn = list()
		for each in acquiredData.data.iteritems():
			snpColumn.append(each[1][snpColumnNo])

		scoreColumnNo = acquiredData.header.index(score)
		scoreColumn = list()
		for each in acquiredData.data.iteritems():
			scoreColumn.append(float(each[1][scoreColumnNo]))

		if beta is not None:
			betaColumnNo = acquiredData.header.index(beta)
			betaColumn = list()
			for each in acquiredData.data.iteritems():
				betaColumn.append(float(each[1][betaColumnNo]))

		if analysis == "GWAS" and firstForHeader:
			"""Currently, only GWAS analysis is supported. 
			Prediction algorithms for SNPs will be included in 
			later versions of the software"""
			if beta is not None:
				keepToWrite = gwasWithBeta(betaColumn, betaTrueFalse, snpTrueFalse, scoreColumn, threshold)
				writeCSV(filename, keepToWrite, "wb", "\t")
			if beta is None:
				keepToWrite = gwasWithoutBeta(snpTrueFalse, scoreColumn, threshold)
				writeCSV(filename, keepToWrite, "wb", "\t")
		else:
		    """Fit statistics calculated from Winnow vary depending on whether or not
		    a beta/effect size column was named in the input data"""
		    if beta is not None:
		        keepToWrite = gwasWithBeta(betaColumn, betaTrueFalse, snpTrueFalse, scoreColumn, threshold)
		        writeCSV(filename, keepToWrite, "a", "\t")
		    if beta is None:
		        keepToWrite = gwasWithoutBeta(snpTrueFalse, scoreColumn, threshold)
		        writeCSV(filename, keepToWrite, "a", "\t")
		firstForHeader = False

if __name__ == "__main__":
	main()
