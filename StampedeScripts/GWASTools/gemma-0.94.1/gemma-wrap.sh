#!/bin/bash 
set -x
chmod +x ./gemma
inputBED=${inputBED}
inputBIM=${inputBIM}
inputFAM=${inputFAM}
Phenotype=${Phenotype}
Annotation=${Annotation}
MeanGenotype=${MeanGenotype}
RelatednessMatrix=${RelatednessMatrix}
RelatednessEigenvalue=${RelatednessEigenvalue}
RelatednessEigenvector=${RelatednessEigenvector}
Covariate=${Covariate}

#Now for the non-file parameters:

PLINK=${PLINK}
BIMBAM=${BIMBAM}
gk=${gk}
lmm=${lmm}
PhenotypeNumbers=${PhenotypeNumbers}
bslmm=${bslmm}
Type=${Type}
output=${output}

#Variable Validation for PLINK and BIMBAM formats:

if [ "$PLINK" = true ] ; then
	if [[ ! -e "$inputBED" ]]; then
		echo "ERROR: InputBED file was not found" >&2
		exit 1
	elif [[ ! -e "$inputBIM" ]]; then
		echo "ERROR: InputBIM file was not found" >&2
		exit 1
	elif [[ ! -e "$inputFAM" ]]; then
		echo "ERROR: InputFAM file was not found" >&2
		exit 1
	fi
elif [ "$BIMBAM" = true ] ; then
	if [[ ! -e "$MeanGenotype" ]]; then
		echo "ERROR: MeanGenotype file for BIMBAM format was not found" >&2
		exit 1
	elif [[ ! -e "$Phenotype" ]]; then
		echo "ERROR: Phenotype file for BIMBAM format was not found" >&2
		exit 1
	fi
elif [ "$PLINK" = true ] && [ "$BIMBAM" = true ] ; then
	echo "ERROR: You must only choose one file format for GEMMA analysis" >&2
	exit 1
else
	echo "ERROR: Either PLINK format or BIMBAM format must be set to true for GEMMA to analyze files" >&2
	exit 1
fi

#Check the other variables:
if [ "$gk" -lt 1 -o $gk -gt 2 ] ; then
   echo "error: Relatedness matrix option gk must an integer (either 1 or 2)" >&2; exit 1
fi

if [ "$lmm" -lt 1 -o -gt 4 ] ; then
	echo "ERROR: Mixed model option lmm must be an integer between 1 and 4 inclusive" >&2; exit 1
fi

PLINKfileset=${inputBED%.*}
#Check the type of analysis to be done
if [ "$Type" -lt 1 -o -gt 5 ] ; then
	echo "ERROR: The Type variable must be an integer between 1 and 5 (inclusive)" >&2; exit 1
fi

if [ "$Type" -eq 1 ] ; then
	if [ "$PLINK" = true ] ; then
		gemma -bfile "$PLINKfileset" -gk "$gk" -o "$output"
	elif [ "$BIMBAM" = true ] ; then
		gemma -g "$MeanGenotype" -p "$Phenotype" -gk "$gk" -o "$output"
	fi
elif [ "$Type" -eq 2 ] ; then
	if [ "$PLINK" = true ] ; then
		gemma -bfile "$PLINKfileset" -k "$RelatednessMatrix" -eigen -o "$output"
	elif [ "$BIMBAM" = true ] ; then
		gemma -g "$MeanGenotype" -p "$Phenotype" -k "$RelatednessMatrix" -eigen -o "$output"
	fi	
elif [ "$Type" -eq 3 ] ; then
	if [ "$PLINK" = true ] ; then
		gemma -bfile "$PLINKfileset" -k "$RelatednessMatrix" -lmm "$lmm" -o "$output"
	elif [ "$BIMBAM" = true ] ; then
		if [[ -n "$Annotation" ]] ; then
			gemma -g "$MeanGenotype" -p "$Phenotype" -a "$Annotation" -k "$RelatednessMatrix" -lmm "$lmm" -o "$output"
		else
			gemma -g "$MeanGenotype" -p "$Phenotype" -k "$RelatednessMatrix" -lmm "$lmm" -o "$output"
		fi
	fi
elif [ "$Type" -eq 4 ] ; then
	if [ "$PLINK" = true ] ; then
		gemma -bfile "$PLINKfileset" -k "$RelatednessMatrix" -num "$PhenotypeNumbers" -lmm "$lmm" -o "$output"
	elif [ "$BIMBAM" = true ] ; then
		if [[ -n "$Annotation" ]] ; then
			gemma -g "$MeanGenotype" -p "$Phenotype" -a "$Annotation" -k "$RelatednessMatrix" -num "$PhenotypeNumbers" -lmm "$lmm" -o "$output"
		else
			gemma -g "$MeanGenotype" -p "$Phenotype" -k "$RelatednessMatrix" -num "$PhenotypeNumbers" -lmm "$lmm" -o "$output"
		fi
	fi
elif [ "$Type" -eq 5 ] ; then
	if [ "$PLINK" = true ] ; then
		gemma -bfile "$PLINKfileset" -bslmm "$bslmm" -o "$output"
	elif [ "$BIMBAM" = true ] ; then
		if [[ -n "$Annotation" ]] ; then
			gemma -g "$MeanGenotype" -p "$Phenotype" -a "$Annotation" -bslmm "$bslmm" -o "$output"
		else
			gemma -g "$MeanGenotype" -p "$Phenotype" -bslmm "$bslmm" -o "$output"
		fi
	fi
fi	