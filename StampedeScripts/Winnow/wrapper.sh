#!/bin/bash

#Load the required arguments here
knowntruth=${Class}
Folder=${Folder}
SNP=${SNP}
Score=${Score}
kttype=${kttype}
filename=${Filename}
#Extra places for the optional arguments
verbose=${verbose}
threshold=${threshold}
beta=${beta}
seper=${seper}
kttypeseper=${kttypeseper}
OptArgs=""

# Boolean handler for --verbose mode
if [ $verbose -eq 1 ]; then 
	OptARGS="$OptARGS--verbose"
else OptARGS="$OptARGS"
fi

if [ -n "$threshold" ]; then 
	OptARGS="${OptARGS} --threshold $threshold"; 
fi

if [ -n "$beta" ]; then 
	OptARGS="${OptARGS} --beta $beta" 
fi

if [ -n "$seper" ]; then 
	OptARGS="${OptARGS} --seper $seper" 
fi

if [ -n "$kttypeseper" ]; then 
	OptARGS="${OptARGS} --kttypeseper $kttypeseper"
fi

#Print each of the arguments to make sure everything is being read correctly
echo "knowntruth=$knowntruth"
echo "Folder=$Folder"
echo "SNP=$SNP"
echo "Score=$Score"
echo "kttype=$kttype"
echo "filename=$filename"
echo "verbose=$verbose"
echo "threhsold=$threshold"
echo "seper=$seper"
echo "kttypeseper=$kttypeseper"
echo "beta=$beta"
echo python ./winpy/winnow.py --Folder $Folder --Class $knowntruth --Snp $SNP --Score $Score --kttype $kttype --filename $filename $OptARGS

python ./winpy/winnow.py --Folder $Folder --Class $knowntruth --Snp $SNP --Score $Score --kttype $kttype --filename $filename $OptARGS