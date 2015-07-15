"""
Performance measures for testing applications in Winnow
"""

import numpy as np
import pandas as pd
from scipy import stats


def rmse(betaColumn, betaTrueFalse):
	betaColumn = np.array(betaColumn)
	betaTrueFalse = np.array(betaTrueFalse)
	return np.mean(np.square(np.subtract(betaColumn, betaTrueFalse)))
"""    Returns the root mean squared error given the known truth and effects
>>>betaColumn=np.array([1,2,3,4,5,6])
>>>betaTF=np.array([1,0,1,1,0,0])
>>>rmse(betaCol, betaTF)
13.0
"""

def mae(betaColumn, betaTrueFalse):
	betaColumn = np.array(betaColumn)
	betaTrueFalse = np.array(betaTrueFalse)
	return np.mean(np.absolute(np.subtract(betaColumn, betaTrueFalse)))
"""    Returns the mean absolute error of the dataset
>>>betaColumn=np.array([1,2,3,4,5,6])
>>>betaTF=np.array([1,0,1,1,0,0])
>>>mae(betaCol, betaTF)
3.0
"""
def r(betaColumn, betaTrueFalse):
	betaColumn = np.array(betaColumn)
	betaTrueFalse = np.array(betaTrueFalse)
	return stats.stats.pearsonr(betaColumn, betaTrueFalse)[0]
"""    Returns the correlation coefficient between the known-truth effects
and the detected true/false effects.
>>>x=[1,2,3,4,5]
>>>y=[5,9,10,12,13]
>>>r(x,y)
0.96457886
"""
def r2(betaColumn, betaTrueFalse):
	betaColumn = np.array(betaColumn)
	betaTrueFalse = np.array(betaTrueFalse)
	return np.square(stats.stats.pearsonr(betaColumn, betaTrueFalse)[0])
"""    Produces the coefficient of determination (AKA 
the correlation coefficient squared); gives the percentage of variation accounted for 
by the relationship between the given variables
>>>x=[3,4,5,6,7]
>>>y=[9,10,13,12,18]
>>>r2(x,y)
0.81300813
"""

def auc(snpTrueFalse, scoreColumn):
	scoreColumn = np.array(scoreColumn)
	snpTrueFalse = np.array(snpTrueFalse)
	x1 = scoreColumn[snpTrueFalse == True]
	n1 = x1.size
	x2 = scoreColumn[snpTrueFalse == False]
	n2 = x2.size
	r = stats.rankdata(np.hstack((x1,x2)))
	auc = (np.sum(r[0:n1]) - n1 * (n1+1)/2) / (n1 * n2)
	return 1 - auc
"""    Returns the area under the reciever-operator curve for binary classification (i.e. true/false on whether
a SNP was part of the known-truth list or not)
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
>>>auc(snpTF,score)
0.56944444
"""
def tp(snpTrueFalse, threshold, scoreColumn):
	testColumn = list()
	for each in scoreColumn:
		if float(each) < threshold:
			testColumn.append(True)
		else:
			testColumn.append(False)
	count = 0
	truePositives = 0
	for each in testColumn:
		if each is True and snpTrueFalse[count] is True:
			truePositives += 1
		count += 1
	return truePositives
"""    Returns the total number of SNPs correctly identified as significant from the analysis
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
tp(snpTF, threshold, score)
4
"""
def fp(snpTrueFalse, threshold, scoreColumn):
	testColumn = list()
	for each in scoreColumn:
		if float(each) < threshold:
			testColumn.append(True)
		else:
			testColumn.append(False)
	count = 0
	falsePositives = 0
	for each in testColumn:
		if each is True and snpTrueFalse[count] is False:
			falsePositives += 1
		count += 1
	return falsePositives
"""    Returns the number of SNPs incorrectly identified as significant
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
2
"""
def tn(snpTrueFalse, threshold, scoreColumn):
	testColumn = list()
	for each in scoreColumn:
		if float(each) < threshold:
			testColumn.append(True)
		else:
			testColumn.append(False)
	count = 0
	trueNegatives = 0
	for each in testColumn:
		if each is False and snpTrueFalse[count] is False:
			trueNegatives += 1
		count += 1
	return trueNegatives
