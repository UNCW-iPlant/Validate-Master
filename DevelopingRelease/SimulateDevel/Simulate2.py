## Original Author: Dustin Landers
import argparse
import random
import sys
import math
from scipy.stats.stats import pearsonr
import numpy
import simuPOP as sim
from simuPOP.utils import saveCSV
import os

"""Functions use somewhere in the software"""

# drange produces a set list sequence for incrementing a loop by decimals
def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step

# restricted_float limits the range of a float number between 0.0 and 1.0, returning an error otherwise 
def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

"""Below is the list of "models" to be used in the simulation of a quantitative trait"""

# The additive model assumes a linear and consistent increase for the presence of each allele
def additive_model(geno):
	my_sum = 0
	my_total_sum = 0
	true_count = 0
	snp_count = 0
	for each in geno:
		my_sum += each * effects[snp_count]
		true_count += 1
		if true_count % 2 is 0:
			snp_count += 1
			my_total_sum += my_sum
			my_sum = 0
	my_trait = my_total_sum
	return my_trait

# The main function: executes the obtaining of command-line flags and then executes the simuPOP simulation.
def main():
    
    # First, grab and interpret command line arguments
    parser=argparse.ArgumentParser(description="Command line arguments for Simulate")
    parser.add_argument("-v", "--verbose", help="Triggers verbose mode", action="store_true")
    parser.add_argument("-d", "--distribution", default="normal", choices=["normal", "gamma"], help="Distribution option")
    parser.add_argument("-p1", "--parameter1", default=3.0, type=float, help="Shape parameter (only used if distribution choice is gamma)")
    parser.add_argument("-p2", "--parameter2", default=1.5, type=float, help="Scale parameter (only used if distribution choice is gamma)")
    parser.add_argument("-s", "--size", required=True, type=int, nargs="+", help="Specify population size(s)")
    parser.add_argument("-l", "--loci", required=True, type=int, nargs="+", help="Loci with effects")
    parser.add_argument("-n", "--number", required=True, default=3000, type=int, help="Number of loci per population or sub-population")
    parser.add_argument("-e", "--effect", required=True, type=float, nargs="+", help="Effect size(s) for the loci specified")
    parser.add_argument("-i", "--heritability", default=0.2, type=restricted_float, help="Heritability coefficient for population")
    parser.add_argument("-m", "--mean", default=2.0, type=float, nargs="+", help="Mean(s) for population phenotype(s)")
    parser.add_argument("-g", "--gen", default=5, type=int, help="Number of generations for population to evolve")
    parser.add_argument("-r", "--rrate", default=0.0, type=restricted_float, help="Recombination rate for given population")
    parser.add_argument("-f", "--filename", default="my", type=str, help="Prefix for output file set")
    args = parser.parse_args()
    
    verbose = args.verbose
    if verbose:
        print "Verbose mode"
    distribution = args.distribution
    if verbose:
        print "Simulation will occur with "+distribution+" distribution"
    parameter1 = args.parameter1
    if verbose and distribution=="gamma":
        print "Gamma distrbution will occur with alpha parameter:", parameter1
    parameter2 = args.parameter2
    if verbose and distribution=="gamma":
        print "Gamma distribution will occur with beta parameter", parameter2
    individuals = args.size
    if verbose:
        print "Population size(s) set at", individuals
    loci = args.loci
    if verbose:
        print "Loci positions per individual set as", loci
    number = args.number
    if verbose:
        print "Number of loci per population set as", number
    global effects
    effects = args.effect
    if verbose:
        print "Effects for loci per individual are", effects
    heritability = args.heritability
    mean = args.mean
    if len(mean) == 1 and len(individuals) > 1:
        mean = numpy.array(mean)
        mean = numpy.repeat(mean, len(individuals), axis=0)
        mean = list(mean)
    if verbose:
        print "Population mean(s) set as", mean
    gen = args.gen
    if verbose:
        print "Number of generations to evolve set as", gen
    rrate = args.rrate
    if verbose:
        print "Recombination rate set as", rrate
    filename = args.filename
    if verbose:
        "File will be saved as", filename
    
    ## Start quantitative trait simulation via simuPOP
    if verbose:
        print "Creating population..."
    pop = sim.Population(size=individuals, loci=int(number), infoFields=["qtrait"])
    if verbose:
        print "Evolving population..."
    type(gen)
    pop.evolve(initOps=[sim.InitSex(), sim.InitGenotype(prop=[0.7, 0.3])], matingScheme=sim.RandomMating(ops=sim.Recombinator(rates=rrate)),postOps=[sim.PyQuanTrait(loci=loci, func=additive_model, infoFields=["qtrait"])], gen=gen)
    
    if verbose:
	print "Coalescent process complete. Population evolved with", pop.numSubPop(),"sub-populations."
    
    genotypes = list()
    for i in pop.individuals():
        genotypes.append(i.genotype())
    
    phenotypes = list()
    for i in pop.individuals():
	phenotypes.append(i.qtrait)
    
    # fun() obtains the heritability equation set to zero for various settings of sigma (standard deviation)
    def fun(sigma, h):
        x_exact = list()
        count = 0
        for i in phenotypes:
            current_mean = mean[pop.subPopIndPair(count)[0]]
            x_exact.append(current_mean + i)
            count += 1
        x_random = list()
        count = 0
        for each in phenotypes:
            current_mean = mean[pop.subPopIndPair(count)[0]]
            x_random.append(random.normalvariate(current_mean + each, sigma))
            count += 1
        r = pearsonr(x_exact, x_random)[0]
        return r - math.sqrt(h)

    if verbose:
        print "Building polynomial model for variance tuning..."

    # Polyfit fits a polynomial model in numpy to the values obtained from the fun() function
    points = list()
    for i in drange(0, max(effects)*10, 0.001):
        points.append(i)
    y_points = list()
    for i in points:
        y_points.append(fun(i, heritability))
    z = numpy.polyfit(x=points, y=y_points, deg=3)
    p = numpy.poly1d(z)

    # Netwon's method finds the polynomial model's roots
    def newton(p):
        xn = 100
        p_d = p.deriv()
        count = 0
        while abs(p(xn)) > 0.01:
            if count > 1000:
                print "Unable to converge after 1000 iterations...\nPlease choose different settings."
                sys.exit()
            count += 1
	    xn = xn - p(xn)/p_d(xn)
	if xn < 0.0:
	        xn = 0.0
	if verbose:
	    print "Estimated variance of phenotypes for specified heriability: ", xn
	return xn

    if verbose:
        print "Using Newton's method to find polynomial roots..."

    # Files are saved to the specified location
    estimated_variance = newton(p)
    new_phenotypes = list()
    count = 0
    for each in phenotypes:
        current_mean = mean[pop.subPopIndPair(count)[0]]
        if distribution=="normal":
            new_phenotypes.append(random.normalvariate(current_mean + each, estimated_variance))
	elif distribution=="gamma":
	    new_phenotypes.append(random.gammavariate((current_mean + each)/parameter2, numpy.sqrt(estimated_variance/parameter1)))
	count += 1
	
    f = open(filename + "_qtrait.txt", "w")
    f.write("\n".join(map(lambda x: str(x), new_phenotypes)))
    f.close()

    numpy.savetxt(filename + "_kt_ote.txt", numpy.column_stack((loci, numpy.array(effects))), fmt='%i %10.7f')
    saveCSV(pop, filename + "_genomes.csv")
    
    # Call the convert.R script to convert the output into usable PLINK files
    # Will probably need to change this line to something more generalizable in the near future
    
    os.system("Rscript convert.R "+filename)
    print "\n\n"

if __name__ == "__main__":
	main()