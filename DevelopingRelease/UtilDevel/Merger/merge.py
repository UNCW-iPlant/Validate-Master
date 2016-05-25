from MergeTypes.BayesRMerge import BayesRMerge
from MergeTypes.LauncherMerge import LauncherMerge
from MergeTypes.AlphaSimMerge import AlphaSimMerge
from commandline import CommandLine


class Merge:
    def __init__(self, args):
        self.output_path = args.output
        if args.mode in ['bayesr', 'alphasim', 'launcher']:
            if args.mode == 'bayesr':
                self.merger = BayesRMerge(self.output_path, args.bim, args.param)
            elif args.mode == 'alphasim':
                self.merger = AlphaSimMerge(self.output_path, args.snp, args.pedigree, args.gender, args.geno, args.sol,
                                            args.col if args.col is not None else 9)
            elif args.mode == 'launcher':
                self.merger = LauncherMerge(self.output_path, args.folder)
            self.merger.write()
        else:
            print args.mode, 'not supported'


if __name__ == '__main__':
    command_line = CommandLine()
    merger = Merge(command_line.args)
