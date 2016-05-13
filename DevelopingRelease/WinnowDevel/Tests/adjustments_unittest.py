import unittest
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('DevelopingRelease')])
from DevelopingRelease.WinnowDevel import adjustments


class AdjustmentsTest(unittest.TestCase):
    """
    Tests method fdr_bh (adjusts p-values using Benjamini-Hochberg FDR method)
    Checks for equality within 7 decimal places of returned list and expected list of values
    """
    def test_fdr_bh(self):
        test1 = [0.012, 0.033, 0.212, 0.9, 0.98, 0.001, 0.999, 0.0003, 0.00001]
        results1 = [0.027, 0.05940000000000001, 0.318, 0.999, 0.999, 0.0030000000000000005, 0.999,
                    0.0013499999999999999, 9e-05]
        test2 = [0.010, 0.013, 0.014, 0.190, 0.350, 0.500, 0.630, 0.670, 0.750, 0.810]
        results2 = [0.04666666666666667, 0.04666666666666667, 0.04666666666666667, 0.475, 0.7, 0.8100000000000002,
                    0.8100000000000002, 0.8100000000000002, 0.8100000000000002, 0.8100000000000002]
        self.assertAlmostEquals(adjustments.fdr_bh(test1), results1)
        self.assertAlmostEquals(adjustments.fdr_bh(test2), results2)


def get_test_suite():
    """
    Returns a test suite with all tests
    """
    return unittest.TestLoader().loadTestsFromTestCase(AdjustmentsTest)

if __name__ == "__main__":
    unittest.main()