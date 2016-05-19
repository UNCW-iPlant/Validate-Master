from MergeType import MergeType
import pandas as pd
from os import path, chdir, listdir


class LauncherMerge(MergeType):
    def __init__(self, output_prefix, folder_path):
        MergeType.__init__(self, output_prefix + '.txt')
        self.folder_path = folder_path

    def read_generator(self):
        chdir(self.folder_path)
        file_list = listdir(path.abspath(self.folder_path))
        initial_data = pd.read_table(file_list[0], sep='\t', header=0)
        column_names = initial_data.columns.values.tolist()
        yield '\t'.join(column_names) + '\n'
        for name in file_list:
            data = pd.read_table(name, sep='\t', header=0)
            values = map(str, data.values.tolist()[0])
            yield '\t'.join(values)+'\n'