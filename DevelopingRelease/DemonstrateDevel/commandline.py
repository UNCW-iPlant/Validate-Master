"""
Functions for identifying and using the command-line to execute Demonstrate through Python
"""

import argparse


def initialize_graphics():
    """ Prints introduction graphics for every time the software runs """

    print "###################################################################"
    print "###                                                            ####"
    print "###                Demonstrate Through Python!                 ####"
    print "###                                                            ####"
    print "###################################################################"


def usage():
    """ Prints all possible command-line arguments to the screen """
    print "\n\n\n"
    print "Command-line usage help menu"
    print "--help or -h to see the help menu"
    print "--verbose or -v for verbose mode"
    print "--dir or -d to specify the directory containing the input files (required)"
    print "--output or -o to specify the output directory, uses the input directory by default"
    print "--settingsfile or -s to specify the settings file from Winnow"
    print "--mode or -o to specify either Demonstrate or Demonstrate2 (required)"
    print "Demonstrate Arguments"
    print "\t--auc or -a to include the AUC plot"
    print "\t--auctitle or -t to specify the AUC plot title"
    print "\t--mae or -m to include the MAE plot"
    print "\t--maetitle or -y to specify the MAE plot title"
    print "\t--heritstring or -r to specify the strings representing heritability found in the data files (required)"
    print "\t--heritvalue or -l to specify the heritability values (required)"
    print "\t--structstring or -u to specify the strings representing the structure found in the data files (required)"
    print "\t--structvalue or -p to specify the value of structure (TRUE or FALSE, required)"
    print "Demonstrate2 Arguments"
    print "\t--pos or -q to include the TP by FP plot"
    print "\t--postitle or -i to specify the TP by FP title"
    print "\t--error or -e to include the Error plot"
    print "\t--errortitle or -w to specify the Error plot title"
    print "\t--extraplots or -x to not include extra plots"
    print "\t--aucmin or -z to specify the minimum for the AUC axis"
    print "\t--aucmax or -b to specify the maximum for the AUC axis"
    print "\t--maemin or -n to specify the minimum for the MAE axis"
    print "\t--maemax or -c to specify the maximum for the MAE axis\n\n"


def check_args():
    """
    Handles arguments for demonstrate and demonstrate2 modes.

    Creates the argument parser and adds a subparser for demonstrate and demonstrate 2 with the needed arguments,
    parses the given arguments as a dictionary, prints if selected, and returns the dictionary of arguments
    :return: dictionary of arguments
    """
    parser = argparse.ArgumentParser(description="Demonstrate command-line arguments")
    parser.add_argument("-v", "--verbose", help="Trigger verbose mode", action="store_true", default=False)
    parser.add_argument("-d", "--dir", required=True, type=str, help="The input folder")
    parser.add_argument("-o", "--output", required=False, type=str, help="The output folder")
    parser.add_argument("-s", "--settings", type=str, help="The .param file from winnow", default=None)
    subparsers = parser.add_subparsers(help="Program mode (e.g. run demonstrate or demonstrate2)",
                                       dest="mode")
    add_demo_command_options(subparsers)
    add_demo2_command_options(subparsers)
    args = vars(parser.parse_args())
    if args["verbose"]:
        print_parameters(args)
    return args


def add_demo_command_options(subparsers):
    """
    Adds the arguments pertaining to the original Demonstrate.

    :param subparsers: the main argument parsers group of subparsers
    """
    demo_parser = subparsers.add_parser('demonstrate', help="Generate the original Demonstrate graphics")
    demo_parser.add_argument("-a", "--xauc", action="store_true", default=False,
                             help="To exclude the AUC plot")
    demo_parser.add_argument("-t", "--auctitle", type=str, default="Mean AUC By Population Structure and Heritability",
                             help="AUC plot title")
    demo_parser.add_argument("-m", "--xmae", action="store_true", default=False,
                             help="To exclude the MAE plot")
    demo_parser.add_argument("-y", "--maetitle", type=str, default="Mean MAE By Population Structure and Heritability",
                             help="MAE plot title")
    demo_parser.add_argument("-r", "--heritstring", type=str, default=["_03_", "_04_", "_06_"],
                             help="Heritability string from input data")
    demo_parser.add_argument("-l", "--heritvalue", type=float, default=[0.3, 0.4, 0.6],
                             help="Heritability value from input data")
    demo_parser.add_argument("-u", "--structstring", type=str, default=["PheHasStruct", "PheNPStruct"],
                             help="Structure string from input data")
    demo_parser.add_argument("-p", "--structvalue", type=bool, default=[True, False],
                             help="Structure value from input data")


