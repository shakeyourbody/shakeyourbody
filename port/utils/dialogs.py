from tkinter import Tk, filedialog, simpledialog
from pathlib import Path
import os


def openfile(title='Select a file to open', filetypes=[('all files', '.*')]):
    Tk().withdraw()
    fname = filedialog.askopenfilename(
        initialdir=os.getcwd(),  # Path.home(),
        title=title,
        filetypes=filetypes
    )
    return fname


def savefile(title='Select a file to save', filetypes=[('all files', '.*')]):
    Tk().withdraw()
    fname = filedialog.asksaveasfile(
        initialdir=os.getcwd(),  # Path.home(),
        title=title,
        filetypes=filetypes
    )
    return fname


def ask_string(title='Input dialog', prompt='Insert a string', default=''):
    Tk().withdraw()
    res = simpledialog.askstring(title, prompt)
    return res if res is not None else default
