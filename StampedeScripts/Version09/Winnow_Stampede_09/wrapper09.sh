#!/bin/bash

#Load the required arguments here
knowntruth=${Class}
Folder=${Folder}
SNP=${SNP}
Score=${Score}
kttype=${kttype}
filename=${Filename}
#Extra places for the optional arguments
threshold=${threshold}
beta=${beta}
seper=${seper}
kttypeseper=${kttypeseper}
Pvaladjust=${Pvaladjust}
covar=${covar}
savep=${savep}
OptArgs=""

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

if [ -n "$Pvaladjust" ]; then
	OptARGS="${OptARGS} --pvaladjust $Pvaladjust"
fi

if [ -n "$covar" ]; then 
	OptARGS="${OptARGS} --covar $covar"
fi

if [ $savep -eq 1 ]; then 
	OptARGS="${OptARGS} --savep"
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
echo "pvaladjust=$Pvaladjust"
echo python ./winpy/winnow.py --Folder $Folder --Class $knowntruth --Snp $SNP --Score $Score --kttype $kttype --filename $filename $OptARGS

python ./winpy/winnow.py --Folder $Folder --Class $knowntruth --Snp $SNP --Score $Score --kttype $kttype --filename $filename $OptARGS