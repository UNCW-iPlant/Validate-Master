#' Demonstrate2: Visualizing output from Winnow for the iPlant Collaborative Validate Workflow
#'
#' This function allows you to enter a directory including multiple Winnow output files and creating
#' visualizations fromt the output.
#' @param dir A character string: input the directory containing the text files you would like to use.
#' @param settingsfile A character string: input the winnow .param file containing settings used. Default is NULL and is not required.
#' @param make.pos.plot Option to make a true positive by false positive plot. Default set to TRUE
#' @param pos.plot.title A Character String: title of the True/False Positives plot.
#' Default set to "True Positives by False Positives"
#' @param make.error.plot Option to make an AUC by MAE plot. Default set to TRUE
#' @param error.plot.title A Character String: title of the AUC/MAE plot. Default set to
#' "Plot of AUC by MAE"
#' @param extra.plots Option to make two histogram files. One file is for false positives and the
#' other for true positives. Default set to TRUE
#' @param AUC.axis.min Sets the minimum value for the y-axis on the AUC by MAE plot. Default
#' set to '0'.
#' @param AUC.axis.max Sets the maximum value for the y-axis on the AUC by MAE plot. Default
#' set to '1.0'.
#' @param MAE.axis.min Sets the minimum value for the x-axis on the AUC by MAE plot. Default
#' set to '0'.
#' @param MAE.axis.max Sets the maximum value for the x-axis on the AUC by MAE plot. Default
#' set to '2.0'.
#' @keywords graph demonstrate GWAS validate
#' @export
#' @examples
#' demonstrate2 (dir="path")
#' demonstrate2 (dir="path", settingsfile="results.param")

