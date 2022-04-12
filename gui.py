from ast import parse
from tkinter import *
from tkinter import filedialog as fd
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from buildDataFrames import buildDataFrames
from parseProjectData import parseProjectData

from datetime import datetime


def select_file():
    dirname = fd.askdirectory()

    parsed_data = parseProjectData(dirname)

    dataframes = buildDataFrames(parsed_data)

    # filter out on wrist
    for subject_id in dataframes:
        df = dataframes[subject_id]
        df = df[df['On Wrist'] == True]

    # testing stuff
    df = dataframes['311']

    print(df['Datetime (UTC)'])

    sns.lineplot(x='Datetime (UTC)', y='Movement intensity', data=df)
    plt.show()


root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=select_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.mainloop()
