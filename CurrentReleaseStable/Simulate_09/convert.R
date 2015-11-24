#!/usr/bin/Rscript
args<-commandArgs(trailingOnly=TRUE)
filename<-args[1]

make.ped <- function(prefix) {
  gen <- read.csv(file=paste(prefix,"_genomes.csv",sep=""),header=T)
  sex <- gen$sex
  qtrait <- read.table(file=paste(prefix,"_qtrait.txt",sep=""),header=F)
  gen <- gen[,3:ncol(gen)]
  gen <- ifelse(gen==1,"A","B")
  ped <- matrix(nrow=nrow(gen),ncol=6)
  ped[,1] <- rep(1,nrow(gen))
  ped[,2] <- c(1:nrow(gen))
  ped[,3] <- rep(0,nrow(gen))
  ped[,4] <- rep(0,nrow(gen))
  ped[,5] <- ifelse(sex=="M",1,2)
  ped[,6] <- qtrait$V1
  final <- cbind(ped,gen)
  return(final)
}
  
make.map <- function(prefix) {
  gen <- read.csv(file=paste(prefix,"_genomes.csv",sep=""),header=T)
  my.names.len <- (length(names(gen))-2)/2
  map <- matrix(nrow=my.names.len,ncol=4)
  map[,1] <- rep(1,nrow(map))
  map[,2] <- c(1:my.names.len)
  map[,3] <- rep(0,nrow(map))
  map[,4] <- c(1:my.names.len)
  return(map)
}

make.pheno <- function(prefix) {
  gen <- read.csv(file=paste(prefix,"_genomes.csv",sep=""),header=T)
  qtrait <- read.table(file=paste(prefix,"_qtrait.txt",sep=""), header=F)
  pheno <- matrix(nrow=nrow(gen),ncol=3)
  pheno[,1] <- rep(1,nrow(gen))
  pheno[,2] <- c(1:nrow(gen))
  pheno[,3] <- qtrait$V1
  return(pheno)
}

write.file <- function(prefix) {
  ped <- make.ped(prefix)
  map <- make.map(prefix)
  pheno <- make.pheno(prefix)
  write.table(ped,file=paste(prefix,".ped",sep=""),quote=F,row.names=F,col.names=F)
  write.table(map,file=paste(prefix,".map",sep=""),quote=F,row.names=F,col.names=F)
  write.table(pheno,file=paste(prefix,".pheno",sep=""),quote=F,row.names=F,col.names=F)
}

write.file(prefix=filename)
cat("File",filename,"converted to PEDMAP\n",sep=" ")