Demonstrate2<-function(dir, outputdir=NULL, settingsfile=NULL, make.pos.plot=TRUE, pos.plot.title="True Positives vs. False Positives.pdf",
                       make.error.plot=TRUE, error.plot.title="Plot of AUC by MAE", extra.plots=TRUE,
                       AUC.axis.min=0, AUC.axis.max=1.0, MAE.axis.min=0, MAE.axis.max=2.0){

  require(ggplot2)
  require(plyr)
  require(grid)
  setOutput <- function(title){
    if (!is.null(outputdir)){
      return(paste(outputdir, title, sep="/"))
    }
    return(title)
  }
readFiles <- function(dir) {
    setwd(dir)
    files <- Sys.glob("*.txt")
    listOfFiles <- lapply(files, function(x) read.table(x, header=TRUE))
    return(listOfFiles)
  }
  myfiles<-readFiles(dir)
  filenames <- unlist(tools::file_path_sans_ext(Sys.glob("*.txt")))
  print(filenames)


  writeSettings <- function(){
    if (!is.null(settingsfile)){
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
  makeSettingsNote <- function(){
    if (!is.null(settingsfile)){
      settings <- readLines(settingsfile)
      pushViewport(viewport())
      grid.text(label=settings[1], x=unit(1, "npc")-unit(5, "mm"), y=unit(170, "mm"), just=c("right", "bottom"),
      gp = gpar(cex = 0.7))
      grid.text(label=settings[2], x=unit(1, "npc")-unit(5, "mm"), y=unit(165, "mm"), just=c("right", "bottom"),
      gp = gpar(cex = 0.7))
      grid.text(label=settings[3], x=unit(1, "npc")-unit(5, "mm"), y=unit(160, "mm"), just=c("right", "bottom"),
      gp = gpar(cex = 0.7))
      if(!is.na(settings[4])){
        grid.text(label=settings[4], x=unit(1, "npc")-unit(5, "mm"), y=unit(155, "mm"), just=c("right", "bottom"),
        gp = gpar(cex = 0.7))
      }
      popViewport()
    }
  }
  #Create some extra plots for univariate visualization
  if (extra.plots){
    pdf(file="TP Histograms.pdf")
    for (i in 1:length(myfiles)){
      hist(myfiles[[i]]$tp, main=paste(filenames[[i]]," True Positives",sep=":"), xlab="True Positives")
    }
    dev.off()
    pdf(file="FP Histograms.pdf")
    for (i in 1:length(myfiles)){
      hist(myfiles[[i]]$fp, main=paste(filenames[[i]]," False Positives",sep=":"), xlab="False Positives")
    }
    dev.off()

    #Make a quick summary table comparing PPV/Precision, sensivity, and specificity
    #and output said table to a CSV file
    sens<-unlist(lapply(myfiles, function(x) mean(x$sens)))
    spec<-unlist(lapply(myfiles, function(x) mean(x$spec)))
    prec<-unlist(lapply(myfiles, function(x) mean(as.numeric(setdiff(x$precision, "undefined")))))
    fitdat<-data.frame(sens,spec,prec, row.names=filenames, stringsAsFactors=FALSE)
    colnames(fitdat)<-c("Average Sensitivity","Average Specificity","Average Precision")
    write.csv(fitdat, "ComparisonTable.csv")
  }

  #Create the plots for true and false positives
  if (make.pos.plot){
    print("Creating positive count plots...")
    for (i in 1:length(myfiles)){
      attach(myfiles[[i]])
      myfiles[[i]]$file <- sQuote(i)
      detach(myfiles[[i]])
    }

    #Determines maximum value of all true positives
    tpmax<-function(list){
      tps<-list()
      for (i in 1:length(list)){
        tps[[i]]<-list[[i]]$tp
      }
      y<-unlist(lapply(tps, max))
      return(max(y))
    }
    ta<-tpmax(myfiles)
    #Determines minimum value of all true positives
    tpmin<-function(list){
      tps<-list()
      for (i in 1:length(list)){
        tps[[i]]<-list[[i]]$tp
      }
      y<-unlist(lapply(tps, min))
      return(min(y))
    }
    tb<-tpmin(myfiles)
    #Determines median value of all true positives
    tpmed<-function(list){
      tps<-list()
      for (i in 1:length(list)){
        tps[[i]]<-list[[i]]$tp
      }
      y<-unlist(lapply(tps, median))
      return(median(y))
    }
    tc<-tpmed(myfiles)
    #Determines maximum value of all false positives
    fpmax<-function(list){
      fps<-list()
      for (i in 1:length(list)){
        fps[[i]]<-list[[i]]$fp
      }
      y<-unlist(lapply(fps, max))
      return(max(y))
    }
    fa<-fpmax(myfiles)
    #Determines minimum value of all false positives
    fpmin<-function(list){
      fps<-list()
      for (i in 1:length(list)){
        fps[[i]]<-list[[i]]$fp
      }
      y<-unlist(lapply(fps, min))
      return(min(y))
    }
    fb<-fpmin(myfiles)
    #Determines median value of all false positives
    fpmed<-function(list){
      fps<-list()
      for (i in 1:length(list)){
        fps[[i]]<-list[[i]]$fp
      }
      y<-unlist(lapply(fps, median))
      return(median(y))
    }
    fc<-fpmed(myfiles)

    all.data<-do.call("rbind", myfiles)

    TPFP <- ddply(all.data, .(tp, fp, file), summarize, count=length(file))

    #Creates pdf output
    pdf(file=setOutput(pos.plot.title))

    #Creates plot of each file with rectangles from minimums to medians and medians
    #to maximums of all true and false positives. Points in the green area represent
    #the "best" outputs, those in the gray area represent the "worst", and those in
    #blue areas are "okay".
    p <- ggplot(TPFP, aes(x=fp, y=tp), environment=environment())
    p2 <- p +
      geom_rect(data=all.data[1,], aes(xmin=fc, xmax=fa, ymin=tc, ymax=ta),
                alpha=0.2, fill="blue", linetype=0) +
      geom_rect(data=all.data[1,], aes(xmin=fb, xmax=fc, ymin=tc, ymax=ta),
                alpha=0.2,fill="green", linetype=0) +
      geom_rect(data=all.data[1,], aes(xmin=fb, xmax=fc, ymin=tb, ymax=tc),
                alpha=0.2, fill="blue", linetype=0) +
      geom_rect(data=all.data[1,], aes(xmin=fc, xmax=fa, ymin=tb, ymax=tc),
                alpha=0.2, fill="gray", linetype=0) +
      theme(panel.background=element_rect(fill='white', colour='black')) +
      theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank()) +
      geom_point(aes(colour=file, size=count)) +
      scale_size_continuous(range=c(2,8)) +
      xlab("False Positives") +
      ylab("True Positives") +
      ggtitle("False Positives by True Positves") +
      xlim(0, fa) + ylim(0, ta) +
      scale_colour_discrete(labels=filenames)
    print(p2)
    makeSettingsNote()


    dev.off()

  }

  #Create the plots for AUC and MAE
  if (make.error.plot){
    print("Creating error plots...")
    for (i in 1:length(myfiles)){
      attach(myfiles[[i]])
      myfiles[[i]]$file <- sQuote(i)
      detach(myfiles[[i]])
    }

    all.data<-do.call("rbind", myfiles)

    MAE_AUC <- ddply(all.data, .(mae, auc, file), summarize, count=length(file))

    #Creates pdf output
    pdfname<-paste(error.plot.title,"pdf",sep=".")
    pdf(file=setOutput(pdfname))

    p <- ggplot(MAE_AUC, aes(x=mae, y=auc, color=file), environment()) + geom_point(
      aes(size=count))

    p2 <- p + geom_smooth(method=lm, fullrange=TRUE) +
      theme(panel.background=element_rect(fill='white', colour='black')) +
      theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank()) +
      scale_colour_discrete(label=filenames)
    print(p2)
    makeSettingsNote()

    dev.off()
  }
  print("Done!")
}