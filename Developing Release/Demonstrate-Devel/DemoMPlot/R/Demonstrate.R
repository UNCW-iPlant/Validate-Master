#' Demonstrate: Visualizing output from Winnow for the iPlant Collaborative Validate Workflow
#'
#' This function allows you to enter a directory including multiple Winnow output files and creating
#' visualizations fromt the output.
#' @param dir A character string: input the directory containing the text files you would like to use.
#' @param make.AUC.plot Option to make a AUC by Population Structure and Heritability. Default set to TRUE
#' @param AUC.plot.title A Character String: title of the AUC plot.
#' Default set to "Mean AUC By Population Structure and Heritability"
#' @param make.MAE.plot Option to make MAE by Population Structure and Heritability plot. Default set to TRUE
#' @param MAE.plot.title A Character String: title of the MAE. Default set to
#' "Mean MAE By Population Structure and Heritability"
#' @param herit.strings Details the strings to look for in filenames for determining the heritability 
#' coefficients. Corresponds to the list in herit.values
#' @param herit.values Sets the values for heritability. Default sets to 0.3, 0.4, 0.6.
#' @param struct.strings Details the strings to look for in filenames for determining population structure. 
#' Corresponds to the list in _struct.values_. Example: list("PheHasStruct", "PheNPStruct")
#' @param struct.values The list of values for population structure. Generally Boolean (i.e. TRUE or FALSE). 
#' Value order should correspond to the _struct.strings_ variable. Example (to go with previous): list(TRUE, FALSE)
#' @keywords graph demonstrate GWAS validate knowntruth
#' @export
#' @examples
#' demonstrate (dir="path")

Demonstrate <- function(dir, make.AUC.plot=TRUE, AUC.plot.title="Mean AUC By Population Structure and Heritability",
                        make.MAE.plot=TRUE, MAE.plot.title="Mean MAE By Population Structure and Heritability",herit.strings=list("_03_","_04_","_06_")
                        ,herit.values=list(0.3,0.4,0.6),struct.strings=list("PheHasStruct","PheNPStruct"),struct.values=list(TRUE,FALSE)) {

  makeFiles <- function(dir) {

    readFiles <- function(dir) {
      setwd(dir)
      files <- (Sys.glob("*.txt"))
      listOfFiles <- lapply(files, function(x) read.table(x, header=TRUE))
      return(listOfFiles)
    }

    createHeritLabel <- function(data) {
      newData <- data
      newData$Herit <- NA
      first <- TRUE
      for (i in 1:length(herit.strings)) {
        newData$Herit <- ifelse(sapply(data$Name,function(x) grepl(herit.strings[[i]],x)),
                                herit.values[[i]],newData$Herit)
      }
      return(newData)
    }

    createStructureLabel <- function(data) {
      newData <- data
      newData$Structure <- NA
      for (i in 1:length(struct.strings)) {
        newData$Structure <- ifelse(sapply(data$Name,function(x) grepl(struct.strings[[i]],x)),
                                    struct.values[[i]],newData$Structure)
      }
      return(newData)
    }

    createLabels <- function(data) {
      newData <- createHeritLabel(data)
      newNewData <- createStructureLabel(newData)
      return(newNewData)
    }

    myFiles <- readFiles(dir)
    myFiles <- lapply(myFiles, createLabels)

    return(myFiles)

  }

  myFiles <- makeFiles(dir)
  totalDataSet <- myFiles[[1]]
  for (i in 2:length(myFiles)) {
    totalDataSet <- rbind(totalDataSet, myFiles[[i]])
  }

  require(sciplot)

  if (make.AUC.plot) {
    pdf(file=AUC.plot.title)
    lineplot.CI(totalDataSet$Herit,totalDataSet$AUC,totalDataSet$Structure,main=AUC.plot.title,
                xlab="Heritability",ylab="Mean AUC",trace.label="Pop. Structure")
    dev.off()
  }

  if (make.MAE.plot) {
    pdf(file=MAE.plot.title)
    lineplot.CI(totalDataSet$Herit,totalDataSet$MAE,totalDataSet$Structure,main=MAE.plot.title,
                xlab="Heritability",ylab="Mean MAE",trace.label="Pop. Structure")
    dev.off()
  }

  return(totalDataSet)

}
