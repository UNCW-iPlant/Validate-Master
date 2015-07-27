import ListRanker_unittest as lr
import unittest


def main():
    test_suite = unittest.TestSuite()

    test_suite.addTests(lr.get_test_suite())

    unittest.TextTestRunner(verbosity=2).run(test_suite)


if __name__ == "__main__":
    main()
