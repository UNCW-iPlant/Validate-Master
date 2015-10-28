#' Demonstrate: Visualizing output from Winnow for the iPlant Collaborative Validate Workflow
#'
#' This function allows you to enter a directory including multiple Winnow output files and creating
#' visualizations fromt the output.
#' @param dir A character string: input the directory containing the text files you would like to use.
#' @param settingsfile A character string: input the winnow .param file containing settings used. Default is NULL and is not required.
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

Demonstrate <- function(dir, outputdir=NULL, settingsfile=NULL, make.AUC.plot=TRUE, AUC.plot.title="Mean AUC By Population Structure and Heritability.pdf",
                        make.MAE.plot=TRUE, MAE.plot.title="Mean MAE By Population Structure and Heritability.pdf",herit.strings=list("_03_","_04_","_06_")
                        ,herit.values=list(0.3,0.4,0.6),struct.strings=list("PheHasStruct","PheNPStruct"),struct.values=list(TRUE,FALSE)) {
  
  setOutput <- function(title){
    if (!is.null(outputdir)){
      return(paste(outputdir, title, sep="/"))
    }
    return(title)
  }
  writeSettings <- function(){
    if (!is.null(settingsfile)){
      setwd(dir)
      settings <- readLines(settingsfile)
      plot(0:10, type="n", xaxt="n", yaxt="n", bty="n", xlab="", ylab="")
      text(font=2, 5, 8, "Winnow Settings:")
      text(5, 7, settings[1])
      text(5, 6, settings[2])
      text(5, 5, settings[3])
      if (!is.na(settings[4])){
        text(5, 4, settings[4])
      }
    }
  }
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
      for (i in seq_along(herit.strings)) {
        newData$Herit <- ifelse(sapply(data$Name,function(x) grepl(herit.strings[[i]],x)),
                                herit.values[[i]],newData$Herit)
      }
      return(newData)
    }
    
    createStructureLabel <- function(data) {
      newData <- data
      newData$Structure <- NA
      for (i in seq_along(struct.strings)) {
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
  library(plyr)
  totalDataSet<-rbind.fill(myFiles)
  library(sciplot)
  
  if (make.AUC.plot) {
    pdf(file=setOutput(AUC.plot.title))
    lineplot.CI(totalDataSet$Herit,totalDataSet$AUC,totalDataSet$Structure,main=AUC.plot.title,
                xlab="Heritability",ylab="Mean AUC",trace.label="Pop. Structure")
    writeSettings()
    dev.off()
  }
  
  if (make.MAE.plot) {
    pdf(file=setOutput(MAE.plot.title))
    lineplot.CI(totalDataSet$Herit,totalDataSet$MAE,totalDataSet$Structure,main=MAE.plot.title,
                xlab="Heritability",ylab="Mean MAE",trace.label="Pop. Structure")
    writeSettings()
    dev.off()
  }
  
  return(totalDataSet)
  
}