from MergeType import MergeType
import MergeTypes.BayesRMerge

b = MergeTypes.BayesRMerge.BayesRMerge('/Users/SamBuck/Desktop/merged',
                                       '/Users/SamBuck/Desktop/simdata.bim',
                                       '/Users/SamBuck/Desktop/simout.param')

b.write()
