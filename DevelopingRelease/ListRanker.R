args<-commandArgs(trailingOnly=TRUE)
maindir<-args[1]
tp_file<-args[2]
fp_file<-args[3]
ListRanker<-function(dir, filename.tp, filename.fp){
  readFiles <- function(dir) {
    setwd(dir)
    files <- Sys.glob("*.txt")
    listOfFiles <- lapply(files, function(x) read.table(x, header=TRUE))
    return(listOfFiles)
  }
  myfiles<-readFiles(dir)
  tp<-fp<-list()
  for (i in 1:length(myfiles)){
    tp[[i]]<-myfiles[[i]]$tp
    fp[[i]]<-myfiles[[i]]$fp
  }
  listrank<-function(tps){
    l<-lapply(tps, function(x) rank(x, ties.method="first"))
    return(l)
  }
  rankedlist.tp<-as.matrix(listrank(tp))
  rankedlist.fp<-as.matrix(listrank(fp))
  MASS::write.matrix(rankedlist.tp, file=filename.tp, sep = ",")
  MASS::write.matrix(rankedlist.fp, file=filename.fp, sep = ",")
}