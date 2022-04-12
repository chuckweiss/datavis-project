from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import pandas as pd

def csv_dataframe(filename):
    return pd.read_csv(filename)

def select_file():
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    df = csv_dataframe(filename)

    print(df)

    # showinfo(title="Selected File", message=df.head(-1))

    
   
root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=select_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.mainloop()
