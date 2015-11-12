#!/usr/bin/python
"""
A program for standardizing GWAS outputs to have matching column names.
This will make it easier to run all data through Winnow, 
and allows for files from multiple analysis tools to run simultaneously.
"""
import argparse
import os.path
import os
import pandas as pd
import csv

parser = argparse.ArgumentParser(description="List of command line arguments for input standardizer")
parser.add_argument("-v", "--verbose", action="store_true", help="Trigger verbose mode")
parser.add_argument("-f", "--folder", type=str, required=True, help="The folder of GWAS outputs to be standardized")
parser.add_argument("-s", "--Snpcols", type=str, nargs="+", required=True, help="The possible strings used for identifying the SNP column")
parser.add_argument("-p", "--Scorecols", type=str, required=True, nargs="+", help="The possible strings used for identifying the Score/P-value column")
parser.add_argument("-d", "--delimiter", choices=["whitespace","comma"], default="comma", help="Delimiter choice for standardized output")
parser.add_argument("-b", "--beta", type=str, default=None, nargs="+", help="Possible strings used for identifying an effect size, SNP weight, or beta column (if one exists)")
parser.add_argument("-c", "--covar", type=str, default=None, nargs="+", help="Possible strings used for identifying a covariate column (if one exists)")
args = parser.parse_args()

verbose = args.verbose
Folder = args.folder
Snpcols = list(args.Snpcols)
Scorecols = list(args.Scorecols)
delimiter = args.delimiter
if args.beta is not None:
    betacols = list(args.beta)
else:
    betacols = args.beta
if args.covar is not None:
    covarcols = list(args.covar)
else:
    covarcols = args.covar

# First, standardize column names
if verbose:
    print "Begin standardizing column names..."
filelist = os.listdir(Folder)
os.chdir(Folder)
if delimiter=="comma":
    seper=","
else:
    seper=" "
for one in filelist:
    if os.path.splitext(one)[1]==".txt":
        df = pd.read_table(os.path.abspath(one), header=0, delim_whitespace=True)
    elif os.path.splitext(one)[1]==".csv":
        df = pd.read_csv(os.path.abspath(one), header=0, sep=",")
    else:
        df = pd.read_table(os.path.abspath(one), header=0, delim_whitespace=True)
    df.rename(columns={name: 'SNP' for name in Snpcols}, inplace=True)
    df.rename(columns={name: 'PVAL' for name in Scorecols}, inplace=True)
    if betacols is not None:
        df.rename(columns={name: 'BETA' for name in betacols}, inplace=True)
    if covarcols is not None:
        df.rename(columns={name: 'COVAR' for name in covarcols}, inplace=True)
    if verbose:
        print "Rewriting file "+one+" with delimiter "+delimiter
    # Next, write everything to a regular file, delimited based on command line argument
    df.to_csv(os.path.abspath(one), sep=seper, index=False, header=True, quoting=csv.QUOTE_NONE)
if verbose:
    print "Standardization complete."
    print "All SNP column names rewritten to SNP"
    print "All score column names rewritten to PVAL"
    if betacols is not None:
        print "All effect size column names rewritten to BETA"
    if covarcols is not None:
        print "All covariate column names rewritten to COVAR"