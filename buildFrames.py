from re import sub
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # NavigationToolbar2Tk
from tkinter import Frame, Button, Canvas, Menu
from matplotlib.figure import Figure
# matplotlib.use("TkAgg")
plt.tight_layout()


def buildFrames(root, tkframes, dataframes):
    for subject_id in tkframes:
        df = dataframes[subject_id]
        df = df.truncate(after=100)  # make faster, needs fix tho
        df = df.set_index("Datetime (UTC)", inplace=False)

        topframe = Frame(tkframes[subject_id])
        topframe.pack(expand=True)

        topfig = Figure(figsize=(10, 1))
        topax = topfig.subplots()
        topax.set_title("All data")

        topcanvas = FigureCanvasTkAgg(topfig, topframe)
        topcanvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        topcanvas.draw()

        for col, color in (
            [("Acc magnitude avg", "b"),
             ("Eda avg", "k"),
             ("Temp avg", "r"),
             ("Movement intensity", "g")]):
            data = df[col]

            frame = Frame(tkframes[subject_id], pady=1)
            frame.pack(expand=True)

            btn = Button(frame, text="Description")
            btn.pack(side="right")

            #  THHIS SHOULD WORK
            # dropdown = Menu(root, tearoff=0)
            # dropdown.add_command(label='Description')

            # def do_popup(event):
            #     try:
            #         dropdown.tk_popup(event.x_root, event.y_root)
            #     finally:
            #         dropdown.grab_release()

            # frame.bind("<Button-3>", do_popup)

            fig = Figure(figsize=(10, 1))
            ax = fig.subplots()
            ax.plot(data, color=color)
            ax.set_title(col)
            topax.plot(data, color=color)

            f = Frame(frame)
            f.pack()
            canvas = FigureCanvasTkAgg(fig, f)
            canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
            canvas.draw()
