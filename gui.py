from ast import parse
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from buildDataFrames import buildDataFrames
from parseProjectData import parseProjectData

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


def select_file(figure, canvas):
    dirname = fd.askdirectory()

    parsed_data = parseProjectData(dirname)

    dataframes = buildDataFrames(parsed_data)

    # filter out on wrist
    for subject_id in dataframes:
        df = dataframes[subject_id]
        df = df[df['On Wrist'] == True]

    # testing stuff
    df = dataframes['311']

    ax = figure.subplots()

    sns.lineplot(x='Datetime (UTC)', y='Movement intensity', data=df, ax=ax)
    canvas.draw()


root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)

figure = Figure(figsize=(6, 6))
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

filemenu.add_command(label="Open", command=lambda: select_file(figure, canvas))

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.mainloop()