"""    Returns the number of SNPs correctly identified as not significant
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
3
"""
def fn(snpTrueFalse, threshold, scoreColumn):
	testColumn = list()
	for each in scoreColumn:
		if float(each) < threshold:
			testColumn.append(True)
		else:
			testColumn.append(False)
	count = 0
	falseNegatives = 0
	for each in testColumn:
		if each is False and snpTrueFalse[count] is True:
			falseNegatives += 1
		count += 1
	return falseNegatives
"""    Returns the number of SNPs incorrectly identified as not significant
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
3
"""

def tpr(snpTrueFalse, threshold, scoreColumn):
	truePositives = tp(snpTrueFalse, threshold, scoreColumn)
	count = 0.0
	for each in snpTrueFalse:
		if each is True:
			count += 1.0
	return float(truePositives/count)
"""    The proportion of true positives identified from the entire dataset
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
0.66666667
"""

def fpr(snpTrueFalse, threshold, scoreColumn):
	falsePositives = fp(snpTrueFalse, threshold, scoreColumn)
	count = 0.0
	for each in snpTrueFalse:
		if each is False:
			count += 1.0
	return float(falsePositives/count)
"""    Returns the proportion of false positives identified from the dataset
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
0.33333333
"""
def error(snpTrueFalse, threshold, scoreColumn):
	truePositives = float(tp(snpTrueFalse, threshold, scoreColumn))
	falsePositives = float(fp(snpTrueFalse, threshold, scoreColumn))
	trueNegatives = float(tn(snpTrueFalse, threshold, scoreColumn))
	falseNegatives = float(fn(snpTrueFalse, threshold, scoreColumn))
	return (falseNegatives + falsePositives) / (truePositives + trueNegatives + falsePositives + falseNegatives)
"""    Returns the error value of the analysis (NOT standard error!) defined as the total false identifications,
positive or negative, by the total number identified
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
>>>error(snpTF,threshold,score)
0.41666667
"""

def sens(snpTrueFalse, threshold, scoreColumn):
	truePositives = float(tp(snpTrueFalse, threshold, scoreColumn))
	falseNegatives = float(fn(snpTrueFalse, threshold, scoreColumn))
	return truePositives / (truePositives + falseNegatives)
"""    Returns the sensitivty value of the analysis;
defined as the number of correctly identified positives divided by the total number of known-truth positives
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
>>>sens(snpTF, threshold, score)
0.57142857
"""

def spec(snpTrueFalse, threshold, scoreColumn):
	trueNegatives = float(tn(snpTrueFalse, threshold, scoreColumn))
	falsePositives = float(fp(snpTrueFalse, threshold, scoreColumn))
	return trueNegatives / (trueNegatives + falsePositives)
"""    Returns the specificity value; defined as the number of correctly identified negatives divided by the
total number of known-truth negatives
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
0.6
"""
def precision(snpTrueFalse, threshold, scoreColumn):
	truePositives = float(tp(snpTrueFalse, threshold, scoreColumn))
	falsePositives = float(fp(snpTrueFalse, threshold, scoreColumn))
	return truePositives / (truePositives + falsePositives)
"""    Returns the precision; defined as the number of correctly identified positives divided by the total identified positives
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold=0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
0.66666667
"""
def youden(snpTrueFalse, threshold, scoreColumn):
	sensitivity = float(sens(snpTrueFalse, threshold, scoreColumn))
	specificity = float(spec(snpTrueFalse, threshold, scoreColumn))
	return sensitivity + specificity - 1.0
"""Returns the Youden statistic for the data
>>>snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
>>>threshold = 0.05
>>>score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
>>>youden(snpTF,threshold,score)
0.17142857
"""
if __name__ == "__main__":
    import doctest
    doctest.testmod()