from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from buildDataFrames import buildDataFrames
from parseProjectData import parseProjectData

def select_file():
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    dirname = fd.askdirectory()

    parsed_data = parseProjectData(dirname)

    print(buildDataFrames(parsed_data))

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
