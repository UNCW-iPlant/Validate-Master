class MergeType:
    def __init__(self, output_path):
        self.output_path = output_path

    def read_generator(self):
        raise NotImplementedError('The read method must be implemented in the subclass')

    def write(self):
        gen = self.read_generator()
        with open(self.output_path, 'w') as output_file:
            for line in gen:
                output_file.write(line)
