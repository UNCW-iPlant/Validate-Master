#!/bin/bash
WRAPPERDIR=$( cd "$( dirname "$0" )" && pwd )
#SBATCH -p development
#SBATCH -t 00:30:00
#SBATCH -n 15
#SBATCH -A iPlant-Collabs 
#SBATCH -J test-bayesR
inputBED="$WRAPPERDIR/test_data/simdata.bed"
inputBIM="$WRAPPERDIR/test_data/simdata.bim"
inputFAM="$WRAPPERDIR/test_data/simdata.fam"
output="bayesRTest.txt"

. ./wrapper.sh
