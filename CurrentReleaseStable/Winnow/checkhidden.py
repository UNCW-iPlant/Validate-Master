"""
Functions to detect if something is meant to be isHidden.

The main reason to use this function is in case some output folders carry a history file with them (for instance, .RHistory files)
which would cause an error when read by the Winnow program.
"""


import ctypes, os


def isHidden(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    return name.startswith('.') or hasHiddenAttribute(filepath)


def hasHiddenAttribute(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result


def checkList(check):
	test = list()
	for each in check:
		if not isHidden(each):
			test.append(each)
	return test