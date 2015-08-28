"""
Performs functions necessary for GWAS analysis 
"""


from performetrics import *


def gwasWithBeta(betaColumn, betaTrueFalse, snpTrueFalse, scoreColumn, threshold):
	return ["rmse", "mae", "r", "r2", "auc", "tp", "fp", "tn", "fn", "tpr", "fpr", "error", "sens", "spec", "precision", "youden"], [rmse(betaColumn, betaTrueFalse), mae(betaColumn, betaTrueFalse), r(betaColumn, betaTrueFalse), r2(betaColumn, betaTrueFalse),auc(snpTrueFalse, scoreColumn), tp(snpTrueFalse, threshold, scoreColumn), fp(snpTrueFalse, threshold, scoreColumn), tn(snpTrueFalse, threshold, scoreColumn), fn(snpTrueFalse, threshold, scoreColumn), tpr(snpTrueFalse, threshold, scoreColumn), fpr(snpTrueFalse, threshold, scoreColumn), error(snpTrueFalse, threshold, scoreColumn), sens(snpTrueFalse, threshold, scoreColumn), spec(snpTrueFalse, threshold, scoreColumn), precision(snpTrueFalse, threshold, scoreColumn), youden(snpTrueFalse, threshold, scoreColumn)]

def gwasWithoutBeta(snpTrueFalse, scoreColumn, threshold):
	return ["auc", "tp", "fp", "tn", "fn", "tpr", "fpr", "error", "sens", "spec", "precision", "youden"], [auc(snpTrueFalse, scoreColumn), tp(snpTrueFalse, threshold, scoreColumn), fp(snpTrueFalse, threshold, scoreColumn), tn(snpTrueFalse, threshold, scoreColumn), fn(snpTrueFalse, threshold, scoreColumn),tpr(snpTrueFalse, threshold, scoreColumn), fpr(snpTrueFalse, threshold, scoreColumn), error(snpTrueFalse, threshold, scoreColumn), sens(snpTrueFalse, threshold, scoreColumn), spec(snpTrueFalse, threshold, scoreColumn), precision(snpTrueFalse, threshold, scoreColumn), youden(snpTrueFalse, threshold, scoreColumn)]
