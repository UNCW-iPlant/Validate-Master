#!/bin/bash
verbose=true
if [ $verbose = true ] ; then
	verbose="--verbose"
distribution=1
parameter1=3
parameter2=1.5
size=1000
number=3000
loci=0
effect=0.6
mean=2.7
generations=100
heritability=0.3
recombination=0

filename="~/Desktop/Test"
bash sim-wrapper.sh 

#Now to execute the main program...

python Simulate.py "$verbose" -d "$distribution" -p1 "$parameter1" -p2 "$parameter2" -s "$size" -n "$number" -l "$loci" -e "$effect" -m "$mean" -g "$generations" -i "$heritability" -r "$recombination" -f "$filename"