#!/bin/bash
WRAPPERDIR=$( cd "$( dirname "$0" )" && pwd ) 
#Grab the args for Simulate; validation is done by regular expressions from the JSON file
verbose=${verbose}
if [[ "${verbose}" == "1" ]]; then
	verbose="--verbose"
fi
distribution=${distribution}
size=${size}
number=${number}
parameter1=${parameter1}
parameter2=${parameter2}
loci=${loci}
effect=${effect}
mean=${mean}
generations=${generations}
heritability=${heritability}
recombination=${recombination}
filename=${filename}

#Need to add a bit about installing simuPOP

#Make directories for the output
outdir="$WRAPPERDIR/Sim_out/"
mkdir -p "$outdir"

#Now to execute the main program...
python ./Simulate.py $verbose -d "$distribution" -p1 "$parameter1" -p2 "$parameter2" -s "$size" -n "$number" -l "$loci" -e "$effect" -m "$mean" -i "$heritability" -g "$generations" -r "$recombination" -f "$outdir/$filename"