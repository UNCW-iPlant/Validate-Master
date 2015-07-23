def fdr_bh(score_col):
    """
    Benjamini-Hochberg FDR Method

    :param score_col: unadjusted list of p-values
    :return: list of adjusted p-values using the Benjamini-Hochberg FDR method
    """
    # List for p-vals in order from largest to smallest
    ordered_scores = list()
    # Copy of list of p-vals so the original is not modified
    score_col_copy = list(score_col)
    # List of adjusted p-vals in original order to be returned
    new_pval = [None] * len(score_col)
    # Copies the original list of p-vals into score_col_copy as a tuple (p, index(p)) so we can save the original order
    for each in score_col_copy:
        ordered_scores.append((each, score_col_copy.index(each)))
        # Removes each p-val from the copy list to ensure that indexes are accurate in case of duplicate p-cals
        score_col_copy[score_col_copy.index(each)] = None
    # Sorts p-vals smallest to largest, then reverses so they are ordered largest to smallest
    ordered_scores.sort()
    ordered_scores.reverse()
    # Solves for the adjusted p-val of the first (largest) original p-val
    adjusted = len(ordered_scores)*ordered_scores[0][0]/len(ordered_scores)
    # Iterates through all ordered p-vals, sets val to the minimum of the previous adjustment and current adjustment
    for each in ordered_scores:
        val = min(adjusted, float(len(ordered_scores)) * float(each[0]) /
                  float(len(ordered_scores) - ordered_scores.index(each)))
        # Sets the index of new_pval(from the tuple in ordered_scores) to the adjusted p-val
        new_pval[each[1]] = val
        # Updates the adjusted value so the minimum function will work on the next iteration
        adjusted = val
    # Returns the list of adjusted p-vals in the original order
    return new_pval


if __name__ == '__main__':
    # Example from "Notes on Bonferroni-Holm method"
    t1 = [0.012, 0.033, 0.212, 0.9, 0.98, 0.001, 0.999, 0.0003, 0.00001]
    print fdr_bh(t1)

    # Example from "Nov 12 Lecture"
    t2 = [0.010, 0.013, 0.014, 0.190, 0.350, 0.500, 0.630, 0.670, 0.750, 0.810]
    print fdr_bh(t2)
