# -*- coding: utf-8 -*-
""" 
Functions for indentifying and using the command-line to execute Winnow for Python
"""


"""Dependencies"""
import getopt, sys

"""Functions to be used later in the software"""
# Prints introduction graphics for every time the software is run
def initializeGraphics():
	print "###################################################################"
	print "###                                                            ####"
	print "###      Winnow for Python!                                    ####"
	print "###      By Dustin A. Landers                                  ####"
	print "###      Contact: (770) 289-8830 -- dustin.landers@gmail.com   ####"
	print "###                                                            ####"
	print "###################################################################"


# Prints all possible command-line arguments to the screen; also ends the execution of the software
def usage():
	print "\n\n\n"
	print "Command-line usage help menu.\n"
	print "--verbose or -v for verbose mode"
	print "--analysis or -a to specify either 'GWAS' or 'prediction' (if blank, Winnow assumes GWAS)"
	print "--Folder or -F to input folder of box results (required)"
	print "--Class or -C to specify the known-truth file for used simulation (required)"
	print "--Snp or -S to specify a string for the name of the SNP column in results file (required)"
	print "--Score or -P to specify a string for the name of the scoring column in results file (e.g., p-value; required)"
	print "--beta or -b to specify a string for the name of the estimated SNP effect column in results file"
	print "--filename or -f to specify the desired filename for the Winnow output file"
	print "--threshold ir -t to specify a desired threshold for classification performetrics where necessary"
	print "--seper or -s to specify either whitespace or comma"
	print "--kttype or -k to specify the type of known-truth file for --class (either OTE or FGS)"
	print "--kttypeseper or -r to specify delimination in known-truth file"
	print "--help or -h to see help menu\n\n"


# Checks for arguments at beginning of the execution of the main function
def checkArgs():
	try:
		opts, args = getopt.getopt(sys.argv[1:], shortopts="vha:F:C:S:P:b:y:f:t:s:k:r", longopts=["verbose", "help", 
			"analysis=", "Folder=", "Class=", "Snp=", "Score=", "beta=", "filename=", "threshold=", "seper=", "kttype=",
			"kttypeseper=", "severity="])

	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit()

	# Specifiying initial values of needed variables; unneeded specification when desiring defaults
	verbose = False 
	"""Tells the program whether or not to enter verbose mode, which displays the inputs and parameters as they are specified"""
	analysis = "GWAS"
	"""GWAS is the only analysis option available currently; prediction mode forthcoming in later versions"""
	filename = "Results"
	threshold = 0.05
	"""Threshold for determining Pvalue of correctly identified SNPs. Set at the standard significance level of 0.05; however,
	please note this default threshold does not take multiple test corrections into account!"""
	seper = "whitespace"
	"""Two options for delimiting input data: whitespace or comma"""
	kttype = "OTE"
	"""For the format of the known-truth file, OTE stands for “Only Truth and Effect.” As the name implies, such a file only contains 
	the SNPs with effects and the values of those effects. FGS stands for “Full Genome Set,” and this file type lists every SNP with their effects. 
	Both file formats can be arranged with either two rows or two columns."""  
	kttypeseper = "whitespace"
        """Similar to input data separation, the known-truth file has two options: whitespace or comma"""
        
	# Looping through command-line arguments to replace and/or create initialized values
	for o in opts:
		if o[0] in ("--help", "-h"):
			usage()
			sys.exit()
	for o in opts:
		if o[0] in ("--verbose", "-v"):
			verbose = True
			print ("Verbose mode\n")
	for o in opts:
		if o[0] in ("--Folder", "-F"):
			folder = str(o[1])
			if verbose:
				print "Folder of results files for validation is located in", folder
		if o[0] in ("--analysis", "-a"):
			analysis = str(o[1])
			if verbose:
				print "Analysis method being validated is specified as", analysis
		if o[0] in ("--Class", "-C"):
			truth = str(o[1])
			if verbose:
				print "Truth file is", truth
		if o[0] in ("--Snp", "-S"):
			snp = str(o[1])
			if verbose:
				print "SNP column name in results files is specified as", snp
		if o[0] in ("--Score", "-P"):
			score = str(o[1])
			if verbose:
				print "Scoring column name (e.g., p-value column) in results files is specified as", score
		if o[0] in ("--beta", "-b"):
			beta = str(o[1])
			if verbose:
				print "Estimated SNP Weight column name (e.g., regression betas) in results files is specified as", beta
		if o[0] in ("--filename", "-f"):
			filename = str(o[1])
			if verbose:
				print "Filename specified as", filename
		if o[0] in ("--threshold", "-t"):
			threshold = float(o[1])
			if verbose:
				print "Theshold is set at", threshold
		if o[0] in ("--seper", "-s"):
			seper = str(o[1])
			if verbose:
				print "Delimination of results files is set as", seper
		if o[0] in ("--kttype", "-k"):
			kttype = str(o[1])
			if verbose:
				print "Known-truth data format is set as", kttype
		if o[1] in ("--kttypeseper", "-r"):
			kttypeseper = str(o[1])
			if verbose:
				print "Known-truth data format delimination is set as", kttypeseper
		if o[1] in ("--severity", "-y"):
			severity = float(o[1])
			if verbose:
				print "Severity ratio is specified at", severity

	# Check to see if needed variables are defined
	try:
		folder
	except NameError:
		print "ERROR: Folder of results files to be validated must be specificed."
		usage()
		sys.exit()
	try:
		truth
	except NameError:
		print "ERROR: Known-truth data file must be supplied in order for results to be validated."
		usage()
		sys.exit()
	try:
		snp
	except NameError:
		print "ERROR: Name of SNP column in results files must be specified."
		usage()
		sys.exit()
	try:
		score
	except NameError:
		print "ERROR: Name of scoring column must be specified in order to validate SNP classifications."
		usage()
		sys.exit()

	"""Setting beta equal to null if not used; this will placehold the need to not run beta analyses
	NOTE: The beta corresponds to the effect size columns for SNPs found in the initial GWAS analysis"""
	try:
		beta
	except NameError:
		beta = None

	"""Severity ratio was originally included in the options for the proposed but unused H-measure fit statistic. Currently, the H-measure is not
	in the list of fit statistics, but once a formula can be implemented in Python, it will be shown in the command line options. 
	For now, we will leave this as the default None.""" 
	try:
		severity
	except NameError:
		severity = None

	return folder, analysis, truth, snp, score, beta, filename, threshold, seper, kttype, kttypeseper, severity
if __name__ == "__main__":
    import doctest
    doctest.testmod()
