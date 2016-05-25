from unittest import TestCase, TestLoader
from DevelopingRelease.UtilDevel.Merger.MergeTypes.BayesRMerge import BayesRMerge


class TestBayesRMerge(TestCase):
    def test_read_generator(self):
        brm = BayesRMerge('TestFiles/bayesOut', 'TestFiles/bayesR.bim', 'TestFiles/bayesR.param')
        expected_line = 'SNP	PIP1	PIP2	PIP3	PIP4	beta\n'
        self.assertEquals(brm.read_generator().next(), expected_line)


def get_test_suite():
    return TestLoader().loadTestsFromTestCase(TestBayesRMerge)
