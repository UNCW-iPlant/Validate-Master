import unittest
import test_alphaSimMerge
import test_bayesRMerge
import test_mergeType
import os


def main():
    test_suite = unittest.TestSuite()

    test_suite.addTests(test_alphaSimMerge.get_test_suite())
    test_suite.addTests(test_bayesRMerge.get_test_suite())
    test_suite.addTests(test_mergeType.get_test_suite())

    unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == '__main__':
    main()