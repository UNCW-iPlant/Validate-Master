from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage as stap
import os


def main():
    mplot_source = 'source("' + os.getcwd()[:os.getcwd().index("Tests")]+'DemoMPlot/R/MPlot.R")'
    test_dir = 'testdir<-"' + os.getcwd() + '/MPlotTestFiles"'
    unit_test_string = """
#Demonstrate package-MPlot function: unit tests
library(testthat)

#NOTE: If you are running this unit test on your own device,
#you may need to change the following directories before testing!""" + mplot_source + """

""" + test_dir + """
test_that("Directory checks", {
  #First, test the blank option, which will throw an error...
  expect_that(MPlot(), throws_error())

  #Next, make sure our test directory is still valid
  expect_that(dir.exists(testdir), is_true())

  #Then we test to make sure that the output is written to the graphical device
  expect_that(MPlot(testdir), prints_text("null device"))
})
#Run the function to make Manhattan Plot.pdf
MPlot(testdir)
test_that("Manhattan Plot output checks", {

  #Check to make sure the file exists in the first place...
  expect_that(file.exists(paste(testdir, "Manhattan Plot.pdf", sep="/")), is_true())

  #Finally, the file should be non-empty...
  expect_that(file.info("Manhattan Plot.pdf")$size, is_more_than(0))
})"""

    powerpack = stap(unit_test_string, "pack")
