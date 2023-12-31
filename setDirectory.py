"""
Browse to a directory, return the path as a string.

Author: Steven J. von Dohlen

getCurrentDirectory -- returns string with the working directory path
browseForDirectory -- returns string with the selected directory path
"""
import os
import tkinter as tk
from tkinter import filedialog


def main()->None:
    """
    Sample use of the functions included.
    """
    directory = getCurrentDirectory()
    print(directory)

    directory = browseForDirectory()
    print(directory)

def getCurrentDirectory()->str:
    result: str
    result = os.getcwdb() # os.getcwd() returns a str, os.getcwdb() returns bytes
    return result

def browseForDirectory()->str:
    result: str
    root = tk.Tk()
    root.withdraw()
    result = filedialog.askdirectory()
    return result


if __name__ == "__main__":
    main()