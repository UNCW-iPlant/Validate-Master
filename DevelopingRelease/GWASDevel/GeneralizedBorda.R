#Code for generalizing the voting algorithm to multiple datasets
#Read in some test data

Voter<-function(dir, data.delim=",", SNP.columns.list, Score.columns.list, threshold=0.05, outname="EnsembleTable.txt"){
  
  readFiles<-function(dir, data.delim){
    setwd(dir)
    files<-Sys.glob(c(".qassoc", "*.csv","*.txt"))
    print(files)
    data.list<-lapply(files, function(x) read.table(x, sep=data.delim, header=T))
    return(data.list)
  }
  
  mydata<-readFiles(dir, data.delim)
  
  Extract<-function(data, SNPcol, Scorecol){
    newdat<-data.frame(data[,SNPcol], data[,Scorecol], row.names=NULL)
    colnames(newdat)<-c("SNP","PVAL")
    return(newdat)
  }
  
  print("Gathering SNP data...")
  sig.SNP.list=c()
  for (i in seq_along(mydata)){
    test<-Extract(mydata[[i]], SNP.columns.list[[i]], Score.columns.list[[i]])
    sig.SNP.list<-c(sig.SNP.list, as.character(subset(test, PVAL < threshold)[,1]))
  }
  remove(test)
  dat<-as.data.frame(table(sig.SNP.list), row.names=NULL, stringsAsFactors=FALSE)
  colnames(dat)<-c("SNP","Vote")
  
  biggest.SNP.list<-function(data.list){
    return(which.max(lapply(data.list, nrow)))
  }
  
  `%notin%`<-function(x,y) !(x %in% y)
  big<-biggest.SNP.list(mydata)
  print("Creating ensemble data frame...")
  max.SNP.col<-SNP.columns.list[[big]]
  full.SNP.list<-mydata[[big]][,max.SNP.col]
  x<-subset(full.SNP.list, full.SNP.list %notin% dat$SNP)
  dat2<-data.frame(x, 0)
  colnames(dat2)<-c("SNP","Vote")
  dat<-rbind(dat, dat2)
  remove(dat2, max.SNP.col)
  dat$Pvalue<-(1/(length(mydata)^dat$Vote))
  write.table(dat, file=outname, sep=",", row.names=FALSE, quote=FALSE)
  print("Done!")
}
