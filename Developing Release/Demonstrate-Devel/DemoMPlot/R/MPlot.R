#' Function to create a Manhattan Plot from GWAS output
#' 
#' This function allows you to create a Manhattan Plot with the size indicating effect size.
#' All colored points are considered significant at a P-Value of 0.05. 
#' @param dir A character string: input the directory containing the text files you would like to use.
#' @keywords manhattanplot GWAS 
#' @export
#' @examples
#' MPlot(dir="path")

MPlot<-function(dir){
  
  require(ggplot2)
  
  readFiles <- function(dir) {
    setwd(dir)
    files <- Sys.glob("*.txt")
    listOfFiles <- lapply(files, function(x) read.table(x, header=TRUE))
    return(listOfFiles)
  }
  
  myfiles<-readFiles(dir)
  #creates a pdf output file of a Manhattan Plot where the size of the points is correlated to effect size. 
  pdf(file="Manhattan Plot.pdf")
  for (i in 1:length(myfiles)){
    
    p<-ggplot(myfiles[[i]], aes(x=GeneticDistance, y=-log(Pvalue), colour=Pvalue, size=SNPWeight), 
              environment=environment(), xlab="Genetic Distance", ylab="P-Value (-log)") 
    p2<-p + geom_point() + scale_colour_gradient(limits=c(0,0.05), low="blue", high="purple") +
      geom_abline(intercept=-log(0.05), slope=0)
    print(p2)
  }
  dev.off()
}