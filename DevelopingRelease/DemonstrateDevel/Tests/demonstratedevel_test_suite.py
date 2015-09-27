import ListRanker_unittest as lr
import MPlot_unittest as mplot
import demonstrate_unittest as dem
import demonstrate2_unittest as dem2
import unittest


def main():
    test_suite = unittest.TestSuite()
    test_suite.addTests(lr.get_test_suite())
    test_suite.addTests(mplot.get_test_suite())
    test_suite.addTests(dem.get_test_suite())
    test_suite.addTests((dem2.get_test_suite()))
    unittest.TextTestRunner(verbosity=2).run(test_suite)


if __name__ == "__main__":
    main()
