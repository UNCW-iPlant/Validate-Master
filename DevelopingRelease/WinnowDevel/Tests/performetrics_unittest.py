import unittest
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('DevelopingRelease')])
from DevelopingRelease.WinnowDevel import performetrics


class PerformetricsTest(unittest.TestCase):
    def test_rmse(self):
        beta_col = [1, 2, 3, 4, 5, 6]
        beta_tf = [1, 0, 1, 1, 0, 0]
        self.assertEqual(performetrics.rmse(beta_col, beta_tf), 13.0)

    def test_mae(self):
        beta_col = [1, 2, 3, 4, 5, 6]
        beta_tf = [1, 0, 1, 1, 0, 0]
        self.assertEqual(performetrics.mae(beta_col, beta_tf), 3.0)

    def test_mattcorr(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.mattcorr(snp_tf, threshold, score), 0.1690308509457033)

    def test_auc(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        self.assertEqual(performetrics.auc(snp_tf, score), 0.56944444444444442)

    def test_tp(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.tp(snp_tf, threshold, score), 4)

    def test_fp(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.fp(snp_tf, threshold, score), 3)

    def test_tn(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.tn(snp_tf, threshold, score), 3)

    def test_fn(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.fn(snp_tf, threshold, score), 2)

    def test_tpr(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.tpr(snp_tf, threshold, score), 0.6666666666666666)

    def test_fpr(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.fpr(snp_tf, threshold, score), 0.5)

    def test_error(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.error(snp_tf, threshold, score), 0.4166666666666667)
    
    def test_accuracy(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.accuracy(snp_tf, threshold, score), 0.5833333333333333)

    def test_sens(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.sens(snp_tf, threshold, score), 0.6666666666666666)

    def test_spec(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.spec(snp_tf, threshold, score), 0.5)

    def test_precision(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.precision(snp_tf, threshold, score), 0.5714285714285714)

    def test_youden(self):
        snp_tf = [True, False, True, True, True, False, False, True, False, False, True, False]
        score = [0.003, 0.65, 0.004, 0.006, 0.078, 0.003, 0.0001, 0.513, 0.421, 0.0081, 0.043, 0.98]
        threshold = 0.05
        self.assertEqual(performetrics.youden(snp_tf, threshold, score), 0.16666666666666652)


def get_test_suite():
    """
    Returns a test suite with all tests

    """
    return unittest.TestLoader().loadTestsFromTestCase(PerformetricsTest)

if __name__ == "__main__":
    unittest.main()
