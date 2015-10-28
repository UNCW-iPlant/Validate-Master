import os
import unittest
import rpy2.robjects as robjects


class MPlotTest(unittest.TestCase):
    testdir = os.getcwd()+"/MPlotTestFiles"

    def test_directory(self):
        self.assertTrue(os.path.isdir(self.testdir))

    def test_function(self):
        if os.path.isfile(self.testdir + '/Manhattan Plot.pdf'):
            os.remove(self.testdir + '/Manhattan Plot.pdf')
        self.load_r()
        r_mplot = robjects.globalenv['MPlot']
        r_mplot(self.testdir)
        self.assertTrue(os.path.isfile(self.testdir + '/Manhattan Plot.pdf'))
        self.assertTrue(os.path.getsize(self.testdir + '/Manhattan Plot.pdf') > 0)
        if os.path.isfile(self.testdir + '/Manhattan Plot.pdf'):
            os.remove(self.testdir + '/Manhattan Plot.pdf')

    def load_r(self):
        with open(os.getcwd()[:os.getcwd().index('Tests')]+'DemoMPlot/R/MPlot.R') as f:
            mp = f.read()
        robjects.r(mp)


def get_test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(MPlotTest)

if __name__ == "__main__":
    unittest.main()
