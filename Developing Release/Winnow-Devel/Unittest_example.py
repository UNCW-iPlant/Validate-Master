import unittest
#Sets up the unit test; basically, it asserts that these variables have a certain value by the time the program
#finishes running
class ValuesTest(unittest.TestCase):
    def test1(self):
        #Basic example: severity ratio is None by default
        self.assertIsNone(severity, "Severity is not none!")
    def test2(self):
        #Requires that verbose flag is on to be OK
        self.assertTrue(verbose, "Verbose mode is off!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action = "store_true", default = False, help = "Triggers verbose mode")
    parser.add_argument('-f', default='MyResults.txt', type = str, help = "Desired name for the Winnow output file")
    parser.add_argument('-a', default = 'GWAS', type = str, help = "The type of analysis (if blank, Winnow assumes GWAS)")
    parser.add_argument('-F', help = "Input folder of box results") 
    parser.add_argument('-C', help = "The name of the known truth file")
    parser.add_argument('-S', help = "The name of the SNP column in the output")
    parser.add_argument('-P', help = "The name of the score column in the output")
    parser.add_argument('-s', choices = ['comma', 'whitespace'], help = "The delimiter for terms in the analysis file (whitespace or comma)")
    parser.add_argument('-b', help = "The name of the effect size column in the analysis output")
    parser.add_argument('-t', default = 0.05, help = "The threshold for use in certain performance metrics")
    parser.add_argument('-r', default = None, help = "The severity ratio used in analysis")
    results = parser.parse_args()
    verbose = results.v 
    filename = results.f
    analysis = results.a 
    folder = results.F 
    Class = results.C
    snp = results.S
    score = results.P
    seper = results.s
    beta = results.b 
    threshold = results.t
    severity = results.r 
    unittest.main()