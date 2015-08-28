#!/bin/bash 
set -x
chmod +x gemma
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
PLINKfileset=${inputBED%.*}
#Variable Validation for PLINK and BIMBAM formats:

if [ "$PLINK" -eq 1 ] ; then
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
elif [ "$BIMBAM" -eq 1 ] ; then
	if [[ ! -e "$MeanGenotype" ]]; then
		echo "ERROR: MeanGenotype file for BIMBAM format was not found" >&2
		exit 1
	elif [[ ! -e "$Phenotype" ]]; then
		echo "ERROR: Phenotype file for BIMBAM format was not found" >&2
		exit 1
	fi
fi



echo "PLINK: $PLINK"
echo "BIMBAM: $BIMBAM"
echo "gk: $gk"
echo "lmm: $lmm"
echo "Phenotype Numbers: $PhenotypeNumbers"
echo "bslmmm: $bslmm"
echo "Type: $Type"
echo "output: $output"
echo "PLINKfileset: $PLINKfileset"
#Check the type of analysis to be done

if [ "$Type" -eq 1 ] ; then
	if [ "$PLINK" -eq 1 ] ; then
		gemma -bfile "$PLINKfileset" -gk "$gk" -o "$output"
	elif [ "$BIMBAM" -eq 1 ] ; then
		gemma -g "$MeanGenotype" -p "$Phenotype" -gk "$gk" -o "$output"
	fi
elif [ "$Type" -eq 2 ] ; then
	if [ "$PLINK" -eq 1 ] ; then
		gemma -bfile "$PLINKfileset" -k "$RelatednessMatrix" -eigen -o "$output"
	elif [ "$BIMBAM" -eq 1 ] ; then
		gemma -g "$MeanGenotype" -p "$Phenotype" -k "$RelatednessMatrix" -eigen -o "$output"
	fi	
elif [ "$Type" -eq 3 ] ; then
	if [ "$PLINK" -eq 1 ] ; then
		gemma -bfile "$PLINKfileset" -k "$RelatednessMatrix" -lmm "$lmm" -o "$output"
	elif [ "$BIMBAM" -eq 1 ] ; then
		if [[ -n "$Annotation" ]] ; then
			gemma -g "$MeanGenotype" -p "$Phenotype" -a "$Annotation" -k "$RelatednessMatrix" -lmm "$lmm" -o "$output"
		else
			gemma -g "$MeanGenotype" -p "$Phenotype" -k "$RelatednessMatrix" -lmm "$lmm" -o "$output"
		fi
	fi
elif [ "$Type" -eq 4 ] ; then
	if [ "$PLINK" -eq 1 ] ; then
		gemma -bfile "$PLINKfileset" -k "$RelatednessMatrix" -num "$PhenotypeNumbers" -lmm "$lmm" -o "$output"
	elif [ "$BIMBAM" -eq 1 ] ; then
		if [[ -n "$Annotation" ]] ; then
			gemma -g "$MeanGenotype" -p "$Phenotype" -a "$Annotation" -k "$RelatednessMatrix" -num "$PhenotypeNumbers" -lmm "$lmm" -o "$output"
		else
			gemma -g "$MeanGenotype" -p "$Phenotype" -k "$RelatednessMatrix" -num "$PhenotypeNumbers" -lmm "$lmm" -o "$output"
		fi
	fi
elif [ "$Type" -eq 5 ] ; then
	if [ "$PLINK" -eq 1 ] ; then
		gemma -bfile "$PLINKfileset" -bslmm "$bslmm" -o "$output"
	elif [ "$BIMBAM" -eq 1 ] ; then
		if [[ -n "$Annotation" ]] ; then
			gemma -g "$MeanGenotype" -p "$Phenotype" -a "$Annotation" -bslmm "$bslmm" -o "$output"
		else
			gemma -g "$MeanGenotype" -p "$Phenotype" -bslmm "$bslmm" -o "$output"
		fi
	fi
fi	