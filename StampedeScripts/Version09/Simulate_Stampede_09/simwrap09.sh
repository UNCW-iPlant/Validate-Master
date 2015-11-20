#!/bin/bash

# May need to change these two commands to accommodate simuPOP install
tar -xvf simuPOP-1.1.4-src.tar.gz
python ./simuPOP-1.1.4/setup.py -f --user

#Check, evaluate, and validate all of the arguments for Simulate
verbose=${verbose}
distribution=${distribution}
size=${size}
number=${number}
loci=${loci}
effect=${effect}
mean=${mean}
generations=${generations}
heritability=${heritability}
OptArgs=""
parameter1=${parameter1}
parameter2=${parameter2}
recombination=${recombination}
filename=${filename}
if [ -n "$recombination" ]; then
	OptArgs="${OptArgs} -r $recombination"
fi

if [ -n "$parameter1" ]; then
	OptArgs="${OptArgs} -p1 $parameter1"
fi

if [ -n "$parameter2" ]; then
	OptArgs="${OptArgs} -p2 $parameter2"
fi

if [ -n "$filename" ]; then
	OptArgs"${OptArgs} -f $filename"
fi

#Run the main program
python Simulate.py -d $distribution -s $size -n $number -l $loci -e $effect -m $mean -g $generations -i $heritability $OptArgs