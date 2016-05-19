from MergeType import MergeType


class BayesRMerge(MergeType):
    def __init__(self, output_prefix, bim_path, param_path):
        MergeType.__init__(self, output_prefix + '.bim')
        self.bim_path = bim_path
        self.param_path = param_path

    def read_generator(self):
        with open(self.bim_path) as bim_file, open(self.param_path) as param_file:
            split_param_line = param_file.readline().split()
            header = '\t'.join([str(p) for p in split_param_line])
            header = 'SNP\t' + header
            yield header + '\n'
            for bim_line, param_line in zip(bim_file, param_file):
                split_param_line = param_line.split()
                yield str(bim_line.split()[1]) + '\t' + '\t'.join([str(p) for p in split_param_line])+'\n'
