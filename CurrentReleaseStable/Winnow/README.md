#Winnow: Known-Truth Testing for Genome Wide Association Studies Tools

##Note:
This README is for the full documentation related to the Winnow program. 
If you just want to dive right in and spare yourself some reading, **[head over to the Quickstart guide.](https://github.com/UNCW-iPlant/Quickstart-guide/blob/master/docs/Winnow.md)** 
If you want a more thorough explanation of Winnow's options and inner workings, read on.

##Documentation:
The bread-and-butter of the Validate Workflow, Winnow (formerly the eponymous Validate), is a Python-compatible known truth testing tool for genome wide association studies (GWAS). Quite simply, Winnow is a tool that evaluates other tools. 
Winnow requires output from a GWAS tool after analyzing a data set. Given the "known truth" of said data set, Winnow outputs a series of fit statistics to determine 
the validity of the GWAS tool and whether or not it was truly useful in analyzing the data. In particular, Winnow is useful for ascertaining which analysis tool may be best for a given data set.
Though Winnow's outputs may be sufficient for some researchers to make an appropriate conclusion, one may also feed the Winnow output into the final part of the workflow: Demonstrate.

Before we get into the command-line arguments necessary for Winnow, it may be beneficial to go over the required layout for certain input files.
Please note that the actual file extension does not matter so much as the layout of the file itself. For instance, though it is preferable that the known-truth file have a .txt extension,
it is not necessary as long as the file is layed out in the following format:

###Known-Truth File

The known-truth file from your analyses may be arranged in either two rows or two columns. Also, there are two acceptable formats for the known-truth file:
  * OTE: Only Truth and Effect. As the name implies, this format only lists those SNPs which are known to have a significant effect, along with their corresponding effect values (in this case, the SNP weight or effect size column would be mandatory in the GWAS output folder)
  * FGS: Full Genome Set. This type of file lists all of the SNPs in the given dataset along with each of their corresponding effect sizes or weights.
    * The known-truth file must be a text file which is separated either by whitespace (regular spacing or tab) or commas 

Here is an example of an OTE known-truth file:

![ExampleKT](https://pods.iplantcollaborative.org/wiki/download/attachments/14582582/Screen%20Shot%202015-02-05%20at%201.29.03%20PM.png?version=1&modificationDate=1423340032000&api=v2)

###GWAS Analysis Files

The input files for Winnow must be output from GWAS analysis tools to obtain an accurate reading; however, because many different GWAS tools exist, the format(s) must be standardized for practical use.
* Data must be arranged into columns, not rows
  * Spreadsheet format (more specifically, CSV) is preferred, but not required
  * The following columns are required for any file format:
    * A column denoting the particular SNP being analyzed
    * A column with the significance score indicating whether or not a SNP is statistically significant (e.g. a p-value column)
* Other columns that may be included are:
  * A column indicating the effect size or weight of a given SNP for determining a phenotype value 

Here is an example of a GWAS results file (from PLINK):
![ExampleGWAS](https://pods.iplantcollaborative.org/wiki/download/attachments/14582582/Screen%20Shot%202015-02-05%20at%201.26.27%20PM.png?version=1&modificationDate=1423339997000&api=v2)

As with the other programs, Winnow is a command-line ready Python program, and like the other steps in the workflow, command-line arguments are required for Winnow to work properly.
In particular, the full list of command-line arguments is as follows:

###Required Arguments

* **-F** or **--Folder**: A string representing the name of the folder where all GWAS analysis outputs are stored. 
Note that this assumes all analyses you wish to run through Winnow already have been aggregated into a folder. 
Also, *be sure to explicity type the full path to the folder if it is not in your current working directory!*

* **-C** or **--Class**: A string denoting the name of the known truth file for your data set. 
Like the Folder argument, remember to explicitly type the full path to the folder if it is not in your current working directory.
The requirements for the known-truth file layout are in the next section. 

* **-S** or **--SNP**: A string representing the name of the SNP column in the GWAS output. 
Because you may only use one option for this argument, all of your GWAS outputs should have the same name for the column.

* **-P** or **--Score**: A string representing the name of the score column in the GWAS output.
Normally, this column will have a name like *P-value* or *P*. 
Quite simply, this column shows the p-values indicating significant SNPs.

* **-k** or **--kttype**: Two options, either "OTE" or "FGS". Indicates the type of known-truth file. 
The "OTE" option stands for "Only Truth and Effect," meaning that only those SNPs deemed significant, along with their effect sizes, are listed.
The "FGS" option stands for "Full Genome Set," meaning that all SNPs along with their effect sizes are listed, regardless of significance.

###Optional Arguments

* **-v** or **--verbose**: Requires no argument. Command-line flag that triggers verbose mode which explicity states each option before running.
Set to False by default (i.e. not verbose mode).

* **-f** or **--filename**: A string representing the name of your Winnow output file. 
This option does not necessarily have to be included, and the default output name will just be *MyResults.txt*.
Please note, however, that the *.csv extension may be used in the filename to have the output returned in CSV format.

* **-a** or **--analysis**: A string, either "GWAS" or "prediction", specifies the type of analysis (currently, only GWAS is available and if left blank, Winnow assumes GWAS).
Prediction methods for missing values is forthcoming in later versions. Set to "GWAS" by default.

* **-t** or **--threshold**: A decimal number between 0 and 1. 
Represents the desired threshold for certain classification metrics (i.e. the threshold at which certain SNPs would be deemed significant).
Set to 0.05 by default.

* **-s** or **--seper**: Two options: "comma" or "whitespace." Indicates the delimiter used in the GWAS analysis outputs. If the file is separated by tabs or spaces, use "whitespace." If the file is in CSV format, use "comma."
Set to "whitespace" by default.

* **-b** or **--beta**: A character string representing the effect size column in the GWAS results outputs. 
Set to "None" by default. If beta is kept at None, this will produce a different set of fit statistics than a dataset with an effect size column. 
More specifically, certain statistics (such as RMSE and the correlation coefficient) will be excluded from the final results if the beta column is not specified.

* **-r** or **--kttypeseper**: Two options: "comma" or "whitespace." Indicates the delimiter used in the known-truth file.
Set to "whitespace" by default.

An example of running Winnow from the command line with these options would look like so:

`python winnow.py --verbose --Folder Example_Data/OutputPlink --Class Example_Data/kt.ote --Snp SNP --Score P --beta BETA --filename ~/Desktop/MyResults --seper whitespace --kttype OTE --kttypeseper whitespace`

###The Output File

The output file for Winnow, specified with whatever name you chose, contains 16 columns, and the number of rows depends on how many results files were placed in the aggregated folder. 
Each column indicates a particular fit statistic with each row indicating one GWAS result file. 
The 16 fit statistics currently used in Validate are…

* Mean absolute error^
* Root mean-squared error (RMSE)^
* Pearson’s correlation coefficient (r)^
* Coefficient of determination (r^2)^
* Area under the receiver-operator curve (AUC)
* True/False positives
* True/False negatives
* True/False positive rates
* True/False negative rates
* Total precision (defined as true positives divided by sum of true and false positives)
* Error (defined as the total number of falses, positive or negative, divided by the total)
* Sensitivity
* Specificity, and
* Youden statistic

^Statistic excluded from the final output if a beta/effect size column is not included in the command line.

Here is an example of what the final Winnow output will look like:
![Example](https://pods.iplantcollaborative.org/wiki/download/attachments/14582582/Screen%20Shot%202015-02-12%20at%2011.57.00%20AM.png?version=1&modificationDate=1423760331000&api=v2)

We recommend referring to the AUC, RMSE, and true/false positive rates when making a judgment call on whether or not a tool is appropriate for a given dataset.
Remember, for RMSE and false positives, lower numbers are better! For AUC the closer to 1, the better! And obviously, higher true positive counts are better as well.

If all you need are the fit statistics, you may simply end the workflow here; however, if you wish to convert your Winnow results into more human-readable output, please
consult [the full documentation](Demonstrate/README.md) or [the Quickstart-guide](https://github.com/UNCW-iPlant/Quickstart-guide/blob/master/docs/Demonstrate.md) for Demonstrate.
