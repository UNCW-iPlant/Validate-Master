"""
Class for consolidating unittests for the winnow folder

"""
import unittest
import winnow_unittest
import performetrics_unittest
import adjustments_unittest
import gwas_unittest


def main():
    """
    Creates a test suite, currently only adds winnow and performetrics unittests to the suite, and runs this test suite

    """
    test_suite = unittest.TestSuite()

    # Test suite's to add
    test_suite.addTests(winnow_unittest.get_test_suite())
    test_suite.addTests(performetrics_unittest.get_test_suite())
    test_suite.addTests(adjustments_unittest.get_test_suite())
    test_suite.addTests(gwas_unittest.get_test_suite())

    # Runs tests
    unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == "__main__":
    main()
