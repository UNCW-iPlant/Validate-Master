args <- commandArgs(TRUE)
dir <- as.character(args[1])


source("Demonstrate_Stampede_Edition.R")
source("lineplotCI.R")
Demonstrate(dir)