from MergeType import MergeType


class AlphaSimMerge(MergeType):
    def __init__(self, output_prefix, snp_path):
        MergeType.__init__(self, output_prefix)
        self.snp_path = snp_path

    def read_generator(self):
        with open(self.snp_path) as snp_file:
            snp_file.next()
            for line in snp_file:
                split_line = line.split()
                yield '\t'.join([split_line[i] for i in [1, 0, 4, 2]]) + '\n'
