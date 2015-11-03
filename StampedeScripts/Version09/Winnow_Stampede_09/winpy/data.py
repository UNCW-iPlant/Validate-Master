"""
Class for whitespace, comma, and tab delimited data 
"""
import sys


class Data:
    def __init__(self, filelocation, seper, skiprow=False):
        self.filelocation = filelocation
        self.seper = seper
        if skiprow is False:
            self.data, self.n = self.split_data()
            self.header = self.data[0]
            self.data = {thisKey: self.data[thisKey] for thisKey in range(1, self.n)}
        else:
            self.data, self.n = self.split_data()

    def split_data(self):
        """
        Produces a dictionary with data that used whitespace as a delimiter

        :return: a dictionary with the parsed data and the amount of data
        """
        if self.seper == "whitespace":
            seperstring = " "
        elif self.seper == "comma":
            seperstring = ","
        elif self.seper == "tab":
            seperstring = "\t"
        else:
            print self.seper + "is not a supported delimiter. Only whitespace, comma, and tab are accepted."
            sys.exit()
        f = open(self.filelocation, "rb")
        temp = list()
        for line in f.readlines():
            temp.append(line.replace("\n", "").split(seperstring))
        f.close()
        data = dict()
        count = 0
        for row in temp:
            data[count] = list()
            for each in row:
                if each is not "":
                    data[count].append(each)
            count += 1
        return data, count