def add_demo2_command_options(subparsers):
    """
    Adds the arguments pertaining to the Demonstrate2 function.

    :param subparsers: the main argument parsers group of subparsers
    """
    demo2_parser = subparsers.add_parser('demonstrate2', help="Generate the Demonstrate2 graphics")
    demo2_parser.add_argument("-q", "--xpos", action="store_true", default=False,
                        help="To exclude the TP by FP plot")
    demo2_parser.add_argument("-i", "--postitle", type=str, default="True Positives by False Positives",
                        help="TP by FP plot title")
    demo2_parser.add_argument("-e", "--xerror", action="store_true", default=False,
                        help="To exclude the error plot")
    demo2_parser.add_argument("-w", "--errortitle", type=str, default="Plot of AUC by MAE",
                        help="The error plot title")
    demo2_parser.add_argument("-x", "--extraplots", action="store_false", default=True,
                        help="To include extra plots")
    demo2_parser.add_argument("-z", "--aucmin", type=float, default=0,
                        help="Minimum auc axis value")
    demo2_parser.add_argument("-b", "--aucmax", type=float, default=1.0,
                        help="Maximum auc axis value")
    demo2_parser.add_argument("-n", "--maemin", type=float, default=0,
                        help="Minimum mae axis value")
    demo2_parser.add_argument("-c", "--maemax", type=float, default=2.0,
                        help="Maximum mae axis value")


def print_parameters(args_dict):
    """
    Prints out the arguments that were passed at run time. This function should only be called after checking for the
    verbose option

    :param args_dict: the arguments in a dictionary
    """
    print "\nVerbose Mode"
    print "Input directory is specified as", args_dict["dir"]
    if args_dict["output"] is not None:
        print "The output directory is specified as", args_dict["output"]
    else:
        print "The output directory is specified as", args_dict["dir"]
    if args_dict["settings"] is not None:
        print "Settings file is specified as", args_dict["settings"]
    print "Demonstrate mode is set to", args_dict["mode"]
    if args_dict["mode"] == "demonstrate":
        if not args_dict["xauc"]:
            print "Including AUC plot"
            print "AUC plot title specified as", args_dict["auctitle"]
        else:
            print "AUC plot not included"
        if not args_dict["xmae"]:
            print "Including MAE plot"
            print "MAE plot title specified as", args_dict["maetitle"]
        else:
            print "MAE plot included"
        print "Heritability strings specified as", args_dict["heritstring"]
        print "Heritability values specified as", args_dict["heritvalue"]
        print "Structure strings specified as", args_dict["structstring"]
        print "Structure values specified as", args_dict["structvalue"]
    elif args_dict["mode"] == "demonstrate2":
        if not args_dict["xpos"]:
            print "Including TP by FP plot"
            print "TP by FP plot title specified as", args_dict["postitle"]
        else:
            print "TP by FP plot not included"
        if not args_dict["xerror"]:
            print "Including Error plot"
            print "Error plot title specified as", args_dict["errortitle"]
        else:
            print "Error plot not included"
        if args_dict["extraplots"]:
            print "Including extra plots"
        print "AUC axis minimum specified as", args_dict["aucmin"]
        print "AUC axis maximum specified as", args_dict["aucmax"]
        print "MAE axis minimum specified as", args_dict["maemin"]
        print "MAE axis maximum specified as", args_dict["maemax"]
