import unittest
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('DevelopingRelease')])
from DevelopingRelease.WinnowDevel import gwas
from DevelopingRelease.WinnowDevel import winnow as Winnow


class GWASTest(unittest.TestCase):
    folder = os.getcwd()[:os.getcwd().index("Validate-Master")] + "Validate-Master/ExampleData/Winnow/data/OutputPlink"
    ote = os.getcwd()[:os.getcwd().index("Validate-Master")] + "Validate-Master/ExampleData/Winnow/data/Plinkkt.ote"
    destination = os.getcwd()[:os.getcwd().index("Validate-Master")] + "Validate-Master/ExampleData/Winnow/results"
    args_without_covar = {'folder': folder, 'analysis': 'GWAS', 'truth': ote, 'snp': 'SNP', 'score': 'P',
                          'beta': 'BETA','filename': destination, 'threshold': 0.05, 'separ': 'whitespace',
                          'kt_type': 'OTE','kt_type_separ': 'whitespace', 'pvaladjust': None, 'savep': False,
                          'covar': None}

    def test_gwas_with_beta(self):
        self.args_without_covar['beta'] = 'BETA'
        self.win = Winnow.Winnow(self.args_without_covar)
        s, b = self.win.load_data("/PlinkStd1.qassoc")
        self.win.load_ote()
        desired = [0.058961209687231286, 0.18211782935394086, -0.038381861728111748, 0.43427678571428574, 0, 384,
                   2816, 35, 0.0, 0.12, 0.1295208655332303, 0.8704791344667697, 0.0, 0.88, 0.0, 1.0, -0.12]
        self.assertAlmostEquals(gwas.gwasWithBeta(b, self.win.beta_true_false, self.win.snp_true_false, s,
                                self.args_without_covar['threshold'])[1], desired)
        pass

    def test_gwas_with_beta_covariate(self):
        pass

    def test_gwas_without_beta(self):
        self.args_without_covar['beta'] = None
        self.win = Winnow.Winnow(self.args_without_covar)
        s = self.win.load_data("/PlinkStd1.qassoc")
        self.win.load_ote()
        desired = [-0.038381861728111748, 0.43427678571428574, 0, 384, 2816, 35, 0.0, 0.12, 0.1295208655332303,
                   0.8704791344667697, 0.0, 0.88, 0.0, 1.0, -0.12]
        self.assertAlmostEquals(gwas.gwasWithoutBeta(self.win.snp_true_false, s,
                                self.args_without_covar['threshold'])[1], desired)

    def test_gwas_with_beta_covariate(self):
        pass

def get_test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(GWASTest)
