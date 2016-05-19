import argparse


class Converter:
    def __init__(self, args):
        self.snp_information_source = args.snp
        self.output_name = args.output

    def parse_snp_lines(self):
        with open(self.snp_information_source) as snp_file:
            snp_file.next()
            for line in snp_file:
                split_line = line.split()
                yield '\t'.join([split_line[i] for i in [1, 0, 4, 2]])+'\n'

    def write_output(self):
        self.write_output_map()

    def write_output_map(self):
        with open(self.output_name+'.map', 'w') as output_file:
            for line in self.parse_snp_lines():
                output_file.write(line)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--snp', type=str, required=True, help='SNP information file from AlphaSim')
    parser.add_argument('-o', '--output', type=str, required=False, help='Output file name prefix', default='output')
    return parser.parse_args()


def main():
    convert = Converter(parse_arguments())
    convert.write_output()

if __name__ == '__main__':
    main()
