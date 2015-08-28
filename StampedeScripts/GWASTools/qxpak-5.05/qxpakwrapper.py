#! /usr/bin/python
#
# Qxpak Wrapper
# http://www.iplantcollaborative.org/
#
# A versatile mixed model application for genetical genomics
# http://www.icrea.cat/Web/OtherSectionViewer.aspx?key=485&titol=Software:Qxpak
#
# See usage file for details.
#
# HISTORY
# v1.0   July 2011
#        Jason Vandeventer, University of North Carolina Wilmington
#        Created.
# v1.1   May 17, 2012
#        Phillip Walker, University of North Carolina Wilmington
#        Changed output parameter file to a temporary file; included
#        additional documentation, usage printing, and error handling.

import sys
import os
import getopt
import re

# Prints the appropriate usage and documentation for this program
# using an external text file, specifically usage.txt.
def usage():
    filename = sys.argv[0] + "_usage.txt"
    if os.path.exists(filename):
        print open(filename).read()
    else:
        print "No usage information found (" + filename + " is missing)"
        
# Print an error message and optionally the usage information. Then
# terminate, returning an error level to the operating system.
def bomb(message, showUsage = False):
    print "Error: " + message
    if showUsage:
        print
        usage()
    sys.exit(2)

def replace_words(text, word_dic):
    rc = re.compile('|'.join(map(re.escape, word_dic)))
    def translate(match):
        return word_dic[match.group(0)]
    return rc.sub(translate, text)

def main(argv):
    #Instantiate each file with empty string. If it doesn't exist, it shouldn't be used    
    parameterFile = dataFile = pedigreeFile = markerFile = userInverseFile = userDirectFile = haplotypeFile = outputFile = ""
    
    try:
        opts, args = getopt.getopt(argv, "p:d:g:m:i:t:h:o:", ["par=", "data=", "ped=", "mkr=", "uinv=", "udir=", "haplo=", "output="])
    except getopt.GetoptError:
        bomb("Invalid options", True)
    for opt, arg in opts:
        if opt in ("-p", "--par"):
            parameterFile = arg
        elif opt in ("-d", "--data"):
            dataFile = arg
        elif opt in ("-g", "--ped"):
            pedigreeFile = arg
        elif opt in ("-m", "--mkr"):
            markerFile = arg
        elif opt in ("-i", "--uinv"):
            userInverseFile = arg
        elif opt in ("-t", "--udir"):
            userDirectFile = arg
        elif opt in ("-h", "--haplo"):
            haplotypeFile = arg
        elif opt in ("-o", "--output"):
            outputFile = arg


    # Read the file
    if parameterFile == "":
        bomb("You must supply a parameter file (-p option)", True)
    try:
        fin = open(parameterFile, "r")
        parFile = fin.read()
        fin.close()
    except IOError as (errno, strerror):
        bomb("{0}: {1} (I/O error {2})".format(parameterFile, strerror, errno))
    
    # Dictionary target_word:replacement_word pairs
    word_dic = {
    '$data': "" + dataFile,
    '$pedigree': "" + pedigreeFile,
    '$marker': "" + markerFile,
    '$userInverse': "" + userInverseFile,
    '$userDirect': "" + userDirectFile,
    '$haplotype': "" + haplotypeFile,
    '$output': "" + outputFile
    }

    # Call the function and get changed text
    newParFile = replace_words(parFile, word_dic)

    # write changed text out
    tmpParameterFile = os.path.basename(parameterFile) + ".tmp"
    fout = open(tmpParameterFile, "w")
    fout.write(newParFile)
    fout.close()

    # Run the program with the new parameter file
    os.system("echo "+tmpParameterFile+" | ./qxpak.linux64")


if __name__ == "__main__":
    main(sys.argv[1:])
