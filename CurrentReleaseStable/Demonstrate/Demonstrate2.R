Demonstrate2<-function(dir, make.pos.plot=TRUE, pos.plot.title="True Positives by False Positives",
                       make.error.plot=TRUE, error.plot.title="Plot of AUC by MAE", extra.plots=TRUE, 
                       AUC.axis.min=0, AUC.axis.max=1.0, MAE.axis.min=0, MAE.axis.max=2.0){
  
  readFiles <- function(dir) {
    setwd(dir)
    files <- Sys.glob("*.txt")
    listOfFiles <- lapply(files, function(x) read.table(x, header=TRUE))
    return(listOfFiles)
  }
  filenames <- unlist(tools::file_path_sans_ext(Sys.glob("*.txt")))
  myfiles<-readFiles(dir)
  print(filenames)
  
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
    prec<-unlist(lapply(myfiles, function(x) mean(x$precision)))
    fitdat<-data.frame(sens,spec,prec, row.names=filenames)
    colnames(fitdat)<-c("Average Sensitivity","Average Specificity","Average Precision")
    write.csv(fitdat, "ComparisonTable.csv")
  }
  
  #Create the plots for true and false positives
  if (make.pos.plot){
    print("Creating positive count plots...")
    tpsizeChecker<-function(list){
      tps<-list()
      for (i in 1:length(list)){
        tps[[i]]<-list[[i]]$tp
      }
      y<-unlist(lapply(tps, max))
      z<-unlist(lapply(tps, min))
      return(c(min(z), max(y)))
    }
    fpsizeChecker<-function(list){
      fps<-list()
      for (i in 1:length(list)){
        fps[[i]]<-list[[i]]$fp
      }
      y<-unlist(lapply(fps, max))
      z<-unlist(lapply(fps, min))
      return(c(min(z), max(y)))
    }
    
    pdfname<-paste(pos.plot.title,"pdf",sep=".")
    pdf(file=pdfname)
    plot(myfiles[[1]]$tp, myfiles[[1]]$fp, main=pos.plot.title, xlab="True Positives", ylab="False Positives",
         pch=21, bg="black", xlim=c(tpsizeChecker(myfiles)), ylim=c(fpsizeChecker(myfiles)))
    plotcol<-c("black")
    if (length(myfiles) >= 2){
      for (i in 2:length(myfiles)){
        points(myfiles[[i]]$tp, myfiles[[i]]$fp, main=pos.plot.title, xlab="True Positives", ylab="False Positives",
               pch=21, bg=rainbow(i+1)[i])
        plotcol[i]<-rainbow(i+1)[i]
      }
      
      legend("topright", legend=filenames, text.font=2, cex=0.63, pt.cex=0.95, pt.bg = plotcol, pch=21)
    }
    dev.off()
    
  }
  
  #Create the plots for AUC and MAE
  if (make.error.plot){
    print("Creating error plots...")
    pdfname<-paste(error.plot.title,"pdf",sep=".")
    pdf(file=pdfname)
    plot(myfiles[[1]]$mae, myfiles[[1]]$auc, main=error.plot.title, xlab="Mean Absolute Error (MAE)", ylab="Area under R-O Curve (AUC)", 
         pch=21, bg="black", xlim=c(MAE.axis.min, MAE.axis.max), ylim=c(AUC.axis.min,AUC.axis.max))
    plotcol<-c("black")
    if (length(myfiles) > 1){
      #Create overlapping data plots to compare potentially by GWAS tool
      #assuming that the length of the Winnow files is at least 2
      for (i in 2:length(myfiles)){
        points(myfiles[[i]]$mae, myfiles[[i]]$auc, main=error.plot.title, xlab="Mean Absolute Error (MAE)", ylab="Area under R-O Curve (AUC)",
               pch=21, bg=rainbow(i+1)[i], xlim=c(MAE.axis.min, MAE.axis.max), ylim=c(AUC.axis.min,AUC.axis.max))
        plotcol[i]<-rainbow(i+1)[i]
      }
      legend("topright", legend=filenames, text.font=2, cex=0.63, pt.cex=0.95, pt.bg = plotcol, pch=21)
    }
    dev.off()
  }
  print("Done!")
}
