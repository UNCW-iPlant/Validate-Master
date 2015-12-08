#!/bin/bash
chmod +x ./bayesR
bedInput=${bedInput}
bimInput=${bimInput}
famInput=${famInput}
output=${output}

nameBED="${bedInput%.*}"
nameBIM="${bimInput%.*}"
nameFAM="${famInput%.*}"

if [ "$nameBED" = "$nameBIM" ] && [ "$nameBED" = "$nameFAM" ]; then
	input="-bfile $nameBED"
else
	echo "Input files need to have the same prefix"
fi

./bayesR $input -out $output