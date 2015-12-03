from commandline import initialize_graphics, check_args
import rpy2.robjects as robjects
import os


class Demonstrate:
    def __init__(self, args):
        """
        Creates a new instance of a Demonstrate object using the runtime arguments.

        :param args: dictionary of arguments
        """
        self.args = args
        self.load_r()

    def load_r(self):
        """
        Loads either Demonstrate or Demonstrate2 to the rpy2 global environment depending on the mode given at runtime.

        """
        if self.args["mode"] == "demonstrate":
            with open(os.getcwd()[:os.getcwd().index('DemonstrateDevel')] +
                              "DemonstrateDevel/DemoMPlot/R/Demonstrate.R") as f:
                dem = f.read()
            robjects.r(dem)
        elif self.args["mode"] == "demonstrate2":
            with open(os.getcwd() + "/DemoMPlot/R/Demonstrate2.R") as g:
                dem2 = g.read()
            robjects.r(dem2)

    def do_demonstrate(self):
        """
        Performs the Demonstrate or Demonstrate2 function depending on the mode given at runtime.

        """
        if self.args["mode"] == "demonstrate":
            self.demonstrate_one()
        elif self.args["mode"] == "demonstrate2":
            self.demonstrate_two()

    def demonstrate_one(self):
        """
        Executes the original Demonstrate function using the arguments given at runtime.

        Loads the Demonstrate R object from the global environment, checks if the title arguments have the pdf
        extension and adds them if not, and performs the R function with the given runtime arguments as the function
        parameters
        """
        r_dem = robjects.globalenv['Demonstrate']
        if self.args.get("auctitle") is not None:
            self.args["auctitle"] = add_pdf_extension(self.args["auctitle"])
        if self.args.get("maetitle") is not None:
            self.args["maetitle"] = add_pdf_extension(self.args["maetitle"])
        r_dem(self.args["dir"], check_for_null(self.args.get("output")), check_for_null(self.args.get("settings")),
              self.args["xauc"] is False, self.args["auctitle"], self.args["xmae"] is False,
              self.args["maetitle"] + ".pdf", self.args["heritstring"], self.args["heritvalue"],
              self.args["structstring"], self.args["structvalue"])

    def demonstrate_two(self):
        """
        Executes the Demonstrate2 function using the arguments given at runtime.

        Loads the Demonstrate2 R object from the global environment, checks if the title arguments have the pdf
        extension and adds them if not, and performs the R function with the given runtime arguments as the function
        parameters
        """
        r_dem2 = robjects.globalenv['Demonstrate2']
        self.args["postitle"] = add_pdf_extension(self.args["postitle"])
        r_dem2(self.args["dir"], check_for_null(self.args.get("output")), check_for_null(self.args.get("settings")),
               self.args["xpos"] is False, self.args["postitle"], self.args["xerror"] is False, self.args["errortitle"],
               self.args["extraplots"], self.args["aucmin"], self.args["aucmax"], self.args["maemin"],
               self.args["maemax"])


def check_for_null(entry):
    """
    If an entry is 'None' returns the rpy2 implementation of R's NULL to be passed in the R function parameters.

    :param entry: the object to check for None
    :return: rpy2 NULL if the object is None, otherwise the original entry
    """
    if entry is None:
        return robjects.NULL
    else:
        return entry


def add_pdf_extension(s):
    """
    Adds a .pdf extension to the string if it doesn't end with it.

    :param s: file name string
    :return: file name with .pdf appended to it
    """
    if len(s) < 4 or s[-4:] != ".pdf":
        return s + ".pdf"
    else:
        return s


def initialize():
    """
    Displays graphics from commandline.py, and loads the runtime parameters to be used while instantiating a Demonstrate
    object.

    """
    initialize_graphics()
    return check_args()


def main():
    """
    Sets the args dictionary - the runtime parameters - from the initialize function, creates a new Demonstrate
    object using that dictionary, and produces the demonstrate graphics.

    """
    args = initialize()
    demon = Demonstrate(args)
    demon.do_demonstrate()


if __name__ == "__main__":
    main()
