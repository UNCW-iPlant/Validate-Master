#!/bin/bash
verbose=true
if [ $verbose = true ] ; then
	verbose="--verbose"
fi
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

filename="Test"
. ./simwrap.sh 