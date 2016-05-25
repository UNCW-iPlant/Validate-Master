#Merger
Used for combining outputs from various applications so that they can be used in Winnow and/or the GWAS tools.
####General Arguments
`--help / -h` Displays the help menu

`--verbose / -v` Triggers verbose mode

`--output / -o` Specifies the output file(s) prefix (optional; defaulted to 'merged_output')

##BayesR
Used to combine the information from the input BIM file and the output PARAM file.
####BayesR Arguments
`--bim / -b` Specifies the BIM file used as input for BayesR (required)

`--param / -p` Specifies the PARAM file received as output from BayesR (required)
#####BayesR Example
`python Merge.py --output bayesR_Example bayesr --bim simdata.bim --param simout.param`

##AlphaSim
Used to convert the outputs of AlphaSim into the PEDMAP format.
####AlphaSim Arguments
`--snp / -s` Specifies the SNP information output file from AlphaSim (required)

`--pedigree / -p` Specifies the PedigreeTbvTdvTpv output file from AlphaSim (required)

`--col / -c` Specifies the phenotype column from the pedigree file (optional; defaulted to 9 for the TPVNormRest1 column)

`--gender / -g` Specifies the gender output file from AlphaSim (required)

`--geno / n` Specifies the genotype output file from AlphaSim (required)

`--sol / -k` Specifies the SNP solution output file from AlphaSim (optional). If this is used, the phenotype values found in this file will be used rather than the ones found in the pedigree file.
#####AlphaSim Example
`python Merge.py --output AlphaSim_Example alphasim --snp SnpInformation.txt --pedigree PedigreeTbcTdvTpv.txt --col 9 --gender Gender.txt --geno Chip1Genotype.txt --sol SnpSolutions.txt`

##Launcher
Used to combine output from Winnow when the parametric launcher is used.
####Launcher Arguments
`--folder / -f` Specifies the folder containing the Winnow outputs to be combined.
#####Launcher Example
`python Merge.py --output Launcher_Example launcher --folder TestData/`