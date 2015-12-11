#!/bin/bash
chmod +x ./bayesR

bedInput=${inputBED}
bimInput=${inputBIM}
famInput=${inputFAM}
nameBED="${bedInput%.*}"
nameBIM="${bimInput%.*}"
nameFAM="${famInput%.*}"
ARGS="-out ${output}"


if [ "$nameBED" = "$nameBIM" ] && [ "$nameBED" = "$nameFAM" ]; then
	ARGS="${ARGS} -bfile $nameBED"
else
	echo "Input files need to have the same prefix"
fi

if [ -z "${n}" ]; then
	echo "n not set"
else 
	echo "n set to ${n}"
	ARGS="${ARGS} -n ${n}"
fi

if [ -z ${vara} ]; then
	echo "vara not set"
else
	echo "vara is set to ${vara}"
	ARGS="${ARGS} -vara ${vara}"
fi

if [ -z ${vare} ]; then
	echo "vare not set"
else
	echo "vare is set to ${vare}"
	ARGS="${ARGS} -vare ${vare}"
fi

if [ -z ${dfvara} ]; then
	echo "dfvara not set"
else
	echo "dfvara is set to ${dfvara}"
	ARGS="${ARGS} -dfvara ${dfvara}"
fi

if [ -z ${dfvare} ]; then
	echo "dfvare not set"
else
	echo "dfvare is set to ${dfvare}"
	ARGS="${ARGS} -dfvare ${dfvare}"
fi

if [ -z ${delta} ]; then
	echo "delta not set"
else
	echo "delta is set to ${delta}"
	ARGS="${ARGS} -delta ${delta}"
fi

if [ -z ${msize} ]; then
	echo "msize not set"
else
	echo "msize is set to ${msize}"
	ARGS="${ARGS} -msize ${msize}"
fi

if [ -z ${mrep} ]; then
	echo "mrep not set"
else
	echo "mrep is set to ${mrep}"
	ARGS="${ARGS} -mrep ${mrep}"
fi

if [ -z ${numberit} ]; then
	echo "numit not set"
else
	echo "numit is set to ${numberit}"
	ARGS="${ARGS} -numit ${numberit}"
fi

if [ -z ${burnin} ]; then
	echo "burnin not set"
else
	echo "burnin is set to ${burnin}"
	ARGS="${ARGS} -burnin ${burnin}"
fi

if [ -z ${thin} ]; then
	echo "thin not set"
else
	echo "thin is set to ${thin}"
	ARGS="${ARGS} -thin ${thin}"
fi

if [ -z ${ndist} ]; then
	echo "ndist not set"
else
	echo "ndist is set to ${ndist}"
	ARGS="${ARGS} -ndist ${ndist}"
fi

if [ -z ${seed} ]; then
	echo "seed not set"
else
	echo "seed is set to ${seed}"
	ARGS="${ARGS} -seed ${seed}"
fi

if [ -z ${predict} ]; then
	echo "predict not set"
else
	if [ "${predict}" -eq 1 ]; then
		echo "predict is set to true"
		ARGS="${ARGS} -predict"
	fi
fi

if [ -z ${snpout} ]; then
	echo "snpout not set"
else
	if [ "${snpout}" -eq 1 ]; then
		echo "snpout is set to true"
		ARGS="${ARGS} -snpout"
	fi
fi

if [ -z ${permute} ]; then
	echo "permute not set"
else
	if [ "${permute}" -eq 1 ]; then
		echo "permute is set to true"
		ARGS="${ARGS} -permute"
	fi
fi

echo "Argument Line:"
echo "./bayesR ${ARGS}"
echo "Starting bayesR"
./bayesR ${ARGS}