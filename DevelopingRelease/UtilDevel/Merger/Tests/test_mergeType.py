from unittest import TestCase, TestLoader
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('DevelopingRelease')])
from DevelopingRelease.UtilDevel.Merger.MergeType import MergeType


class TestMergeType(TestCase):
    def test_read_generator(self):
        mt = MergeType('test')
        with self.assertRaises(NotImplementedError) as context:
            mt.read_generator()
        self.assertTrue('The read method must be implemented in the subclass' in context.exception)


def get_test_suite():
    return TestLoader().loadTestsFromTestCase(TestMergeType)
