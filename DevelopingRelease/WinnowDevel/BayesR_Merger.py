import argparse


class Merge:
    def __init__(self, args):
        self.bim_source = args.bim
        self.param_source = args.param
        self.output_name = args.output
        self.line_generator = self.parse_lines()
        self.write_output()

    def parse_lines(self):
        with open(self.bim_source) as bim_file, open(self.param_source) as param_file:
            header = '\t'.join([str(p) for p in param_file.readline().split()])
            header = 'SNP\t' + header
            yield header + '\n'
            for bim_line, param_line in zip(bim_file, param_file):
                yield str(bim_line.split()[1]) + '\t' + '\t'.join([str(p) for p in param_line.split()]) + '\n'

    def write_output(self):
        with open(self.output_name, 'w') as output_file:
            for line in self.line_generator:
                output_file.write(line)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bim', type=str, required=True, help='BIM file used in BayesR')
    parser.add_argument('-p', '--param', type=str, required=True,  help='.param output file from BayesR')
    parser.add_argument('-o', '--output', type=str, required=False, default='merged_output.txt',
                        help='Output file prefix')
    args = parser.parse_args()
    return args


def main():
    merger = Merge(parse_arguments())

if __name__ == '__main__':
    main()
