"""
Performs functions necessary for GWAS analysis 
"""

from performetrics import *


def gwasWithBeta(betaColumn, betaTrueFalse, snpTrueFalse, scoreColumn, threshold):
    """
    Performs GWAS analysis with beta/effect size

    :param betaColumn: collected positions
    :param betaTrueFalse: known of the collected positions
    :param snpTrueFalse: true/false data set
    :param scoreColumn: score data set
    :param threshold: significant threshold
    :return: an array of functions and an array of those functions' results
    """
    return ["rmse", "mae", "mattcorr", "auc", "tp", "fp", "tn", "fn",
            "tpr", "fpr", "error", "accuracy", "sens", "spec", "precision", "fdr", "youden"], \
           [rmse(betaColumn, betaTrueFalse), mae(betaColumn, betaTrueFalse),
            mattcorr(snpTrueFalse, threshold, scoreColumn),
            auc(snpTrueFalse, scoreColumn), tp(snpTrueFalse, threshold, scoreColumn),
            fp(snpTrueFalse, threshold, scoreColumn), tn(snpTrueFalse, threshold, scoreColumn),
            fn(snpTrueFalse, threshold, scoreColumn),
            tpr(snpTrueFalse, threshold, scoreColumn), fpr(snpTrueFalse, threshold, scoreColumn),
            error(snpTrueFalse, threshold, scoreColumn), accuracy(snpTrueFalse, threshold, scoreColumn),
            sens(snpTrueFalse, threshold, scoreColumn), spec(snpTrueFalse, threshold, scoreColumn),
            precision(snpTrueFalse, threshold, scoreColumn), fdr(snpTrueFalse, threshold, scoreColumn),
            youden(snpTrueFalse, threshold, scoreColumn)]


def gwasBetaCovar(betaColumn, betaTrueFalse, snpTrueFalse, scoreColumn, threshold, covar):
    """
    Performs GWAS analysis with beta/effect size and covariates

    :param betaColumn: collected positions
    :param betaTrueFalse: known of the collected positions
    :param snpTrueFalse: true/false data set
    :param scoreColumn: score data set
    :param threshold: significant threshold
    :param covar: the covariate column from data set
    :return: an array of functions and an array of those functions' results
    """
    return ["rmse", "mae", "mattcorr", "auc", "tp", "fp", "tn", "fn",
            "tpr", "fpr", "error", "accuracy", "sens", "spec", "precision", "fdr", "youden", "avgcovarweight"], \
           [rmse(betaColumn, betaTrueFalse), mae(betaColumn, betaTrueFalse),
            mattcorr(snpTrueFalse, threshold, scoreColumn),
            auc(snpTrueFalse, scoreColumn), tp(snpTrueFalse, threshold, scoreColumn),
            fp(snpTrueFalse, threshold, scoreColumn), tn(snpTrueFalse, threshold, scoreColumn),
            fn(snpTrueFalse, threshold, scoreColumn),
            tpr(snpTrueFalse, threshold, scoreColumn), fpr(snpTrueFalse, threshold, scoreColumn),
            error(snpTrueFalse, threshold, scoreColumn), accuracy(snpTrueFalse, threshold, scoreColumn),
            sens(snpTrueFalse, threshold, scoreColumn), spec(snpTrueFalse, threshold, scoreColumn),
            precision(snpTrueFalse, threshold, scoreColumn), fdr(snpTrueFalse, threshold, scoreColumn),
            youden(snpTrueFalse, threshold, scoreColumn),
            avgcovarweight(covar)]


def gwasWithoutBeta(snpTrueFalse, scoreColumn, threshold):
    """
    Performs GWAS analysis without beta/effect size

    :param snpTrueFalse: true/false data set
    :param scoreColumn: score data set
    :param threshold: significant threshold
    :return: an array of functions and an array of those functions' results
    """
    return ["mattcorr", "auc", "tp", "fp", "tn", "fn", "tpr",
            "fpr", "error", "accuracy", "sens", "spec", "precision", "fdr", "youden"], [
               mattcorr(snpTrueFalse, threshold, scoreColumn),
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


def gwasNoBetaCovar(snpTrueFalse, scoreColumn, threshold, covar):
    """
    Performs GWAS analysis without beta/effect size but with covariates

    :param snpTrueFalse: true/false data set
    :param scoreColumn: score data set
    :param threshold: significant threshold
    :param covar: covariate column from data set
    :return: an array of functions and an array of those functions' results
    """
    return ["mattcorr", "auc", "tp", "fp", "tn", "fn", "tpr",
            "fpr", "error", "accuracy", "sens", "spec", "precision", "fdr", "youden", "avgcovarweight"], [
               mattcorr(snpTrueFalse, threshold, scoreColumn),
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
               youden(snpTrueFalse, threshold, scoreColumn),
               avgcovarweight(covar)]
