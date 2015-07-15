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
nameP="${inputPED%.*}"
nameB="${inputBED%.*}"
nameT="${inputTPED%.*}"

if [ "$verboseOutput" = true ]; then
	verbose="-verboseOutput"
else
	verbose=
fi

re='^[0-9]+$'
if [[ -s "$inputPED" ]] && [[ -s "$inputMAP" ]]; then
	if [ "$SimFileset" != "PEDMAP" ]; then
		PEDMAP="-file $nameP"
	fi
else
	PEDMAP=
fi

if [ "$B" = true ]; then
	if [[ -s "$inputBED" ]] && [[ -s "$inputBIM" ]]; then
			if [ "$SimFileset" != "BEDBIMFAM" ]; then
				BEDBIMFAM="-bfile $nameB"
			fi
	fi
fi

if [ "$T" = true ]; then
	if [[ -s "$inputTPED" ]] && [[ -s "$inputTFAM" ]]; then
		if [ "$SimFileset" != "TPEDTFAM" ]; then
			TPEDTFAM="-tfile $nameT"
		fi
	fi
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

#Can remove this part later. For now, this checks to make sure all inputs are properly read before the program is executed
#Also, this will help in isolating errors when debugging
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
#Run the main program
./fastlmmc "$verbose" $PEDMAP $BEDBIMFAM $TPEDTFAM $pheno $COVAR $Sim $fileSIM $out