#!/bin/bash
chmod +x ./bayesR
bedInput=${inputBED}
bimInput=${inputBIM}
famInput=${inputFAM}
nameBED="${bedInput%.*}"
nameBIM="${bimInput%.*}"
nameFAM="${famInput%.*}"

ARGS="-out $output"

if [ "$nameBED" = "$nameBIM" ] && [ "$nameBED" = "$nameFAM" ]; then
	ARGS="${ARGS} -bfile $nameBED"
else
	echo "Input files need to have the same prefix"
fi

if [ -z ${n+x} ]; then
	echo "n is set to ${n}"
	ARGS="${ARGS} -n ${n}"
fi

if [ -z ${vara+x} ]; then
	echo "vara is set to ${vara}"
	ARGS="${ARGS} -vara ${vara}"
fi

if [ -z ${vare+x} ]; then
	echo "vare is set to ${vare}"
	ARGS="${ARGS} -vare ${vare}"
fi

if [ -z ${dfvara+x} ]; then
	echo "dfvara is set to ${dfvara}"
	ARGS="${ARGS} -dfvara ${dfvara}"
fi

if [ -z ${dfvare+x} ]; then
	echo "dfvare is set to ${dfvare}"
	ARGS="${ARGS} -dfvare ${dfvare}"
fi

if [ -z ${delta+x} ]; then
	echo "delta is set to ${delta}"
	ARGS="${ARGS} -delta ${delta}"
fi

if [ -z ${msize+x} ]; then
	echo "msize is set to ${msize}"
	ARGS="${ARGS} -msize ${msize}"
fi

if [ -z ${mrep+x} ]; then
	echo "mrep is set to ${mrep}"
	ARGS="${ARGS} -mrep ${mrep}"
fi
if [ -z ${numit+x} ]; then
	echo "numit is set to ${numit}"
	ARGS="${ARGS} -numit ${numit}"
fi

if [ -z ${burnin+x} ]; then
	echo "burnin is set to ${burnin}"
	ARGS="${ARGS} -burnin ${burnin}"
fi

if [ -z ${thin+x} ]; then
	echo "thin is set to ${thin}"
	ARGS="${ARGS} -thin ${thin}"
fi

if [ -z ${ndist+x} ]; then
	echo "ndist is set to ${ndist}"
	ARGS="${ARGS} -ndist ${ndist}"
fi

if [ -z ${seed+x} ]; then
	echo "seed is set to ${seed}"
	ARGS="${ARGS} -seed ${seed}"
fi

if [ -z ${predict+x} ] && [ "${predict}" -eq 1 ]; then
	echo "predict is set to true"
	ARGS="${ARGS} -predict"
fi

if [ -z ${snpout+x} ] && [ "${snpout}" -eq 1 ]; then
	echo "snpout is set to true"
	ARGS="${ARGS} -snpout"
fi

if [ -z ${permute+x} ] && [ "${permute}" -eq 1 ]; then
	echo "permute is set to true"
	ARGS="${ARGS} -permute"
fi

echo "Argument Line:"
echo "./bayesR ${ARGS}"

./bayesR ${ARGS}