#!/bin/bash

tar -xvf simuPOP-1.1.4-src.tar.gz
python ./simuPOP-1.1.4/setup.py -f --user

#Check, evaluate, and validate all of the arguments for Simulate
verbose=${verbose}
if [[ "${verbose}" == "1" ]]; then
	verbose="--verbose"
fi

distribution=${distribution}
if [[ -n distribution ]]; then
	distro="-d $distribution"
fi
size=${size}
number=${number}
if [ $distribution -eq 1 ]; then
	parameter1=" -p1 ${parameter1}"
	parameter2=" -p2 ${parameter2}"
else
	parameter1=""
	parameter2=""
fi
loci=${loci}
if [[ -n $loci ]]; then
	loci="-l $loci"
fi

effect=${effect}

mean=${mean}

generations=${generations}

heritability=${heritability}

recombination=${recombination}
if [[ -n $recombination ]]; then
	recombination=" -r ${recombination}"
fi

filename=${filename}
if [[ -n $filename ]]; then
	filename=" -f $filename"
fi
#Run the main program
python Simulate.py $verbose -d "$distro""$parameter1""$parameter2" -s "$size" -n "$number" -l "$loci" -e "$effect" -m "$mean" -i "$heritability" -g "$generations" "$recombination" -f "$filename"