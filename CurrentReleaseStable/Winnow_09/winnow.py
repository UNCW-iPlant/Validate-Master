# WinPy -- formerly Validate.R in Python
# Author: Dustin Landers
# Contact: (770 289-8830) :: dustin.landers@gmail.com


""" Dependencies """
from commandline import initializeGraphics, checkArgs
from fileimport import getList, loadKT, loadFile, trueFalse, writeCSV, writeSettings
from checkhidden import checkList
from gwas import gwasWithBeta, gwasWithoutBeta, gwasBetaCovar, gwasNoBetaCovar
from statsmodels.sandbox.stats.multicomp import multipletests

class Winnow:
    def __init__(self, args):
        """
        Creates a new instance of a Winnow object using the runtime arguments.

        :param args: dictionary of arguments
        :return: a new Winnow object with snp_true_false and beta_true_false initialized as empty lists
        """
        self.args_dict = args
        self.snp_true_false = list()
        self.beta_true_false = list()

    def load_kt(self):
        """
        Loads the known truth file by type; currently only OTE is supported.

        """
        if self.args_dict['kt_type'] == 'OTE':
            self.load_ote()
        else:  # pragma: no cover
            print 'Currently only OTE is supported'

    def load_ote(self):
        """
        Loads only truth and effect type known truth file.

        :return: sets the instance list variables snp_true_false and beta_true_false with data from the known truth file
        given at runtime, separated by the given delimiter
        """
        app_output_list = checkList(getList(self.args_dict['folder']))
        kt_file = loadKT(self.args_dict['truth'], self.args_dict['kt_type_separ'])
        acquired_data = loadFile(self.args_dict['folder'], app_output_list[0], self.args_dict['separ'])
        snp_column = data_to_list(acquired_data, 1, acquired_data.header.index(self.args_dict['snp']))
        kt_snps = data_to_list(kt_file, 1, 0)
        kt_betas = data_to_list(kt_file, 1, 1)
        for each in snp_column:
            self.snp_true_false.append(trueFalse(each, kt_snps))
        self.load_ote_betas(snp_column, kt_snps, kt_betas)

    def load_ote_betas(self, snp_col, kt_snp, kt_beta):
        """
        Loads beta values as floats from the only truth and effect type known truth file if the beta argument is passed
        at runtime.

        :param snp_col: the column number that the SNPs are listed in
        :param kt_snp: list of known truth SNPs
        :param kt_beta: list of known truth betas
        :return: Stores the float representation of betas in the instance variable beta_true_false
        """
        if self.args_dict['beta'] is not None:
            count = 0
            for each in self.snp_true_false:
                if each:
                    current = snp_col[count]
                    match = kt_snp.index(current)
                    this_beta = kt_beta[match]
                    self.beta_true_false.append(float(this_beta))
                else:
                    self.beta_true_false.append(float(0))
                count += 1

    def load_data(self, data_file):
        """
        Returns a list of score and beta values from a file that is given as the parameter

        :param data_file: file containing score and, if selected, beta values
        :return: a list of scores and, if selected, a list of betas in the form of a tuple
        """
        acquired_data = loadFile(self.args_dict['folder'], data_file, self.args_dict['separ'])
        score_column = data_to_list(acquired_data, 1, acquired_data.header.index(self.args_dict['score']), True)
        snp_column = data_to_list(acquired_data, 1, acquired_data.header.index(self.args_dict['snp']))
        adjusted_score_column = self.adjust_score(score_column)
        self.save_snp_score(snp_column, score_column, adjusted_score_column)
        if self.args_dict['beta'] is not None:
            beta_column = data_to_list(acquired_data, 1, acquired_data.header.index(self.args_dict['beta']), True)
            if self.args_dict['covar'] is not None:
                covar_column = data_to_list(acquired_data, 1, acquired_data.header.index(self.args_dict['covar']), True)
                return adjusted_score_column, beta_column, covar_column
            else:
                return adjusted_score_column, beta_column
        else:
            if self.args_dict['covar'] is not None:
                covar_column = data_to_list(acquired_data, 1, acquired_data.header.index(self.args_dict['covar']), True)
                return adjusted_score_column, covar_column
            else:
                return adjusted_score_column

    def do_analysis(self):
        """
        Generator that performs the analysis. Uses data from the files within the folder that was given at runtime.
        Currently, only GWAS is supported.

        :return: loads all files from the folder given at runtime, parses data with the load_data function, returns the
        results of the analysis with this data
        """
        app_output_list = sorted(checkList(getList(self.args_dict['folder'])))
        for each in app_output_list:
            if self.args_dict['beta'] is not None:
                if self.args_dict['covar'] is not None:
                    score_column, beta_column, covar_column = self.load_data(each)
                else:
                    score_column, beta_column = self.load_data(each)
                    covar_column = None
            else:
                if self.args_dict['covar'] is not None:
                    score_column, covar_column = self.load_data(each)
                    beta_column = None
                else:
                    score_column = self.load_data(each)
                    beta_column = None
                    covar_column = None
            if self.args_dict['analysis'] == 'GWAS':
                yield self.do_gwas(score_column, beta_column, covar_column)
            else:
                # Add other analysis methods here
                print 'Currently, only GWAS is supported.'

    def write_to_file(self, gen):  # pragma: no cover
        """
        Writes the results of the analysis to the file given at runtime. Gets the resulting data from a generator.

        :param gen: generator that yields data to be written
        :return: writes the data to the given file
        """
        first_for_header = True
        for each in gen:
            if not first_for_header:
                writeCSV(self.args_dict['filename'], each, 'a', '\t')
            else:
                writeCSV(self.args_dict['filename'], each, 'wb', '\t')
                first_for_header = False
        gen.close()

    def do_gwas(self, score_column, beta_column, covar_column):
        """
        Returns the results of the GWAS analysis, with or without beta, using the instance variables snp_true_false and
        beta_true_false and the lists, from the parameters, the lists of scores and, if applicable, the list of betas.

        :param score_column: the list of scores
        :param beta_column: the list of betas if performing analysis with beta
        :return: the values of the GWAS analysis with or without beta depending on runtime parameters
        """
        threshold = self.args_dict['threshold']
        if self.args_dict['beta'] is None:
            if self.args_dict['covar'] is None:
                return gwasWithoutBeta(self.snp_true_false, score_column, threshold)
            else:
                return gwasNoBetaCovar(self.snp_true_false, score_column, threshold, covar_column)
        else:
            if self.args_dict['covar'] is not None:
                return gwasBetaCovar(beta_column, self.beta_true_false, self.snp_true_false, score_column, threshold, covar_column)
            else:
                return gwasWithBeta(beta_column, self.beta_true_false, self.snp_true_false, score_column, threshold)

    def adjust_score(self, score):
        """
        Returns a list of adjusted p-values. Currently only the Benjamini-Hochberg method is supported.

        :param score: the list of p-values to adjust
        :return: the list of adjusted p-values
        """
        if self.args_dict['pvaladjust'] is None:
            return score
        else:
            return multipletests(score, alpha=self.args_dict['threshold'], method=self.args_dict['pvaladjust'])[1]

    def save_snp_score(self, snp, score, adjusted):  # pragma: no cover
        """
        Saves the file name, p-value, and adjusted p-value if set

        :param data: the data file
        :param score: the list of p-values
        :param adjusted: the list of adjusted p-values
        :return: saves a text file in the format file, p-value, adjusted p-value if adjustments has been selected
        """
        if self.args_dict['savep']:
            try:
                with open(self.args_dict['filename'] + '_scores.txt') as f:
                    f.close()
                    with open(self.args_dict['filename'] + '_scores.txt', 'a') as a:
                        if self.args_dict['pvaladjust'] is not None:
                            for (x, y, z) in zip(score, adjusted, snp):
                                a.write('\n' + z + '\t' + str(x) + '\t' + str(y))
                        else:
                            for (x, z) in zip(score, snp):
                                a.write('\n' + z + '\t' + str(x))
            except IOError:
                with open(self.args_dict['filename'] + '_scores.txt', 'w') as f:
                    if self.args_dict['pvaladjust'] is not None:
                        f.write('SNP ID \tP-Value \tP-Value Adjusted')
                    else:
                        f.write('SNP ID \tP-Value')
                self.save_snp_score(snp, score, adjusted)

    def save_settings(self):
        """
        Saves the parameters: Output file, analysis type, Known truth type, and threshold to a text file

        :return: saved settings file
        """
        writeSettings(self.args_dict)


