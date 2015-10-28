# Demonstrate: A Data Visualization Tool for Summarizing Validate Output (version 0.9)

Demonstrate is the final step in the Validate known-truth pipeline for iPlant Collaborative. It produces a single data set from several Winnow results files as well as human-readable graphics showing differences in a GWAS/QTL applications performance under varying heritability and population structure. Furthermore, the Demonstrate2 function allows for visualizations of other data sets regardless of whether or not population structure or heritability is included. Like the original function, Demonstrate2 also creates graphics showing differences in GWAS/QTL applications; however, since Demonstrate2 does not account for heritability or population structure, it instead creates other graphics: scatterplots based on AUC/MAE and true/false positives, true and false positives histograms for each dataset, and a comparison table based on precision, sensitivity, and specificity.

**Now included for version 0.9:** An additional [Manhattan plot](https://en.wikipedia.org/wiki/Manhattan_plot) function, *MPlot*, is now available in the Demonstrate package. This Manhattan plot allows one to bypass the Winnow program entirely and directly plot any GWAS output based on transformed P-values in relation to genetic distance. An example of this Manhattan Plot is shown under the usage section. In addition, the scatterplots in the Demonstrate2 function have been updated to color regions of high true/false positive concentration along with plotting the individual points. 

###Requirements 
The requirements for running the DemoMPlot package smoothly are:
* R version >= 3.2.1
* Package *plyr*
* Package *ggplot2*

##Usage
Please note that to use any of these functions, you must first download and install the package from Github. Once downloaded, boot up an R or RStudio session, and install DemoMPlot with the following command:

`install.packages("DemoMPlot.tar.gz", repos=NULL, type="source")`

Once this is done, type `library(DemoMPlot)` to load the package. If the prompt returns with no additional feedback, the loading process worked.

###Demonstrate usage

NOTE: All of these details are also included under the *man* folder in the DemoMPlot package itself; however, this README documentation has been included for convenience.

`Demonstrate(dir, outputdir=NULL, settingsfile=NULL, make.AUC.plot=TRUE, AUC.plot.title="Mean AUC By Population Structure and Heritability", make.MAE.plot=TRUE, MAE.plot.title="Mean MAE By Population Structure and Heritability",herit.strings=list("_03_","_04_","_06_"),herit.values=list(0.3,0.4,0.6),struct.strings=list("PheHasStruct","PheNPStruct"),struct.values=list(TRUE,FALSE))`

  * *dir:*  The directory where your Winnow outputs are stored (must give full path!)
  * *make.AUC.plot:* Boolean value (i.e. either TRUE or FALSE). Indicates to the function whether or not to run the Area under the RO curve lineplot
  * *AUC.plot.title:* Character string, only necessary if the previous option is TRUE.  Gives the main title for the AUC lineplot.
  * *make.MAE.plot:* Boolean value. Indicates whether or not to include the Mean absolute error by heritability lineplot
  * *MAE.plot.title*: Character string, only necessary if previous option is TRUE; gives main title for MAE lineplot
  * *herit.strings/herit.values:* lists of strings and numbers, respectively. Denotes the strings to look for indicating different heritability values in datasets and the heritability values those strings correspond to. Must be in the proper order! (e.g. the string 03 corresponds to the heritability value 0.3, so both are first in their respective lists, and so on)
  * *struct.strings/struct.values:* lists of strings and boolean values, respectively. Denotes the strings in dataset names to look for when separating by population structure and the population structure states those strings correspond to; optional for both plots. Must be in the proper order!

Assuming all options are used, Demonstrate will give two outputs: a lineplot of heritability by AUC, separating datasets by whether or not they have population structure and a lineplot of heritability by MAE, similarly separated by population structure. Both of these plots will be in PDF format. Examples shown below:`

[AUC Plot for original Demonstrate](https://pods.iplantcollaborative.org/wiki/download/attachments/18188259/AUC-pop-structure.JPG?version=1&modificationDate=1434060411000&api=v2)

[MAE Plot for original Demonstrate](https://pods.iplantcollaborative.org/wiki/download/attachments/18188259/MAE-pop-structure.JPG?version=1&modificationDate=1434060431000&api=v2)

###Demonstrate2 usage

`Demonstrate2(dir, make.pos.plot=TRUE, pos.plot.title="True Positives by False Positives", make.error.plot=TRUE, error.plot.title="Plot of AUC by MAE", extra.plots=TRUE, AUC.axis.min=0, AUC.axis.max=1.0, MAE.axis.min=0, MAE.axis.max=2.0)`

  * *dir:*  The directory where your Winnow outputs are stored (must give full path!)
  * *make.pos.plot:* Boolean value (i.e. either TRUE or FALSE). Indicates whether or not to create the true positive by false positive scatterplot
  * *pos.plot.title:* Character string. Denotes the main title for the True Positives by False Positives scatterplot; only necessary if make.pos.plot is set to TRUE
  * *make.error.plot:* Boolean value. Indicates whether the program creates the AUC by MAE scatterplot
  * *error.plot.title:* Character string. Denotes the main title for the AUC by MAE scatterplot
  * *extra.plots:* Boolean value. Determines if the true/false positive histograms and comparison tables are created along with other plots
  * *AUC.axis.min:* Floating point number. Gives the lower boundary of the x-axis on the AUC by MAE scatterplot
  * *AUC.axis.max:* Floating point number. Gives the upper boundary of the x-axis on the AUC by MAE scatterplot
  * *MAE.axis.min:* Floating point number. Gives the lower boundary of the y-axis on the AUC by MAE scatterplot
  * *MAE.axis.max:* Floating point number. Gives the upper boundary of the y-axis on the AUC by MAE scatterplot

Assuming all options are used in the function call, Demonstrate2 will give five outputs: a scatterplot of true positives by false positives, color coded by Winnow file source, true/false positive histogram sets separate for each dataset, a scatterplot of MAE by AUC color coded by source, and a Comparison Table comparing the average specificity, sensitivity, and precision among Winnow files. All files except the comparison table will be in PDF format (Comparison Table will be in CSV format). Examples are linked below:

[MAE by AUC scatterplot](https://github.com/UNCW-iPlant/Validate-Master/files/538/My.Error.Plot.pdf)

###Demonstrate With Python Usage

The Python implementation of Demonstrate works similar to the original program and provides the same output. The most important difference is the syntax to run the program. 

To see all of the possible options, type this command into the terminal/command line from the directory containing demonstrate.py:

`python demonstrate.py --help`

Though there are quite a few possible options, the following are the only arguments that are needed for both versions of Demonstrate: 
* **--verbose** (or **-v**) to trigger verbose mode 
* **--dir** (or **-d**) which denotes the folder of input files (_required_)
* **--output** (or **-o**) which denotes the folder to store the output. This is optional and the input folder will be used if this is not specified
* **--settings** (or **-s**) which denotes the .param file from Winnow containing the settings used to be included on the output plots. This is optional and not used by default
* **demonstrate** or **demonstrate2** to specify which version of Demonstrate to use (_required_)

To run Demonstrate with only these settings; note the only 2 _required_ settings are **--dir** and the mode

`python demonstrate.py --verbose --dir ~/Documents/DemInputFiles --output ~/Documents/DemOutput --settings ~/Documents/DemInputFiles/winnowoutput.param demonstrate`

`python demonstrate.py --verbose --dir ~/Documents/Dem2InputFiles --output ~/Documents/Dem2Output --settings ~/Documents/Dem2InputFiles/winnowoutput.param demonstrate2`

####Extra Parameters

These have default settings but can be changed by adding the argument after the mode (e.g. after "demonstrate")

####Demonstrate

* **--xauc** (or **-a**) to exclude the AUC by Population Structure and Heritability plot (not set _by default_)
* **--auctitle** (or **-t**) to specify the AUC plot title ("Mean AUC by Population Structure and Heritability" _by default_)
* **--xmae** (or **-m**) to exclude the MAE by Population Structure and Heritability plot (not set _by default_)
* **--maetitle** (or **-y**) to specify the MAE plot title ("Mean MAE by Population Structure and Heritability" _by default_)
* **--heritstring** (or **-r**) to specify the heritability string found in the input data ("\_03_","\_04_","\_06_" _by default_)
* **--heritvalue** (or **-l**) to specify the heritability value found in the input data (0.3, 0.4, 0.6 _by default_)
* **--structstring** (or **-u**) to secify the structure string found in the input data ("PheHasStruct", "PheNPStruct" _by default_)
* **--structvalue** (or **-p**) to specify the structure value found in the input data (True, False _by default_)

#####Run Example (Including all plots)

`python demonstrate.py --verbose --dir ~/Documents/DemInputFiles --output ~/Documents/DemOutput --settings ~/Documents/DemInputFiles/winnowoutput.param demonstrate --auctitle AUC --maetitle MAE --heritstrig _03_ _04_ _06_ --heritvalue 0.3 0.4 0.6 --structstring PheHasStruct PheNPStruct --structvalue True False`

####Demonstrate2
* **--xpos** (or **-q**) to exclude the True Positives by False Positives plot (not set _by default_)
* **--postitle** (or **-i**) to specify the True Positives by False Positives plot title ("True Positives by False Positives _by default_)
* **--xerror** (or **-e**) to exclude the error plot (not set _by default_)
* **--errortitle** (or **-w**) to specify the error plot title ("Plot of AUC by MAE" _by default_)
* **--extraplots** (or **-x**) to exclude the extra plots (not set _by default_)
* **--aucmin** (or **-z**) to specify minimum axis value for the AUC plot (0 _by default_)
* **--aucmax** (or **-b**) to specify maximum axis value for the AUC plot (1.0 _by default_)
* **--maemin** (or **-n**) to specify minimum axis value for the MAE plot (0 _by default_)
* **--maemax** (or **-c**) to specify minimum axis value for the MAE plot (2.0 _by default_)

#####Run Example (Including all plots)

`python demonstrate.py --verbose --dir ~/Documents/Dem2InputFiles --output ~/Documents/Dem2Output --settings ~/Documents/Dem2InputFiles/winnowoutput.param demonstrate2 --postitle TPbyFP --errortitle AUCbyMAE --aucmin 0 --aucmax 1.5 --maemin 0 --maemax 2.5`

###MPlot usage

`MPlot(dir)`

* *dir*: The directory where your GWAS ouputs are stored.

This function will create a [Manhattan plot](https://en.wikipedia.org/wiki/Manhattan_plot) for all individual GWAS output files in a given folder. These Manhattan plots show genetic distance for SNPs plotted by the -log(P-value), and the plots have a color coded cutoff for significance at -log(0.05). Please note that for the Manhattan plot to work, the GWAS output must actually include a valid genetic distance column. A sample plot is linked below: 

[Manhattan Plot](https://github.com/UNCW-iPlant/Validate-Master/files/535/Manhattan.Plot.pdf)
