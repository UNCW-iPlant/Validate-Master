#Simulate: A Data Generation Program for Genome Wide Association Studies Tool Analysis

###NOTE:
This README is for the full documentation related to the Simulate program. If you want to dive right in and spare yourself some reading, **[head over to the Quickstart guide](https://github.com/UNCW-iPlant/Quickstart-guide/blob/master/docs/Simulate.md)**. If you want a more thorough explanation of Simulate's options and inner workings, read on.

###Documentation:
Simulate is a Python script that runs directly from the command line. It is a forward-in-time genetic individual-based simulation software that evolves for a specified number of generations and estimates a quantitative trait from an additive model given an initial mean value.

In the context of the Validate Workflow, the Simulate program allows for on-the-fly data generation if you do not already have any data of your own. Furthermore, Simulate exports this data into the ubiquitous PED/MAP formats for compatibility with most Genome Wide Association Studies (GWAS) tools. It also has many options and features for customization, with more appearing with each version. The foundation of this program is the simuPOP Python package. For more information on that package, [check its sourceforge page.](http://simupop.sourceforge.net/Main/HomePage)

The full list of command-line options for Simulate is as follows:
* **-v** or **--verbose**: Triggers verbose mode which explicity states each option before running and prints statements at each step of the simulation process.

* **-s** or **--size**: One or more integers, separated by commas with no spaces, indicating the size of your population or sub-populations. Ideally, you should place these values above 100, as any number below that will result in a population convergence and an error in the program.

* **-n** or **--number**: An integer, indicates the number of genetic markers per individual. This number will be one of the key determinants of the size of the final output, and will influence how frequently the effects of the loci will change per generation. If multiple subpopulations are specified, the individuals of all subpopulations will have the number of markers denoted by *n*

* **-l** or **--loci**: A list of integers, starting with 0 (e.g. 0,1,2) to denote which number of loci will have the effects. For example, if `-l 0,1,2` is chosen, then individuals having 0 loci, 1 locus, or 2 loci will have some kind of effect, the exact effect being represented with the next command line argument...

* **-e** or **--effect**: A list of floating point numbers equal in length to the list given by `-l`; indicates the actual effect on the phenotype having said number of loci will have. Using the above example with 0,1, and 2 loci having effects, if one listed `-e 0.2,0.2,0.2`, then in this case each additional loci would contribute 0.2 units to the phenotype of an individual.

* **-m** or **--mean**: One or multiple floating point numbers separated by commas. The length of the list should not exceed the number of subpopulations specified. Represents the mean of the phenotype for your population or subpopulation. If only one number is given for the mean when multiple subpopulations exist, then the mean will apply to all (sub)population(s).

* **-i** or **--heritability**: Decimal between 0 and 1. Denotes the heritability coefficient for your (sub)population(s). The heritability coefficient in this program means the probability of an individual inheriting a given set of loci and effects from a parent individual.

* **-g** or **--gen**: A single integer, indicates the number of generations you wish to have your (sub)population(s) evolve. To get reliable output, we recommend a number above 50.

* **-r** or **--rate**: Decimal value between 0 and 1. Denotes the genetic recombination rate of your (sub)population(s). The genetic recombination rate is the proportion of offspring in a population that will have a combination of traits not found in either of the individual's parents.

* **-d** or **--distribution**: The underlying distribution of your population. Can either be 0 for normal distribution (the default option) or 1 for gamma distribution. Any other number will result in an error (for now...) If option 1 is chosen-the gamma distribution-then you will need to fill in the next two arguments:

  * **-p1** or **--parameter1**: A single floating point number. Denotes the *shape parameter* of your population's underlying gamma distribution (only required if gamma distribution was chosen as an input above).

  * **-p2** or **--parameter2**: A single floating point number. Denotes the *scale parameter* of your population's underlying gamma distribution (only required if gamma distribution was chosen as an input above).

* **-f** or **--filename**: A character string. Indicates the name to be attached to all Simulate outputs. For example, if filename was *MyResults*, then the genomic information file would be *MyResults_genomes.csv*

These command-line arguments need not be in any particular order; however, we do at least recommend that any flags with no arguments (e.g. the verbose flag) be placed before those flags which require arguments.

The final output for Simulate will be four files:
  1. A set of PED/MAP files with the final genetic information of your (sub)population(s). This will likely be the file set that you want to use for the actual GWA study. 
  2. A known-truth file which will be required for later tool testing with Winnow. 
  3. A .csv file with the genomic information of your population
