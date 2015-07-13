#!/bin/bash
chmod +x ./fastlmmc
#Read in whatever input PLINK files exist
#Will validate them after reading everything in
inputPED=${inputPED}
inputMAP=${inputMAP}
inputTPED=${inputTPED}
inputTFAM=${inputTFAM}
inputBED=${inputBED}
inputBIM=${inputBIM}
inputFAM=${inputFAM}

#Read in the other input files here
Sim=${Sim}
inputPHENO=${inputPHENO}
inputCOVAR=${inputCOVAR}

#Now for the non-file parameters:

verboseOutput=${verboseOutput}
C=${C}
B=${B}
SimFileset=${SimFileset}
mpheno=${mpheno}
T=${T}
output=${output}

#Variable Validation:

if [ "$verboseOutput" = true ]; then
	verbose="-verboseOutput"
else
	verbose=
fi

re='^[0-9]+$'
if [[ -s "$inputPED" ]] && [[ -s "$inputMAP" ]]; then
	nameP="${inputPED%.*}"
	if [ "$SimFileset" != "PEDMAP" ]; then
		PEDMAP="-file $nameP"
	fi
else
	PEDMAP=
fi


if [ "$B" = true ]; then
	if [[ -s "$inputBED" ]] && [[ -s "$inputBIM" ]]; then
		nameB="${inputBED%.*}"
			if [ "$SimFileset" != "BEDBIMFAM" ]; then
				BEDBIMFAM="-bfile $nameB"
			fi
	fi
else
	BEDBIMFAM=
fi

if [ "$T" = true ]; then
	if [[ -s "$inputTPED" ]] && [[ -s "$inputTFAM" ]]; then
		nameT="${inputTPED%.*}"
		if [ "$SimFileset" != "TPEDTFAM" ]; then
			TPEDTFAM="-tfile $nameT"
		fi
	else
		TPEDTFAM=
	fi
fi

if [[ -z "$inputPHENO" ]]; then
	echo "ERROR: Phenotype file is required for analysis" >&2; exit 1
else
	pheno="-pheno $inputPHENO"
fi


if [ "$C" = true ]; then
	if [[ -s "$inputCOVAR" ]]; then
		COVAR="-covar $inputCOVAR"
	else
		echo "WARNING: C option set to true. Expecting covariate input, but none found."
	fi
fi

if  [[ -n "$SimFileset" ]]; then
	if [ "$SimFileset" == "PEDMAP" ]; then
		fileSIM="-fileSim $nameP"
	elif [ "$SimFileset" == "BEDBIMFAM" ]; then
		fileSIM="-bfileSim $nameB"
	elif [ "$SimFileset" == "TPEDTFAM" ]; then
		fileSIM="-tfileSim $nameT"
	else
		echo "ERROR: SimFileset option specified, but no files found." >&2; exit 1
	fi
fi

if  [[ ! -e "$Sim" ]] && [ -z "$SimFileset" ]; then
	echo "ERROR: Unable to compute genetic similarity matrix. A PLINK fileset for computation or the actual genetic similarity matrix file is required" >&2; exit 1
fi

if  [ -z "$output" ]; then
	echo "ERROR: String for output is required" >&2; exit 1
else
	out="-out $output"
fi

#Run the main program
echo "$inputPED"
echo "verbose: $verbose"
echo "PEDMAP: $PEDMAP"
echo "BEDBIMFAM: $BEDBIMFAM"
echo "TPEDTFAM: $TPEDTFAM"
echo "pheno: $pheno"
echo "COVAR: $COVAR"
echo "Sim: $Sim"
echo "fileSIM: $fileSIM"
echo "output: $out"
./fastlmmc "$verbose" $PEDMAP $BEDBIMFAM $TPEDTFAM $pheno $COVAR $Sim $fileSIM $out