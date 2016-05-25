from MergeType import MergeType


class BayesRMerge(MergeType):
    """
    MergeType children class to handle outputs from using BayesR.

    """
    def __init__(self, output_prefix, bim_path, param_path):
        """
        Initializes the BayesRMerge object (to handle reading) and its parent class (to handle writing).

        :param output_prefix: Prefix for the output file. '.bim' is added if it is not already specified
        :param bim_path: BIM file path (BayesR input file)
        :param param_path: PARAM file path (BayesR output file)
        """
        output_path = output_prefix if output_prefix.endswith('.bim') else output_prefix + '.bim'
        MergeType.__init__(self, output_path)
        self.bim_path = bim_path
        self.param_path = param_path

    def read_generator(self):
        """
        Iterates over the BIM and PARAM files synchronously. Combines the data within the PARAM file with the SNP ID
        from the BIM file so that it can be used as input to Winnow.

        :return: Yields the SNP id and the PARAM data associated with that ID
        """
        with open(self.bim_path) as bim_file, open(self.param_path) as param_file:
            split_param_line = param_file.readline().split()
            header = '\t'.join([str(p) for p in split_param_line])
            header = 'SNP\t' + header
            yield header + '\n'
            for bim_line, param_line in zip(bim_file, param_file):
                split_param_line = param_line.split()
                yield str(bim_line.split()[1]) + '\t' + '\t'.join([str(p) for p in split_param_line])+'\n'
