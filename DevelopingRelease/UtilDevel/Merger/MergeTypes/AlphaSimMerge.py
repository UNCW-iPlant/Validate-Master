from MergeType import MergeType


class AlphaSimMerge(MergeType):
    """
    MergeType children class to handle AlphaSim outputs.

    """
    def __init__(self, output_prefix, snp_path, pedigree_path, gender_path, genotype_path, snp_solution_path,
                 pedigree_tpv_col):
        """
        Initializes the AlphaSimMerge object and its parent class.

        :param output_prefix: Prefix for output files. Extensions will be added below
        :param snp_path: Path to the ChipXSnpInformation.txt file from AlphaSim
        :param pedigree_path: Path to the PedigreeTbvTdvTpv.txt file from AlphaSim
        :param gender_path: Path to the Gender.txt file from AlphaSim
        :param genotype_path: Path to the ChipXGenotype.txt file from AlphaSim
        :param snp_solution_path: Path to the SnpSolution.txt file from AlphaSim
        :param pedigree_tpv_col: column in the pedigree file containing the phenotype value. Defaulted to 9 for the
                                 TPVNormRest1 column
        """
        output_path = output_prefix
        MergeType.__init__(self, output_path)
        self.output_prefix = output_prefix
        self.snp_path = snp_path
        self.pedigree_path = pedigree_path
        self.pedigree_tpv_col=pedigree_tpv_col
        self.gender_path = gender_path
        self.genotype_path = genotype_path
        self.snp_solution_path = snp_solution_path

    def write(self):
        """
        Overrides parent's write method because multiple files are being merged. Writes to output files using the
        numerous generators found below.

        """
        map_path = self.output_prefix + '.map'
        ped_path = self.output_prefix + '.ped'
        kt_path = self.output_prefix+'_pheno.txt'
        with open(map_path, 'w') as map_file:
            map_gen = self.map_generator()
            for entry in map_gen:
                map_file.write(entry)
        with open(ped_path, 'w') as ped_file, open(kt_path, 'w') as kt_file:
            ped_gen = self.ped_generator()
            for entry in ped_gen:
                ped_file.write(entry)
                split_entry = entry.split()
                kt_file.write(split_entry[1] + '\t' + split_entry[5] + '\n')

    def read_generator(self):
        """
        Not used because multiple files are being read throughout the process and at different times depending on
        which file is being written.

        """
        raise NotImplementedError('AlphaSimMerge uses a different read methodology')

    def map_generator(self):
        """
        Parses the snp_file and extracts the needed data to create the MAP file.

        :return: Yields each line in MAP format.
        """
        with open(self.snp_path) as snp_file:
            snp_file.next()
            for line in snp_file:
                split_line = line.split()
                yield '\t'.join([split_line[i] for i in [1, 0, 4, 2]]) + '\n'

    def ped_generator(self):
        """
        Uses the pedigree, gender, and geno generators to extract the needed data to create PED files. AlphaSim does not
        output Family information so the Individual ID is also used as the Family ID. GWAS tools will see this and treat
         every individual separately.

        :return: Yields each line in PED format (FamilyID, IndividualID, PaternalID, MaternalID, Gender, Pheno, Geno)
        """
        if self.snp_solution_path is None:
            ped_gen = self.pedigree_generator()
        else:
            ped_gen = self.snp_solution_generator()
        gend_gen = self.gender_generator()
        geno_gen = self.genotype_generator()
        for ped, gend, geno in zip(ped_gen, gend_gen, geno_gen):
            t = (ped[0], ped[0], ped[1], ped[2], gend[1], ped[3], geno[1])
            yield '\t'.join(list(t))+'\n'

    def pedigree_generator(self):
        """
        Parses the pedigree file and extracts the needed pedigree data for PED files.

        :return: Yields the individual, paternal, and maternal IDs as well as the phenotype value.
        """
        with open(self.pedigree_path) as pedigree_file:
            pedigree_file.next()
            for pedigree_line in pedigree_file:
                split_line = pedigree_line.strip().split()
                yield split_line[1], split_line[2], split_line[3], split_line[self.pedigree_tpv_col]

    def snp_solution_generator(self):
        """
        Does the same as the above pedigree_generator but uses the phenotype value from the SnpSolution file rather
        than from the Pedigree file.

        :return: Yields the individual, paternal, and maternal IDs as well as the phenotype value.
        """
        ped_gen = self.pedigree_generator()
        with open(self.snp_solution_path) as snp_solution_file:
            for snp_solution_line, ped_gen_line in zip(snp_solution_file, ped_gen):
                split_snp_line = snp_solution_line.strip().split()
                yield ped_gen_line[0], ped_gen_line[1], ped_gen_line[2], split_snp_line[1]

    def gender_generator(self):
        """
        Parses the Gender file.

        :return: Yields the individual ID and gender
        """
        with open(self.gender_path) as gender_file:
            gender_file.next()
            for gender_line in gender_file:
                split_line = gender_line.strip().split()
                snp_id = split_line[1]
                gender = split_line[2]
                yield snp_id, gender

    def genotype_generator(self):
        """
        Parses the genotype file and formats this info. Replaces '1' with 'A', '2' with 'B' and leaves 0 as is.

        :return: Yields the individual ID and its formatted genotype
        """
        with open(self.genotype_path) as genotype_file:
            for genotype_line in genotype_file:
                split_line = genotype_line.strip().split(' ', 1)
                id = split_line[0]
                geno = split_line[1].replace('1', 'A').replace('2', 'B')
                yield id, geno
