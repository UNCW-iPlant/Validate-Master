import unittest
import os
import sys

sys.path.append(os.getcwd()[:os.getcwd().index('DevelopingRelease')])
from DevelopingRelease.WinnowDevel import winnow
from DevelopingRelease.WinnowDevel.fileimport import loadKT


class WinnowTest(unittest.TestCase):
    folder = os.getcwd()[:os.getcwd().index("Validate-Master")] + "Validate-Master/ExampleData/Winnow/data/OutputPlink"
    ote = os.getcwd()[:os.getcwd().index("Validate-Master")] + "Validate-Master/ExampleData/Winnow/data/Plinkkt.ote"
    destination = os.getcwd()[:os.getcwd().index("Validate-Master")] + "Validate-Master/ExampleData/Winnow/results"
    args = {'folder': folder, 'analysis': 'GWAS', 'truth': ote, 'snp': 'SNP', 'score': 'P', 'beta': 'BETA',
            'filename': destination, 'threshold': 0.05, 'separ': 'whitespace', 'kt_type': 'OTE',
            'kt_type_separ': 'whitespace', 'pvaladjust': None, 'savep': False, 'covar': None}

    def test_load_ote(self):
        self.win = winnow.Winnow(self.args)
        self.win.load_ote()
        snp = (False, False, False, True, False, False, False, False, False, True)
        beta = (0.0002, 0.0, 0.0061, 0.0, 0.0, 0.0026, 0.0454, 0.0, 0.0, 0.0)
        self.assertEqual((snp, beta), ((self.win.snp_true_false[2549], self.win.snp_true_false[1510],
                                        self.win.snp_true_false[1587], self.win.snp_true_false[12],
                                        self.win.snp_true_false[458], self.win.snp_true_false[502],
                                        self.win.snp_true_false[577], self.win.snp_true_false[3209],
                                        self.win.snp_true_false[1709], self.win.snp_true_false[15]),
                                       (self.win.beta_true_false[22], self.win.beta_true_false[684],
                                        self.win.beta_true_false[16], self.win.beta_true_false[2745],
                                        self.win.beta_true_false[832], self.win.beta_true_false[15],
                                        self.win.beta_true_false[29], self.win.beta_true_false[2028],
                                        self.win.beta_true_false[715], self.win.beta_true_false[276])))

    def test_load_data(self):
        self.win = winnow.Winnow(self.args)
        s, b = self.win.load_data("/PlinkStd1.qassoc")
        score = (0.6028, 0.06006, 0.4884, 0.6276, 0.8426, 0.4332, 0.717, 0.3584, 0.1795, 0.3647)
        beta = (0.3355, 0.3324, 0.2584, -0.2379, 0.0457, 0.113, -0.3001, -0.3267, 0.09707, 0.006248)
        self.assertEqual((score, beta), ((s[2061], s[1678], s[1553], s[2455], s[746], s[1892], s[813], s[1886],
                                          s[2005], s[1116]),
                                         (b[1766], b[2847], b[194], b[299], b[1813], b[2593], b[497], b[2572],
                                          b[2107], b[829])))

    def test_do_analysis(self):
        self.win = winnow.Winnow(self.args)
        self.win.load_kt()
        gen = self.win.do_analysis()
        a = gen.next()[1]
        self.assertEqual(format_float(a),
                         [0.05896121, 0.18211783, -0.03838186, 0.43427679, 0.0, 384.0, 2816.0, 35.0, 0.0, 0.12,
                          0.01081917, 0.12952087, 0.87047913, 0.0, 0.88, 0.0, 1.0, -0.12])
        gen.close()

    def test_do_gwas(self):
        self.win = winnow.Winnow(self.args)
        self.win.snp_true_false = (True, False, True, True, True, False, False, True, False, False, True, False)
        score_column = (0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98)
        self.win.beta_true_false = (1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1)
        beta_column = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        a = format_float(self.win.do_gwas(score_column, beta_column, None)[1])
        self.assertEqual(a,
                         [47.08333333, 5.91666667, 0.16903085, 0.56944444, 4.0, 3.0, 3.0, 2.0, 0.66666667, 0.5, 0.5,
                          0.41666667, 0.58333333, 0.66666667, 0.5, 0.57142857, 0.42857143, 0.16666667])



    def test_data_to_list(self):
        kt_file = loadKT(self.args['truth'], self.args['kt_type_separ'])
        self.assertEqual(winnow.data_to_list(kt_file, 1, 0),
                         ['gpm705a', 'tub1', 'gpm113b', 'gpm325a', 'dmt103b', 'gpm699d', 'gpm27', 'gpm319', 'bnl5.62a',
                          'fus6', 'mmp102', 'IDP1447', 'AY110314', 'IDP1464', 'gpm331', 'umc94a', 'lim179', 'AY107629',
                          'IDP755', 'mmp49', 'cdo1081a', 'gpm330', 'gpm83b', 'gpm767', 'asg31', 'npi415', 'AY108650',
                          'ufg31', 'ufg33', 'ufg32', 'ufg34', 'IDP4043', 'gpm495', 'bnlg1014', 'umc1363a'])


def format_float(float_list):
    """
    Truncates floats to 5 decimal places

    :param float_list:
    :return: a list of float truncuated to 5 decimal places
    """
    return_list = list()
    for each in float_list:
        return_list.append(float('%.8f' % each))
    return return_list


def get_test_suite():
    """
    Returns a test suite with all tests

    """
    return unittest.TestLoader().loadTestsFromTestCase(WinnowTest)
