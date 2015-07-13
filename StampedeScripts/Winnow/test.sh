#!/bin/bash
WRAPPERDIR=$( cd "$( dirname "$0" )" && pwd ) 
#SBATCH -p development
#SBATCH -t 00:30:00
#SBATCH -n 15
#SBATCH -A iPlant-Collabs 
#SBATCH -J test-winnow
knowntruth="$WRAPPERDIR/test/kt.ote"
Folder="$WRAPPERDIR/test/OutputPlink/"
SNP="SNP"
Score="P"
beta="BETA"
module load python/2.7.3-epd-7.3.2
tar xvzf winnow.tgz
#Now to execute the main program
python ./winpy/winnow.py --Folder $Folder --Class $knowntruth --Snp $SNP --Score $Score --beta $beta