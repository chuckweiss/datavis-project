import pandas as pd
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


def plot_data(frame, axes, cans, df):
    topframe = Frame(frame)
    topframe.pack(expand=True)

    topfig = Figure(figsize=(10, 1))
    topax = topfig.subplots()

    topcanvas = FigureCanvasTkAgg(topfig, topframe)
    topcanvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    topcanvas.draw()

    cans.append(topcanvas)

    def span_select(xmin, xmax):
        indmin = xmin
        indmax = xmax
        for ax in axes:
            ax.set_xlim(indmin, indmax)
        for canvas in cans:
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

    # spans.append(span)

    for col, color in (
        [("Acc magnitude avg", "b"),
            ("Eda avg", "k"),
            ("Temp avg", "r"),
            ("Movement intensity", "g")]):
        data = df[col]

        f = Frame(frame, pady=1)
        f.pack(expand=True)

        btn = Button(f, text="Description")
        btn.pack(side="right")

        #  THHIS SHOULD WORK
        dropdown = Menu(f, tearoff=0)
        dropdown.add_command(label='Description')

        def do_popup(event):
            try:
                dropdown.tk_popup(event.x_root, event.y_root)
            finally:
                dropdown.grab_release()

        btn.bind("<Button-3>", do_popup)

        fig = Figure(figsize=(10, 1))
        ax = fig.subplots()

        axes.append(ax)

        topax.set_xlim(df.index[0], df.index[-1])
        ax.set_xlim(df.index[0], df.index[-1])

        ax.plot(data, color=color)
        topax.plot(data, color=color)

        canvas = FigureCanvasTkAgg(fig, f)
        cans.append(canvas)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        canvas.draw()

    return span


def buildFrames(root, tkframes, dataframes):
    axes = {}
    cans = {}
    spans = []

    for subject_id in tkframes:
        df = dataframes[subject_id]
        df = df[df["On Wrist"] == True]

        if df.empty:
            continue

        df["Datetime (UTC)"] = pd.to_datetime(df["Datetime (UTC)"], utc=True)

        df = df.set_index("Datetime (UTC)", inplace=False)

        df = df[~df.index.duplicated(keep='first')]

        # df = df.resample('1H').mean()

        axes[subject_id] = []
        cans[subject_id] = []

        span = plot_data(tkframes[subject_id],
                         axes[subject_id], cans[subject_id], df)

        spans.append(span)

    return spans
