#!/bin/bash
WRAPPERDIR=$( cd "$( dirname "$0" )" && pwd ) 

#Load the required arguments here and check if they exist

truth=${knowntruth}
if [[ ! -e "$truth" ]]; then
	echo "Known truth file was not found" >&2
	exit 1
fi

inputFolder=${GWASResults}
if [[ ! -e "$inputFolder" ]]; then
	echo "Input folder was not found" >&2
	exit 1
fi

SNPname=${SNPcolname}
if [[! -n "$SNPname" ]]; then
	echo "Name for SNP column is required" >&2
	exit 1
fi

Score=${Pvalcolname}
if [[! -n "$Score" ]]; then
	echo "Name for significance/p-value column is required" >&2
	exit 1
fi

kttype=${truthtype}
if [["$kttype"!="OTE" -o "$kttype"!="FGS" ]]; then
	echo "Known-truth file type not accepted" >&2
	exit 1
fi

#Extra places for the optional arguments and checking their existence

if [[ "${verbose}" == "1" ]]; then
	VERBOSE="--verbose"
fi

threshold=${Siglevel}
if [[ -n "$threshold" ]]; then
	THRESH="--threshold ${threshold}"	
fi

beta=${effect}
if [[ -n "$beta" ]]; then
	BETA="--beta ${beta}"	
fi

seper=${delim}
if [[ -n "$seper" ]]; then
	if [[ "$seper"=="whitespace" -o "$seper"=="comma" ]]; then 
		SPACER="--seper ${seper}"
	fi	
fi

truthseper=${truthseper}
if [[ -n "$kttype" ]]; then
	if [[ "$truthseper"=="whitespace" -o "$truthseper"=="comma" ]]; then 
		KTSPACER="--kttypeseper ${seper}"
	fi	
fi

#Load the Enthought distribution for Python to get the necessary packages
module load python/2.7.3-epd-7.3.2

tar xvzf winnow.tgz

outdir="$WRAPPERDIR/Winnow_output"
mkdir -p "$outdir"

#Now to execute the main program...
python $WRAPPERDIR/winpy/winnow.py ${VERBOSE} --Folder "${inputFolder}" --Class "${truth}" --SNP "${SNPname}" --Score "${Score}" --kttype "${THRESH}" "${BETA}" "${SPACER}" "${KTSPACER}"