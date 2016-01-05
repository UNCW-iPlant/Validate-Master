#!/usr/bin/python
# Script for merging launcher outputs into a single file
import argparse
import os
import os.path
import pandas as pd
import numpy as np

def main():
    # Read in command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--folder',help="The folder containing all GWAS outputs")
    parser.add_argument('-o','--output',help="The name of the output file for your merged results")
    args = parser.parse_args()
    folder = args.folder
    outname = args.output
    
    # First, read in the list of filenames
    os.chdir(folder)
    filelist = os.listdir(os.path.abspath(folder))
    
    # Next, read in column headers from initial file
    initial_data = pd.read_table(filelist[0], sep="\t", header=0)
    colnames = initial_data.columns.values.tolist()
    
    # Finally, write the file in which the results will be combined
    with open(outname+".txt",mode="w") as final_file:
        final_file.write('\t'.join(colnames)+'\n')
        for name in filelist:
            data = pd.read_table(name, sep="\t",header=0)
            vals = map(str, data.values.tolist()[0])
            final_file.write('\t'.join(vals)+'\n')

if __name__ == "__main__":
    main()
