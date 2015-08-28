#required to allow executing the program
chmod +x qxpak.linux64
WRAPPERDIR="$( cd "$( dirname "$0" )" && pwd )"

#required files
inputPed=${pedigree_file}
inputMkr=${marker_file}
inputDat=${data_file}
inputPar=${parameter_file}
#Desired name for output
output=${output}
# Run the actual program
echo $inputPed
echo $inputMkr
echo $inputDat
echo $inputPar
python qxpakwrapper.py -p $inputPar -d $inputDat -m $inputMkr -g $inputPed -o $output