def initialize():  # pragma: no cover
    """
    Displays graphics from commandline.py and loads runtime parameters, from a tuple, as a dictionary.

    :return: a dictionary of the runtime parameters
    """
    initializeGraphics()
    folder, analysis, truth, snp, score, beta, filename, threshold, separ, kt_type, \
    kt_type_separ, severity, pvaladjust, covar, savep= checkArgs()
    args = {'folder': folder, 'analysis': analysis, 'truth': truth, 'snp': snp, 'score': score, 'beta': beta,
            'filename': filename, 'threshold': threshold, 'separ': separ, 'kt_type': kt_type,
            'kt_type_separ': kt_type_separ, 'severity': severity, 'pvaladjust': pvaladjust, 'covar': covar, 'savep': savep}
    return args


def data_to_list(data_file, x, y, is_float=False):
    """
    Iterates over a file, returns a list of data parsed using x and y as the indexes of the data to be extracted.

    :param data_file: the file containing data
    :param x: the x index of the column containing the data
    :param y: the y index of the row containing the data
    :param is_float: if True, the data in the list will be represented as a float
    :return: the list of parsed data
    """
    column = list()
    for each in data_file.data.iteritems():
        if is_float:
            column.append(float(each[x][y]))
        else:
            column.append(each[x][y])
    return column


def main():  # pragma: no cover
    """
    Sets the args dictionary - the runtime parameters - from the initialize function, creates a new Winnow using those
    parameters, and performs the analysis.

    """
    args = initialize()
    w = Winnow(args)
    w.load_kt()
    w.write_to_file(w.do_analysis())
    w.save_settings()

	
if __name__ == "__main__":
    main()