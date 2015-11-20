import unittest
import os
import rpy2.robjects as robjects


class DemonstrateTest(unittest.TestCase):
    testdir = os.getcwd() + '/DemTestFiles'
    demoargs = {"mode": "demonstrate", "dir": testdir};
    args = (testdir, None, None, False, "Mean AUC By Population Structure and Heritability", False,
            "Mean MAE By Population Structure and Heritability", ["_03_", "_04_", "_06_"], [0.3, 0.4, 0.6],
            ["PheHasStruct", "PheNPStruct"], [True, False])

    def test_directory(self):
        self.assertTrue(os.path.isdir(self.testdir))

    def test_function(self):
        self.load_r()
        r_dem = robjects.globalenv['Demonstrate']
        outputs = ['Mean AUC By Population Structure and Heritability.pdf',
                   'Mean MAE By Population Structure and Heritability.pdf']
        for each in outputs:
            if os.path.isfile(self.testdir + '/' + each):
                os.remove(self.testdir + '/' + each)
        r_dem(self.testdir)
        for each in outputs:
            self.assertTrue(os.path.isfile(self.testdir + '/' + each))
            self.assertTrue(os.path.getsize(self.testdir + '/' + each) > 0)
            if os.path.isfile(self.testdir + '/' + each):
                os.remove(self.testdir + '/' + each)

    def load_r(self):
        with open(os.getcwd()[:os.getcwd().index('Tests')]+'DemoMPlot/R/Demonstrate.R') as f:
            dem = f.read()
        robjects.r(dem)


def get_test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(DemonstrateTest)

if __name__ == "__main__":
    unittest.main()