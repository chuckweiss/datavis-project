from distutils.command.build import build
from turtle import width
import pandas as pd
from re import sub
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame, Button, Canvas, Menu, Label
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from buildDescription import buildDescription
# matplotlib.use("TkAgg")
plt.tight_layout()
matplotlib.pyplot.ion()


def do_popup(event, m):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()


def setup_span(ax, axes, cans):
    def span_select(xmin, xmax):
        indmin = xmin
        indmax = xmax
        for ax in axes:
            ax.set_xlim(indmin, indmax)
        for canvas in cans:
            canvas.draw_idle()

    return SpanSelector(
        ax,
        span_select,
        "horizontal",
        useblit=True,
        props=dict(alpha=0.5, facecolor="tab:blue"),
        interactive=True,
        drag_from_anywhere=True
    )


def setup_aggregation(df, col, ax, canvas, menu, color):
    def sample_dataframe(sample):
        df2 = df.resample(sample).mean()
        data = df2[col]

        ax.clear()
        ax.plot(data, color=color)

        canvas.draw_idle()

    for sample in ('1min', '15min', '30min', '1H', '2H', '4H', '1d', '1w'):
        menu.add_command(
            label=sample, command=lambda sample=sample: sample_dataframe(sample))


def setup_top(f):
    frame = Frame(f, height=1)
    frame.pack(expand=True)
    frame.place(relheight=0.2, relwidth=1, rely=0)

    fig = Figure()
    ax = fig.subplots()

    Label(frame, text="Viewfinder", width=20, height=5).pack(side="left")

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    canvas.draw()

    return (ax, canvas)


def plot_data(root, topframe, axes, cans, df):
    (topax, topcanvas) = setup_top(topframe)

    cans.append(topcanvas)

    pos = 0.2

    for col, color in (
        [("Acc magnitude avg", "b"),
            ("Eda avg", "k"),
            ("Temp avg", "r"),
            ("Movement intensity", "g")]):
        data = df[col]

        frame = Frame(topframe, pady=1)
        frame.pack(expand=True)
        frame.place(relheight=0.2, relwidth=1, rely=pos)
        pos += 0.2

        fig = Figure()
        ax = fig.subplots()
        axes.append(ax)

        topax.set_xlim(df.index[0], df.index[-1])
        ax.set_xlim(df.index[0], df.index[-1])

        ax.plot(data, color=color)
        topax.plot(data, color=color)

        title = Label(frame, text=col, width=20, height=5)
        title.pack(side="left")

        rclickmenu = Menu(topframe, tearoff=0)
        agg_menu = Menu(rclickmenu, tearoff=0)
        rclickmenu.add_cascade(label="Aggregation", menu=agg_menu)

        title.bind("<Button-3>", lambda event,
                   rclickmenu=rclickmenu: do_popup(event, rclickmenu))

        canvas = FigureCanvasTkAgg(fig, frame)
        cans.append(canvas)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        canvas.draw()

        setup_aggregation(df, col, ax, canvas, agg_menu, color)
        buildDescription(root, df, col, rclickmenu)

    return setup_span(topax, axes, cans)


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

        df = df.resample("1min").mean()

        axes[subject_id] = []
        cans[subject_id] = []

        span = plot_data(root, tkframes[subject_id],
                         axes[subject_id], cans[subject_id], df)

        spans.append(span)

    return spans
