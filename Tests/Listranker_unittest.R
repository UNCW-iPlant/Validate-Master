#Unit tests for the List Ranker algorithm
library("testthat")
source("ListRanker.R")

#Obviously, will need to change this if you're running on a different machine
maindir<-"C:/Users/Owner/Dropbox/iPlant Collaborative Files/Listranktest"
secondarg<-"TestTP.csv"
thirdarg<-"TestFP.csv"

test_that("Test the List ranker inputs", {
  
  #First, test that the directory in use exists...
  expect_true(dir.exists(maindir))
  
  #Next, check the filenames are valid
  expect_is(secondarg, "character")
  expect_that(nchar(secondarg), is_more_than(0))
  expect_is(thirdarg, "character")
  expect_that(nchar(thirdarg), is_more_than(0))
})

test_that("Test the actual function", {
  #No defaults, so this will throw an error
  expect_error(ListRanker())
  
  #Test that the inputs produce nothing i.e. success
  expect_that(ListRanker(maindir, secondarg, thirdarg), prints_text(""))
})

test_that("Test the outputs", {
  
  #Make sure the files are valid and non-empty
  expect_true(file.exists(paste(maindir, "TestTP.csv", sep="/")))
  expect_that(file.info("TestTP.csv")$size, is_more_than(0))
  expect_true(file.exists(paste(maindir, "TestFP.csv", sep="/")))
  expect_that(file.info("TestFP.csv")$size, is_more_than(0))
})

