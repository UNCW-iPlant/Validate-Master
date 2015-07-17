def fdr_bh(score_col):
    """
    Benjamini-Hochberg FDR Method

    :param score_col: unadjusted list of p-values
    :return: list of adjusted p-values using the Benjamini-Hochberg FDR method
    """
    ordered_scores = list()
    score_col_copy = list(score_col)
    new_pval = [None] * len(score_col)
    for each in score_col_copy:
        ordered_scores.append((each, score_col_copy.index(each)))
        score_col_copy[score_col_copy.index(each)] = None
    ordered_scores.sort()
    ordered_scores.reverse()
    adjusted = len(ordered_scores)*ordered_scores[0][0]/len(ordered_scores)
    for each in ordered_scores:
        val = min(adjusted, float(len(ordered_scores)) * float(each[0]) /
                  float(len(ordered_scores) - ordered_scores.index(each)))
        new_pval[each[1]] = val
        adjusted = val
    return new_pval


if __name__ == '__main__':
    # Example from "Notes on Bonferroni-Holm method"
    t1 = [0.012, 0.033, 0.212, 0.9, 0.98, 0.001, 0.999, 0.0003, 0.00001]
    print fdr_bh(t1)

    # Example from "Nov 12 Lecture"
    t2 = [0.010, 0.013, 0.014, 0.190, 0.350, 0.500, 0.630, 0.670, 0.750, 0.810]
    print fdr_bh(t2)
