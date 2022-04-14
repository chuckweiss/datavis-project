from re import sub
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # NavigationToolbar2Tk
from tkinter import Frame, Button, Canvas, Menu
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
# matplotlib.use("TkAgg")
plt.tight_layout()
matplotlib.pyplot.ion()


def buildFrames(root, tkframes, dataframes):
    axes = {}
    cans = {}
    spans = []

    for subject_id in tkframes:
        df = dataframes[subject_id]
        df = df.truncate(after=100)  # make faster, needs fix tho
        df = df.set_index("Datetime (UTC)", inplace=False)

        topframe = Frame(tkframes[subject_id])
        topframe.pack(expand=True)

        topfig = Figure(figsize=(10, 1))
        topax = topfig.subplots()

        axes[subject_id] = []  # [topax]

        topcanvas = FigureCanvasTkAgg(topfig, topframe)
        topcanvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        topcanvas.draw()

        cans[subject_id] = [topcanvas]

        def span_select(xmin, xmax):
            indmin = round(xmin)
            indmax = round(xmax)
            for ax in axes[subject_id]:
                ax.set_xlim(indmin, indmax)
            for canvas in cans[subject_id]:
                canvas.draw_idle()

        span = SpanSelector(
            topax,
            span_select,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:blue"),
            interactive=True,
            drag_from_anywhere=True
        )

        spans.append(span)

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

            axes[subject_id].append(ax)

            ax.plot(data, color=color)
            topax.plot(data, color=color)

            canvas = FigureCanvasTkAgg(fig, frame)
            cans[subject_id].append(canvas)
            canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
            canvas.draw()

    return spans
