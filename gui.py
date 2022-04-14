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


def select_file(figure, canvas):
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

    root.geometry("1400x600")
    figure.subplots_adjust(hspace=0.5)
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
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

filemenu.add_command(label="Open", command=lambda: select_file(figure, canvas))

axes1 = figure.add_axes([0.905, 0.16, 0.1, 0.075])
b1 = plt.Button(axes1, label='Description', color="yellow")
b1.on_clicked(description1)
b1.ax.patch.set_visible(False)
b1.label.set_visible(False)
b1.ax.axis('off')

axes2 = figure.add_axes([0.905, 0.45, 0.1, 0.075])
b2 = plt.Button(axes2, label='Description', color="yellow")
b2.on_clicked(description2)
b2.ax.patch.set_visible(False)
b2.label.set_visible(False)
b2.ax.axis('off')

axes3 = figure.add_axes([0.905, 0.75, 0.1, 0.075])
b3 = plt.Button(axes3, label='Description', color="yellow")
b3.on_clicked(description3)
b3.ax.patch.set_visible(False)
b3.label.set_visible(False)
b3.ax.axis('off')

canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
canvas.draw()

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


root.config(menu=menubar)
root.geometry("200x200")
root.eval('tk::PlaceWindow . center')
root.mainloop()
