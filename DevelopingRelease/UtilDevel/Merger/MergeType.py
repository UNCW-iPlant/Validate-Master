class MergeType:
    """
    Parent class for other MergeTypes. Handles the writing portion of the merge process in most cases. Children classes
    must implement the read generator at a minimum.

    """
    def __init__(self, output_path):
        """

        :param output_path: Path to save the output file to
        """
        self.output_path = output_path

    def read_generator(self):
        """
        Generator to use with the write function. Children classes must implement this.

        :return: generator that yields the lines to write
        """
        raise NotImplementedError('The read method must be implemented in the subclass')

    def write(self):
        """
        Writes the output file, line-by-line, using the read generator

        """
        gen = self.read_generator()
        with open(self.output_path, 'w') as output_file:
            for line in gen:
                output_file.write(line)
