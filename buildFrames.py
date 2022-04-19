import pandas as pd
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame, Menu, Label
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from buildDescription import buildDescription


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
        ax.set_xlim(df.index[0], df.index[-1])

        canvas.draw_idle()

    for sample in ('1min', '15min', '30min', '1H', '2H', '4H', '1d', '1w'):
        menu.add_command(
            label=sample, command=lambda sample=sample: sample_dataframe(sample))


def setup_timezone_select(dataframe, axes, cans, topax, 
                          topcanvas, rclickmenu, timezone_selection):
    menu = Menu(rclickmenu, tearoff=0)
    rclickmenu.add_cascade(label="Timezone", menu=menu)

    def set_timezone(timezone):
        timezone_selection["timezone"] = timezone
        df = dataframe
        if (timezone == "Local"):
            df["Datetime (Local)"] = df.index + \
                pd.TimedeltaIndex(df["Timezone (minutes)"], unit='min')
            df = df.set_index("Datetime (Local)", inplace=False)
            df = df[~df.index.duplicated(keep='first')]
            df = df.resample("1min").mean()

        topax.clear()

        count = 0
        for col, color in (
            [("Acc magnitude avg", "b"),
                ("Eda avg", "k"),
                ("Temp avg", "r"),
                ("Movement intensity", "g"),
                ("Steps count", "b"),
                ("Rest", "indigo")]):
            data = df[col]

            axes[count].clear()
            axes[count].plot(data, color=color)
            axes[count].set_xlim(df.index[0], df.index[-1])
            topax.plot(data, color=color, alpha=0.5)

            cans[count].draw_idle()

            count += 1

        topax.xaxis.set_ticklabels([])
        topax.set_xticks([])
        topax.set_yticks([])
        topax.set_xlim(df.index[0], df.index[-1])
        topcanvas.draw_idle()

    menu.add_command(label="UTC", command=lambda: set_timezone("UTC"))
    menu.add_command(label="Local", command=lambda: set_timezone("Local"))


def setup_top(f, df, axes, cans, timezone_selection):
    frame = Frame(f, height=1)
    frame.pack(expand=True)
    frame.place(relheight=0.1, relwidth=1, rely=0)

    fig = Figure(layout='tight')
    ax = fig.subplots()

    ax.xaxis.set_ticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(df.index[0], df.index[-1])

    label = Label(frame, text="Viewfinder", width=20, height=5)
    label.pack(side="left")

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    canvas.draw()

    rclickmenu = Menu(frame, tearoff=0)
    label.bind("<Button-3>", lambda event,
               rclickmenu=rclickmenu: do_popup(event, rclickmenu))

    setup_timezone_select(df, axes, cans, ax, canvas, rclickmenu, timezone_selection)

    return (ax, canvas)


def plot_data(root, topframe, axes, cans, df, timezone_selection):
    (topax, topcanvas) = setup_top(topframe, df, axes, 
                                   cans, timezone_selection)

    cans.append(topcanvas)

    pos = 0.1

    for col, color in (
        [("Acc magnitude avg", "b"),
            ("Eda avg", "k"),
            ("Temp avg", "r"),
            ("Movement intensity", "g"),
            ("Steps count", "b"),
            ("Rest", "indigo")]):
        data = df[col]

        frame = Frame(topframe, pady=1)
        frame.pack(expand=True)
        frame.place(relheight=(0.9 / 6), relwidth=1, rely=pos)

        pos += (0.9 / 6)

        fig = Figure(layout='tight')
        ax = fig.subplots()
        axes.append(ax)

        ax.set_xlim(df.index[0], df.index[-1])

        ax.plot(data, color=color)
        topax.plot(data, color=color, alpha=0.5)

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
        buildDescription(root, df, col, rclickmenu, timezone_selection)

    return setup_span(topax, axes, cans)


def buildFrames(root, tkframes, dataframes, timezone_selection):
    axes = {}
    cans = {}
    spans = []

    for subject_id in tkframes:
        df = dataframes[subject_id]
        df = df[df["On Wrist"] == True]
        
        timezone_selection[subject_id] = { "timezone": "UTC" }

        if df.empty:
            continue

        df["Datetime (UTC)"] = pd.to_datetime(
            df["Datetime (UTC)"], utc=True, infer_datetime_format=True)
        df = df.set_index("Datetime (UTC)", inplace=False)
        df = df[~df.index.duplicated(keep='first')]
        df = df.resample("1min").mean()

        axes[subject_id] = []
        cans[subject_id] = []

        span = plot_data(root, tkframes[subject_id],
                         axes[subject_id], cans[subject_id], df, 
                         timezone_selection[subject_id])

        spans.append(span)

    return spans
