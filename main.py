from tkinter import *
from dataSelect import dataSelect
from subjectSelect import subjectSelect
from buildFrames import buildFrames

data = []


def handle_data(root, menubar):
    dataframes = dataSelect()
    tkframes = subjectSelect(root, menubar, dataframes)
    data.append(buildFrames(root, tkframes, dataframes))


def build_root():
    return Tk()


root = build_root()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=lambda: handle_data(root, menubar))

menubar.add_cascade(label="Subject")

root.config(menu=menubar)
root.geometry("1500x800")
root.mainloop()
