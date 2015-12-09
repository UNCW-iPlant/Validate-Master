#!/bin/bash
#SBATCH -p development
#SBATCH -t 00:30:00
#SBATCH -n 15
#SBATCH -A iPlant-Collabs 
#SBATCH -J test-bayesR
inputBED="test_data/simdata.bed"
inputBIM="test_data/simdata.bim"
inputFAM="test_data/simdata.fam"
output="bayesRTest.txt"

. ./wrapper.sh
