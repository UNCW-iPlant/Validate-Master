# -*- coding: utf-8 -*-
""" 
Functions for indentifying and using the command-line to execute Winnow for Python
"""


# Dependencies
import argparse


# Functions to be used later in the software
def initializeGraphics():
    """Prints introduction graphics for every time the software is run"""

    print "###################################################################"
    print "###                                                            ####"
    print "###      Winnow for Python!                                    ####"
    print "###      By Dustin A. Landers                                  ####"
    print "###      Contact: (770) 289-8830 -- dustin.landers@gmail.com   ####"
    print "###                                                            ####"
    print "###################################################################"


def checkArgs():
    """Checks for arguments at beginning of the execution of the main function"""
    parser = argparse.ArgumentParser(description="Winnow command line arguments")
    parser.add_argument("-v", "--verbose", help="Trigger verbose mode", action="store_true")
    parser.add_argument("-a", "--analysis", nargs='?',
                        help="The type of analysis for Winnow to perform (currently, only GWAS is supported)",
                        default="GWAS", type=str, choices=["GWAS"])
    parser.add_argument("-F", "--Folder", required=True, type=str, help="The input folder of box results")
    parser.add_argument("-C", "--Class", required=True, type=str, help="The known-truth file for used simulation")
    parser.add_argument("-S", "--Snp", required=True, type=str, help="The name of the SNP column in results file")
    parser.add_argument("-P", "--Score", required=True, type=str,
                        help="The name of the scoring column in results file (e.g. p-value)")
    parser.add_argument("-b", "--beta", type=str, help="Name of the estimated SNP effect column in results file")
    parser.add_argument("-f", "--filename", type=str, default="Results",
                        help="The desired filename for the Winnow output file")
    parser.add_argument("-t", "--threshold", type=float, default=0.05,
                        help="A desired threshold for classification performetrics where necessary")
    parser.add_argument("-s", "--seper", type=str, choices=["comma", "whitespace", "tab"], default="whitespace",
                        help="Delimiter for box results")
    parser.add_argument("-k", "--kttype", type=str, required=True, choices=["OTE", "FGS"], default="OTE",
                        help="The type of known-truth file for --Class. OTE is only truth and effect, and FGS is full genome set")
    parser.add_argument("-r", "--kttypeseper", choices=["comma", "whitespace", "tab"], nargs='?', default="whitespace",
                        help="Specify delimitation in known-truth file")
    parser.add_argument("-y", "--severity", type=float, default=None, nargs='?',
                        help="Severity ratio used in the h-measure calculation (currently not available, can leave blank)")
    adjust_methods=["bonferroni", "sidak", "holm-sidak", "holm", "simes-hochberg", "hommel", "fdr_bh","fdr_by","fdr_tsbh","fdr_tsbky"]
    parser.add_argument("-p", "--pvaladjust", default=None, nargs='?', choices=adjust_methods, help="Specify the type of p-value adjustment (not case sensitive)")
    """
            Explanation of p-value adjustment methods:
                -bonferroni: one-step Bonferroni method
                -sidak: one-step Sidak method
                -holm-sidak: step down method using Sidak adjustments
                -holm: step down method using Bonferroni adjustments
                -simes-hochberg: step down method (for independent statistics)
                -hommel: closed method based on Simes procedure (non-negatively associated statistics only)
                -fdr_bh: Benjamini-Hochberg method for false discovery rate control (non-negatively associated or independent statistics only)
                -fdr_by: Benjamini-Yekutieli method for false discovery rate control
                -fdr_tsbh: Two-stage FDR control (non-negatively associated or independent statistics only) 
                -fdr_tsbky: Two-stage FDR control
            
            P-value adjustment algorithms are those created by Holm (1979), Hochberg (1988), 
            Hommel (1988), Benjamini & Hochberg (1995), and Benjamini & Yekutieli (2001).
    """
    parser.add_argument("-c", "--covar", default=None, help="The name of the covariate column from results file")
    parser.add_argument("-o", "--savep", default=False, action="store_true",
                        help="Saves P-values in a text file if specified")
    args = parser.parse_args()

    """Change command line arguments into variables to pass along to the rest of the program"""
    verbose = args.verbose
    folder = args.Folder
    analysis = args.analysis
    truth = args.Class
    snp = args.Snp
    score = args.Score
    beta = args.beta
    filename = args.filename
    threshold = args.threshold
    seper = args.seper
    kttype = args.kttype
    kttypeseper = args.kttypeseper
    severity = args.severity
    if args.pvaladjust==None:
        pvaladjust = None
    else:
        pvaladjust = args.pvaladjust.lower()
    covar = args.covar
    savep = args.savep
    
    if pvaladjust not in adjust_methods and pvaladjust is not None:
        print 'P-value adjustment method given is not supported. The original p-values will be used instead.'
        pvaladjust=None
    
    if verbose:
        print "\nVerbose mode"
        print "Analysis method for being validated is specified as", analysis
        print "Folder of results files for validation is located in", folder
        print "Truth file is", truth
        print "SNP column name in results files is specified as", snp
        print "Scoring Column name (e.g. p-value column) in results files is specified as", score
        print "Estimated SNP weight column name (e.g. regression betas) in results files is specified as", beta
        print "Filename specified as", filename
        print "Threshold is set at", threshold
        print "Delimination of results files is set as", seper
        print "Known-truth data format is set as", kttype
        print "Known-truth delimiter is set as", kttypeseper
        print "Severity ratio is specified at", severity
        print "P-value adjustment is set as", pvaladjust
        print "Covariate column is specified as", covar
        if savep:
            print "Saving p-values..."

    return folder, analysis, truth, snp, score, beta, filename, \
           threshold, seper, kttype, kttypeseper, severity, pvaladjust, covar, savep


if __name__ == "__main__":
    import doctest
    doctest.testmod()
