from ast import parse
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
import seaborn as sns
import pandas as pd
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import os

from buildDataFrames import buildDataFrames
from parseProjectData import parseProjectData

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


def select_file(figure):
    dirname = fd.askdirectory()
    parsed_data = parseProjectData(dirname)
    folder_name = os.path.basename(dirname)
    dataframes = buildDataFrames(parsed_data)

    # filter out on wrist
    plot_count = 0
    ax = figure.subplots(3, 1)
    for subject_id in dataframes:
        df = dataframes[subject_id]
        #df = df[df['On Wrist'] == True]   #idk if we should do this
        df.set_index("Datetime (UTC)", inplace=True)
        ax[plot_count].plot(df["Movement intensity"])
        ax[plot_count].xaxis.set_major_locator(plt.MaxNLocator(4))
        ax[plot_count].set_title(subject_id)
        plot_count += 1

    axes = plt.axes(plt.axes([0.1, 0.1, 0.1, 0.1])) #testing buttons, wont show up currently
    bnext = Button(axes, label='Add', color="yellow")

    root.geometry("1400x600")
    figure.subplots_adjust(hspace=0.5)
    root.title(folder_name)
    canvas.draw()


def description():
    pass


root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)

figure = Figure(figsize=(20, 7), dpi=100)
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

filemenu.add_command(label="Open", command=lambda: select_file(figure))
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# plot_button = tk.Button(master=root,
#                      command=description,
#                      height=2,
#                      width=10,
#                      text="Plot")
# plot_button.pack()

root.config(menu=menubar)
root.geometry("200x200")
root.eval('tk::PlaceWindow . center')
root.mainloop()
