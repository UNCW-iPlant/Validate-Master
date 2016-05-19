from MergeTypes.BayesRMerge import BayesRMerge
from MergeTypes.AlphaSimMerge import AlphaSimMerge
from MergeTypes import LauncherMerge
from commandline import CommandLine


class Merge:
    def __init__(self, args):
        self.output_path = args.output
        if args.mode in ['bayesr', 'alphasim', 'launcher']:
            if args.mode == 'bayesr':
                self.merger = BayesRMerge(self.output_path, args.bim, args.param)
            elif args.mode == 'alphasim':
                self.snp_path = args.snp
                self.merger = AlphaSimMerge(self.output_path, args.snp)
            elif args.mode == 'launcher':
                self.merger = LauncherMerge(self.output_path, args.folder)
            self.merger.write()
        else:
            print args.mode, 'not supported'


if __name__ == '__main__':
    command_line = CommandLine()
    merger = Merge(command_line.args)
