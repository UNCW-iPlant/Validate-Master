from MergeType import MergeType
import pandas as pd
from os import path, chdir, listdir


class LauncherMerge(MergeType):
    """
    MergeType children class to handle outputs from Launcher.

    """
    def __init__(self, output_prefix, folder_path):
        """
        Initializes the LauncherMerge object (to handle reading) and its parent class (to handle writing).

        :param output_prefix: Prefix for output file. '.txt' is added if is not already specified
        :param folder_path: Folder containing input files to merge together
        """
        output_path = output_prefix if output_prefix.endswith('.txt') else output_prefix + '.txt'
        MergeType.__init__(self, output_path)
        self.folder_path = folder_path

    def read_generator(self):
        """
        Iterates over the files, and their lines, in the specified folder.

        :return: Yields all lines in all files
        """
        chdir(self.folder_path)
        file_list = listdir(path.abspath(self.folder_path))
        initial_data = pd.read_table(file_list[0], sep='\t', header=0)
        column_names = initial_data.columns.values.tolist()
        yield '\t'.join(column_names) + '\n'
        for name in file_list:
            data = pd.read_table(name, sep='\t', header=0)
            values = map(str, data.values.tolist()[0])
            yield '\t'.join(values) + '\n'
