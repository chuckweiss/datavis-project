from ast import parse
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.widgets import Button, SpanSelector
import matplotlib.pyplot as plt
import os
from buildDataFrames import buildDataFrames
from parseProjectData import parseProjectData
from descriptionButton import descriptionButton

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


def select_file(figure, ax):
    dirname = fd.askdirectory()
    parsed_data = parseProjectData(dirname)
    folder_name = os.path.basename(dirname)
    dataframes = buildDataFrames(parsed_data)

    # filter out on wrist
    plot_count = 1
    # for subject_id in dataframes:
    #     df = dataframes[subject_id]

    df = dataframes["310"]
    df.set_index("Datetime (UTC)", inplace=True)

    def setup_ax(df, ax1, ax2, title, color):
        ax1.plot(df[title], color=color)
        ax2.plot(df[title], color=color)
        ax1.xaxis.set_major_locator(plt.MaxNLocator(4))
        ax1.set_title(title)

    setup_ax(df, ax[1], ax[0], "Acc magnitude avg", 'b')
    setup_ax(df, ax[2], ax[0], "Eda avg", 'k')
    setup_ax(df, ax[3], ax[1], "Temp avg", 'r')
    setup_ax(df, ax[4], ax[1], "Movement intensity", 'g')

    plot_count += 1

    ax[0].xaxis.set_major_locator(plt.MaxNLocator(4))
    # span = SpanSelector(
    #     ax[0],
    #     onselect,
    #     "horizontal",
    #     useblit=True,
    #     props=dict(alpha=0.5, facecolor="tab:blue"),
    #     interactive=True,
    #     drag_from_anywhere=True
    # )
    root.geometry("1400x600")
    figure.subplots_adjust(hspace=1.2)
    root.title(folder_name)

    def button_setup(b):
        b.ax.patch.set_visible(True)
        b.label.set_visible(True)
        b.ax.axis('on')

    button_setup(b1)
    button_setup(b2)
    button_setup(b3)
    button_setup(b4)


# def onselect(xmin, xmax):
#     indmin = ax[1].
#     indmax = min(len(x) - 1, indmax)

#     region_x = x[indmin:indmax]
#     region_y = y[indmin:indmax]

#     if len(region_x) >= 2:
#         line2.set_data(region_x, region_y)
#         ax2.set_xlim(region_x[0], region_x[-1])
#         ax2.set_ylim(region_y.min(), region_y.max())
#         fig.canvas.draw_idle()


root = Tk()

figure = Figure(figsize=(20, 7), dpi=100)
canvas = FigureCanvasTkAgg(figure, root)
ax = figure.subplots(5, 1)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

b1 = descriptionButton(root, figure, [0.905, 0.113, 0.1, 0.075])
b2 = descriptionButton(root, figure, [0.905, 0.285, 0.1, 0.075])
b3 = descriptionButton(root, figure, [0.905, 0.457, 0.1, 0.075])
b4 = descriptionButton(root, figure, [0.905, 0.632, 0.1, 0.075])

canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
canvas.draw()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)

filemenu.add_command(
    label="Open", command=lambda: select_file(figure, ax))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)


root.config(menu=menubar)
root.geometry("200x200")
root.eval('tk::PlaceWindow . center')
root.mainloop()
