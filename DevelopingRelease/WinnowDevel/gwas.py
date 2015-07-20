"""
Performs functions necessary for GWAS analysis 
"""

from performetrics import *


def gwasWithBeta(betaColumn, betaTrueFalse, snpTrueFalse, scoreColumn, threshold):
    """
    Performs GWAS analysis with Beta

    :param betaColumn: collected positions
    :param betaTrueFalse: known of the collected positions
    :param snpTrueFalse: true/false data set
    :param scoreColumn: score data set
    :param threshold: significant threshold
    :return: an array of functions and an array of those functions' results
    """
    return ["rmse", "mae", "mattcorr", "auc", "TruePositives", "FalsePositives", "TrueNegatives", "FalseNegatives",
            "TruePosRate", "FalsePosRate", "error", "accuracy" "sens", "spec", "precision", "fdr", "youden"], \
           [rmse(betaColumn, betaTrueFalse), mae(betaColumn, betaTrueFalse), mattcorr(snpTrueFalse, threshold, scoreColumn), 
           auc(snpTrueFalse, scoreColumn), tp(snpTrueFalse, threshold, scoreColumn),fp(snpTrueFalse, threshold, scoreColumn), tn(snpTrueFalse, threshold, scoreColumn), fn(snpTrueFalse,threshold,scoreColumn),
            tpr(snpTrueFalse, threshold, scoreColumn), fpr(snpTrueFalse, threshold,scoreColumn), error(snpTrueFalse, threshold, scoreColumn), accuracy(snpTrueFalse, threshold, scoreColumn),
            sens(snpTrueFalse, threshold, scoreColumn),spec(snpTrueFalse, threshold, scoreColumn), precision(snpTrueFalse, threshold, scoreColumn), fdr(snpTrueFalse, threshold, scoreColumn),
            youden(snpTrueFalse, threshold, scoreColumn)]


def gwasWithoutBeta(snpTrueFalse, scoreColumn, threshold):
    """
    Performs GWAS analysis without Beta

    :param snpTrueFalse: true/false data set
    :param scoreColumn: score data set
    :param threshold: significant threshold
    :return: an array of functions and an array of those functions' results
    """
    return ["mattcorr", "auc", "TruePositives", "FalsePositives", "TrueNegatives", "FalseNegatives", "TruePosRate", "FalsePosRate",
            "error", "accuracy", "sens", "spec", "precision", "fdr", "youden"], [mattcorr(snpTrueFalse, threshold, scoreColumn),
                                                              auc(snpTrueFalse, scoreColumn),
                                                              tp(snpTrueFalse, threshold, scoreColumn),
                                                              fp(snpTrueFalse, threshold, scoreColumn),
                                                              tn(snpTrueFalse, threshold, scoreColumn),
                                                              fn(snpTrueFalse, threshold, scoreColumn),
                                                              tpr(snpTrueFalse, threshold, scoreColumn),
                                                              fpr(snpTrueFalse, threshold, scoreColumn),
                                                              error(snpTrueFalse, threshold, scoreColumn),
                                                              accuracy(snpTrueFalse, threshold, scoreColumn),
                                                              sens(snpTrueFalse, threshold, scoreColumn),
                                                              spec(snpTrueFalse, threshold, scoreColumn),
                                                              precision(snpTrueFalse, threshold, scoreColumn),
                                                              fdr(snpTrueFalse, threshold, scoreColumn),
                                                              youden(snpTrueFalse, threshold, scoreColumn)]

