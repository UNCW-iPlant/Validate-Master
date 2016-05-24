import os
import unittest
import rpy2.robjects as robjects


class ListRankerTest(unittest.TestCase):
    maindir = os.getcwd() + "/ListRankerTestFiles"
    secondarg = "TestTP.csv"
    thirdarg = "TestFP.csv"

    def test_inputs(self):
        self.assertTrue(os.path.isdir(self.maindir))
        self.assertTrue(len(self.secondarg) > 0)
        self.assertTrue(len(self.thirdarg) > 0)
        self.assertIsInstance(self.secondarg, str)
        self.assertIsInstance(self.thirdarg, str)

    def test_function(self):
        self.load_r()
        r_listranker = robjects.globalenv['ListRanker']
        return_value = str(r_listranker(self.maindir, self.secondarg, self.thirdarg))
        self.assertEquals(return_value, 'NULL')

    def test_outputs(self):
        self.load_r()
        r_listranker = robjects.globalenv['ListRanker']
        if os.path.isfile(self.maindir + "/" + self.secondarg):
            os.remove(self.maindir + "/" + self.secondarg)
        if os.path.isfile(self.maindir + "/" + self.thirdarg):
            os.remove(self.maindir + "/" + self.thirdarg)
        r_listranker(self.maindir, self.secondarg, self.thirdarg)
        self.assertTrue(os.path.isfile(self.maindir + "/" + self.secondarg))
        self.assertTrue(os.path.isfile(self.maindir + "/" + self.thirdarg))
        self.assertTrue(os.path.getsize(self.maindir + "/" + self.secondarg) > 0)
        self.assertTrue(os.path.getsize(self.maindir + "/" + self.thirdarg) > 0)

    @staticmethod
    def load_r():
        with open(os.getcwd()[:os.getcwd().index('DevelopingRelease/')] +
                  'DevelopingRelease/UtilDevel/ListRanker.R') as f:
            lr = f.read()
        robjects.r(lr)


def get_test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(ListRankerTest)

if __name__ == "__main__":
    unittest.main()
