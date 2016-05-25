from unittest import TestCase, TestLoader
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('Merger')]+'Merger')
sys.path.append(os.getcwd()[:os.getcwd().index('Merger')]+'Merger/MergeTypes')
from BayesRMerge import BayesRMerge


class TestBayesRMerge(TestCase):
    def test_read_generator(self):
        brm = BayesRMerge('Tests/TestFiles/bayesOut', 'Tests/TestFiles/bayesR.bim', 'Tests/TestFiles/bayesR.param')
        expected_line = 'SNP	PIP1	PIP2	PIP3	PIP4	beta\n'
        self.assertEquals(brm.read_generator().next(), expected_line)


def get_test_suite():
    return TestLoader().loadTestsFromTestCase(TestBayesRMerge)
