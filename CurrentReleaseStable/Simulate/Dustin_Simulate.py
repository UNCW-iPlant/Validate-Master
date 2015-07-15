## Original Author: Dustin Landers
import getopt
import random
import sys
import math
from scipy.stats.stats import pearsonr
import numpy
import simuPOP as sim
from simuPOP.utils import saveCSV

"""Functions use somewhere in the software"""

# drange produces a set list sequence 
def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step


# usage() prints to the screen the help messages; in other words, the possible command-lines to be used in the execution the software
def usage():
	#print "\n"
	print "-h or --help for help"
	print "-v or --verbose for verbose"
	print "-s or --size to specify population size/s"
	print "-n or --number to specify number of loci"
	print "-l or --loci to specify loci with effects (separated by commas w/ no spaces)"
	print "-e or --effect to specify corresponding loci effects (separated by commas w/ no spaces)"
	print "-i or --heritability for specifying heritability (between 0 and 1)"
	print "-m or --mean for specifying population/s mean (seperated by commas w/ no spaces if multiple populations)"
	print "-g or --gen for the number of generations for the coalescent model to evolve"
	print "-r or --rrate to specify a recombination rate (between 0 and 1)"
	print "-f or --filename for naming output in CSV format"

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

	# Check for arguments passed
	try:
		opts, args = getopt.getopt(sys.argv[1:], shortopts="vhs:n:l:e:f:i:m:g:r:", longopts=["verbose", "help", "size=", 
			"number=", "loci=", "effect=", "mean=", "filename=", "heritability=", "gen=", "rrate="])

	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit()

	verbose = False
	filename = "my"
	size = 1000
	number = 100
	heritability = 0.2
	mean = 2.0
	gen = 5
	rrate = 0.0
	print "\n"

	for o in opts:
		if o[0] in ("-v", "--verbose"):
			verbose = True
			print ("Verbose mode")
	for o in opts:
		if o[0] in ("-s", "--size"):
			individuals = o[1].split(",")
			individuals = map(int, individuals)
			if verbose:
				print "Population size/s is set at", individuals
	for o in opts:
		if o[0] in ("-h", "--help"):
			usage()
			sys.exit()
		elif o[0] in ("-n", "--number"):
			number = o[1]
			if verbose:
				print "Number of loci per individual is set at", number
		elif o[0] in ("-l", "--loci"):
			global loci
			loci = o[1].split(",")
			loci = map(int, loci)
			if verbose:
				print "Loci positions per individual are:", loci
		elif o[0] in ("-e", "--effect"):
			global effects
			effects = o[1].split(",")
			effects = map(float, effects)
			if verbose:
				print "Effects for loci per individual are:", effects
		elif o[0] in ("-f", "--filename"):
			filename = o[1]
			if verbose:
				print "File will be saved as:", filename
		elif o[0] in ("-i", "--heritability"):
			heritability = float(o[1])
			if verbose:
				print "Heritability for simulation specified as:", heritability
		elif o[0] in ("-m", "--mean"):
			mean = o[1].split(",")
			mean = map(float, mean)
			if len(mean) == 1 and len(individuals) > 1:
				mean = numpy.array(mean)
				mean = numpy.repeat(mean, len(individuals), axis=0)
				mean = list(mean)
			if verbose:
				print "Population mean/s specified as:", mean
		elif o[0] in ("-g", "--gen"):
			gen = int(o[1])
			if verbose:
				print "Generations to evolve specified as:", gen
		elif o[0] in ("-r", "--rrate"):
			rrate = float(o[1])
			if verbose:
				print "Recombination will occur with rate:", rrate


	## Start quantitative trait simulation
	if verbose:
		print "Creating population..."

	pop = sim.Population(size=individuals, loci=int(number), infoFields=["qtrait"])

	if verbose:
		print "Evolving population..."

	pop.evolve(initOps=[sim.InitSex(), sim.InitGenotype(prop=[0.7, 0.3])], 
		matingScheme=sim.RandomMating(ops=sim.Recombinator(rates=rrate)),
	           postOps=[sim.PyQuanTrait(loci=loci, func=additive_model, infoFields=["qtrait"])],
	           gen=gen)

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

	# Fits a polynomial model in numpy to the values obtained from the fun() function
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
				usage()
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
		new_phenotypes.append(random.normalvariate(current_mean + each, estimated_variance))
		count += 1

	f = open(filename + "_qtrait.txt", "w")
	f.write("\n".join(map(lambda x: str(x), new_phenotypes)))
	f.close()

	numpy.savetxt(filename + "_kt_ote2.txt", numpy.column_stack((loci, numpy.array(effects))))

	saveCSV(pop, filename + "_genomes.csv")
	print "\n\n"


if __name__ == "__main__":
	main()
