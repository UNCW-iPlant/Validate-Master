"""
Class for whitespace and comma delimited data 
"""


class Data:

	def __init__(self, filelocation, seper, skiprow=False):
		self.filelocation = filelocation
		self.seper = seper
		if skiprow is False:
			if self.seper == "whitespace":
				self.data, self.n = self.whitespace()
				self.header = self.data[0]
				self.data = {thisKey : self.data[thisKey] for thisKey in range(1, self.n)}
			elif self.seper == "comma":
				self.data, self.n = self.comma()
				self.header = self.data[0]
				self.data = {thisKey : self.data[thisKey] for thisKey in range(1, self.n)}
		else:
			if self.seper == "whitespace":
				self.data, self.n = self.whitespace()
			elif self.seper == "comma":
				self.data, self.n = self.comma()
        """    The following two functions establish the possible options for delimiters: whitespace or comma"""
	def whitespace(self):
	    f = open(self.filelocation, "rb")
	    temp = list()
	    for line in f.readlines():
	        temp.append(line.replace("\n","").split(" "))
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

	def comma(self):
	    f = open(self.filelocation, "rb")
	    temp = list()
	    for line in f.readlines():
	        temp.append(line.replace("\n","").split(","))
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