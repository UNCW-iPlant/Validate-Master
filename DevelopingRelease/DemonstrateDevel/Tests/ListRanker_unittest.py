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
        self.assertEquals(return_value, '[1] "Done"\n')

    def test_outputs(self):
        self.load_r()
        r_listranker = robjects.globalenv['ListRanker']
        if os.path.isfile(self.maindir + "/" + self.secondarg):
            os.remove(self.maindir + "/" + self.secondarg)
        if os.path.isfile(self.maindir+ "/" + self.thirdarg):
            os.remove(self.maindir + "/" + self.thirdarg)
        r_listranker(self.maindir, self.secondarg, self.thirdarg)
        self.assertTrue(os.path.isfile(self.maindir + "/" + self.secondarg))
        self.assertTrue(os.path.isfile(self.maindir + "/" + self.thirdarg))
        self.assertTrue(os.path.getsize(self.maindir + "/" + self.secondarg) > 0)
        self.assertTrue(os.path.getsize(self.maindir + "/" + self.thirdarg) > 0)
        if os.path.isfile(self.maindir + "/" + self.secondarg):
            os.remove(self.maindir + "/" + self.secondarg)
        if os.path.isfile(self.maindir+ "/" + self.thirdarg):
            os.remove(self.maindir + "/" + self.thirdarg)

    def load_r(self):
        robjects.r("""
            readFiles <- function(d) {
                setwd(d)
                files <- Sys.glob("*.txt")
                listOfFiles <- lapply(files, function(x) read.table(x, header=TRUE))
                return(listOfFiles)
            }
            listrank<-function(tps) {
                l <- lapply(tps, function(x) rank(x, ties.method="first"))
                return(l)
            }
            ListRanker<-function(dir, filename.tp, filename.fp) {
                myfiles <- readFiles(dir)
                tp<-fp<-list()
                for (i in 1:length(myfiles)){
                    tp[[i]]<-myfiles[[i]]$tp
                    fp[[i]]<-myfiles[[i]]$fp
                }
                rankedlist.tp<-as.matrix(listrank(tp))
                rankedlist.fp<-as.matrix(listrank(fp))
                MASS::write.matrix(rankedlist.tp, file=filename.tp, sep = ",")
                MASS::write.matrix(rankedlist.fp, file=filename.fp, sep = ",")
                return("Done")
            }
        """)


def get_test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(ListRankerTest)

if __name__ == "__main__":
    unittest.main()
