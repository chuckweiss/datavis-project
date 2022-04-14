from ast import parse
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
from click import password_option
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.widgets import Button, SpanSelector
import matplotlib.pyplot as plt
import os
from buildDataFrames import buildDataFrames
from parseProjectData import parseProjectData

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
    global df
    df = dataframes["310"]
    # filter out on wrist
    plot_count = 1
    # for subject_id in dataframes:
    #     df = dataframes[subject_id]
    
    df.set_index("Datetime (UTC)", inplace=True)

    line, = ax[1].plot(df["Acc magnitude avg"], color='b')
    ax[0].plot(df["Acc magnitude avg"], color='b')
    ax[1].xaxis.set_major_locator(plt.MaxNLocator(4))
    ax[1].set_title("Acc magnitude avg")

    ax[2].plot(df["Eda avg"], color='k')
    ax[0].plot(df["Eda avg"], color='k')
    ax[2].xaxis.set_major_locator(plt.MaxNLocator(4))
    ax[2].set_title("Eda avg")

    ax[3].plot(df["Temp avg"], color='r')
    ax[0].plot(df["Temp avg"], color='r')
    ax[3].xaxis.set_major_locator(plt.MaxNLocator(4))
    ax[3].set_title("Temp avg")

    ax[4].plot(df["Movement intensity"], color='g')
    ax[0].plot(df["Movement intensity"], color='g')
    ax[4].xaxis.set_major_locator(plt.MaxNLocator(4))
    ax[4].set_title("Movement intensity")


    plot_count += 1
        
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(4))

    root.geometry("1400x600")
    figure.subplots_adjust(hspace=1.2)
    root.title(folder_name)
    
    b1.ax.patch.set_visible(True)
    b1.label.set_visible(True)
    b1.ax.axis('on')

    b2.ax.patch.set_visible(True)
    b2.label.set_visible(True)
    b2.ax.axis('on')

    b3.ax.patch.set_visible(True)
    b3.label.set_visible(True)
    b3.ax.axis('on')

    b4.ax.patch.set_visible(True)
    b4.label.set_visible(True)
    b4.ax.axis('on')


def onselect(xmin, xmax):
    indmin = round(xmin)
    indmax = round(xmax)
    ax[1].set_xlim(indmin, indmax)
    ax[2].set_xlim(indmin, indmax)
    ax[3].set_xlim(indmin, indmax)
    ax[4].set_xlim(indmin, indmax)
    figure.canvas.draw_idle()
        

def desc_popup():
    top=Toplevel(root)
    top.geometry("750x250")
    top.title("Description")
    Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)


def description1(val):
    desc_popup()


def description2(val):
    desc_popup()


def description3(val):
    desc_popup()


root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)

figure = Figure(figsize=(20, 7), dpi=100)
canvas = FigureCanvasTkAgg(figure, root)
ax = figure.subplots(5, 1)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
filemenu.add_command(label="Open", command=lambda: select_file(figure, ax))

axes1 = figure.add_axes([0.905, 0.113, 0.1, 0.075])
b1 = plt.Button(axes1, label='Description', color="yellow")
b1.on_clicked(description1)
b1.ax.patch.set_visible(False)
b1.label.set_visible(False)
b1.ax.axis('off')

axes2 = figure.add_axes([0.905, 0.285, 0.1, 0.075])
b2 = plt.Button(axes2, label='Description', color="yellow")
b2.on_clicked(description2)
b2.ax.patch.set_visible(False)
b2.label.set_visible(False)
b2.ax.axis('off')

axes3 = figure.add_axes([0.905, 0.457, 0.1, 0.075])
b3 = plt.Button(axes3, label='Description', color="yellow")
b3.on_clicked(description3)
b3.ax.patch.set_visible(False)
b3.label.set_visible(False)
b3.ax.axis('off')

axes4 = figure.add_axes([0.905, 0.632, 0.1, 0.075])
b4 = plt.Button(axes4, label='Description', color="yellow")
b4.on_clicked(description3)
b4.ax.patch.set_visible(False)
b4.label.set_visible(False)
b4.ax.axis('off')

span = SpanSelector(
        ax[0],
        onselect,
        "horizontal",
        useblit=True,
        props=dict(alpha=0.5, facecolor="tab:blue"),
        interactive=True,
        drag_from_anywhere=True,
    )

canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
canvas.draw()

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.geometry("200x200")
root.eval('tk::PlaceWindow . center')
root.mainloop()
