"""
Functions to detect if something is meant to be isHidden.

The main reason to use this function is in case some output folders carry a history file with them (for instance, .RHistory files)
which would cause an error when read by the Winnow program.
"""


import ctypes
import os


def isHidden(filepath):
    """
    Returns whether the file is hidden by name or attribute

    :param filepath: the file path to check if hidden
    :return: True if the file is hidden
    """
    name = os.path.basename(os.path.abspath(filepath))
    return name.startswith('.') or hasHiddenAttribute(filepath)


def hasHiddenAttribute(filepath):
    """
    Returns whether the file has hidden attributes

    :param filepath: the file path to check for hidden attributes
    :return: True if the file has a hidden attribute
    """
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result


def checkList(check):
    """
    Returns the files that are not hidden

    :param check: list of file paths to check if hidden
    :return: the list of file paths that are not hidden
    """
    test = list()
    for each in check:
        if not isHidden(each):
            test.append(each)
    return test
