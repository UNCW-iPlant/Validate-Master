Demonstrate2<-function(dir, make.pos.plot=TRUE, pos.plot.title="True Positives by False Positives",
                       make.error.plot=TRUE, error.plot.title="Plot of AUC by MAE", extra.plots=TRUE, 
                       AUC.axis.min=0, AUC.axis.max=1.0, MAE.axis.min=0, MAE.axis.max=2.0){
  
  require(ggplot2)
  require(plyr)
  
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
      hist(myfiles[[i]]$TruePositives, main=paste(filenames[[i]]," True Positives",sep=":"), xlab="True Positives")
    }
    dev.off()
    pdf(file="FP Histograms.pdf")
    for (i in 1:length(myfiles)){
      hist(myfiles[[i]]$FalsePositives, main=paste(filenames[[i]]," False Positives",sep=":"), xlab="False Positives")
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
    for (i in 1:length(myfiles)){
      attach(myfiles[[i]])
      myfiles[[i]]$file <- sQuote(i)
      detach(myfiles[[i]])
    }
    
  #Determines maximum value of all true positives
  tpmax<-function(list){
    tps<-list()
    for (i in 1:length(list)){
      tps[[i]]<-list[[i]]$TruePositives
    }
    y<-unlist(lapply(tps, max))
    return(max(y))
  }
  ta<-tpmax(myfiles)
  #Determines minimum value of all true positives
  tpmin<-function(list){
    tps<-list()
    for (i in 1:length(list)){
      tps[[i]]<-list[[i]]$TruePositives
    }
    y<-unlist(lapply(tps, min))
    return(min(y))
  }
  tb<-tpmin(myfiles)
  #Determines median value of all true positives
  tpmed<-function(list){
    tps<-list()
    for (i in 1:length(list)){
      tps[[i]]<-list[[i]]$TruePositives
    }
    y<-unlist(lapply(tps, median))
    return(median(y))
  }
  tc<-tpmed(myfiles)
  #Determines maximum value of all false positives
  fpmax<-function(list){
    fps<-list()
    for (i in 1:length(list)){
      fps[[i]]<-list[[i]]$FalsePositives
    }
    y<-unlist(lapply(fps, max))
    return(max(y))
  }
  fa<-fpmax(myfiles)
  #Determines minimum value of all false positives
  fpmin<-function(list){
    fps<-list()
    for (i in 1:length(list)){
      fps[[i]]<-list[[i]]$FalsePositives
    }
    y<-unlist(lapply(fps, min))
    return(min(y))
  }
  fb<-fpmin(myfiles)
  #Determines median value of all false positives
  fpmed<-function(list){
    fps<-list()
    for (i in 1:length(list)){
      fps[[i]]<-list[[i]]$FalsePositives
    }
    y<-unlist(lapply(fps, median))
    return(median(y))
  }
  fc<-fpmed(myfiles)
  
  all.data<-do.call("rbind", myfiles)
  
  TPFP <- ddply(all.data, .(TruePositives, FalsePositives, file), summarize, count=length(file))
  
  #Creates pdf output
  pdf(file="True Positives vs. False Positives.pdf")
  
  #Creates plot of each file with rectangles from minimums to medians and medians 
  #to maximums of all true and false positives. Points in the green area represent 
  #the "best" outputs, those in the red area represent the "worst", and those in
  #blue areas are "okay". 
  p <- ggplot(TPFP, aes(x=FalsePositives, y=TruePositives), environment=environment())
    
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
    xlim(0, fa) + ylim(0, ta)
  
    print(p2)
  
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
