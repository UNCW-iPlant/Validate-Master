import unittest
import os
import rpy2.robjects as robjects


class Dem2Test(unittest.TestCase):
    testdir = os.getcwd()+"/Dem2TestFiles"

    def test_directory(self):
        self.assertTrue(os.path.isdir(self.testdir))

    def test_function(self):
        self.load_r()
        r_dem2 = robjects.globalenv['Demonstrate2']
        return_value = str(r_dem2(self.testdir))
        self.assertEquals(return_value, '[1] "Done!"\n')
        
    def test_outputs(self):
        self.load_r()
        r_dem2 = robjects.globalenv['Demonstrate2']
        outputnames = ['ComparisonTable.csv', 'TP Histograms.pdf', 'FP Histograms.pdf',
                       'True Positives vs. False Positives.pdf', 'Plot of AUC by MAE.pdf']
        for name in outputnames:
            if os.path.isfile(self.testdir + '/' + name):
                os.remove(self.testdir + '/' + name)
        r_dem2(self.testdir)
        for name in outputnames:
            self.assertTrue(os.path.isfile(self.testdir + '/' + name))
            self.assertTrue(os.path.getsize(self.testdir + '/' + name) > 0)
            os.remove(self.testdir + '/' + name)
        
    def load_r(self):
        with open(os.getcwd()[:os.getcwd().index('Tests')]+'DemoMPlot/R/Demonstrate2.R') as f:
            dem2 = f.read()
        robjects.r(dem2)


def get_test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(Dem2Test)

if __name__ == "__main__":
    unittest.main()