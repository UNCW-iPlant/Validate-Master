#!/bin/bash
#Check, evaluate, and validate all of the arguments for Simulate
verbose=${verbose}
if [[ "${verbose}" == "1" ]]; then
	verbose="--verbose"
fi

distribution=${distribution}
if [[ "${distribution}" != 0 -o "${distribution}" != 1  ]]; then
	echo "Distribution option must be either 0 or 1!"
	exit 1
fi

size=${size}
#Need to add list validation here

reg1=^[0-9]+$
if ! [[ "${size}" =~ $reg1 ]]; then
	echo "Size variable must be integer!"
	exit 1
fi

number=${number}
if ! [[ "${number}" =~ $reg1 ]]; then
		echo "Number of loci must be an integer value!"
		exit 1
fi

parameter1=${parameter1}
reg2=^[0-9]+(\.[0-9]{1,2})?$
if ! [[ ${parameter1} =~ $reg2 ]]; then
	echo "Alpha paramter must be a decimal number or integer."
	exit 1
fi

parameter2=${parameter2}
if ! [[ ${parameter2} =~ $reg2 ]]; then
	echo "Beta parameter must be a decimal number or integer."
	exit 1
fi

loci=${loci}
#Need to add in validation here just to make sure. 

effect=${effect}
#Same goes for this variable

mean=${mean}
if ! [[ ${mean} =~ $reg2 ]]; then
	echo "Population mean must be a decimal number or integer."
	exit 1
fi

generations=${generations}
if ! [[ generations =~ $reg1 ]]; then
	echo "ERROR: Number of generations must be an integer!" >&2; exit 1
else
fi

heritability=${heritability}
gt=$(echo "$heritability < 1" | bc -q )
# return 1 if true ; O if not
if [ $gt = 1 ]
then
	:
else
   echo "ERROR: Recombination rate must be between 0 and 1"
fi

recombination=${recombination}

gt=$(echo "$recombination < 1" | bc -q )
# return 1 if true ; O if not
if [ $gt = 1 ]
then
	:
else
   echo "ERROR: Recombination rate must be between 0 and 1"
fi

filename=${filename}
if [[ -n "$kttype" ]]; then
	if [[ "$truthseper"=="whitespace" -o "$truthseper"=="comma" ]]; then 
		KTSPACER="--kttypeseper ${seper}"
	fi	
fi

#Load the Enthought distribution for Python to get the necessary packages
module load python

#Download and install simuPOP
wget sourceforge.net/projects/simupop/files/simupop/1.1.4/simuPOP-1.1.4-src.tar.gz


#Make directories for the output
outdir="$WRAPPERDIR/Sim_out"
mkdir -p "$outdir"

#Now to execute the main program...
python Simulate.py $verbose -d "$distribution" -p1 "$parameter1" -p2 "$parameter2" -s "$size" -n "$number" -l "$loci" -e "$effect" -m "$mean" -i "$heritability" -g "$generations" -r "$recombination" -f "$filename"