from locale import normalize
from tkinter import Toplevel, Entry, END, Frame
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_plot(top, dataframe, col, timezone):
    df = dataframe
    if (timezone == "Local"):
            df["Datetime (Local)"] = df.index + \
                pd.TimedeltaIndex(df["Timezone (minutes)"], unit='min')
            df = df.set_index("Datetime (Local)", inplace=False)
            df = df[~df.index.duplicated(keep='first')]
            df = df.resample("1min").mean()

    frame = Frame(top, pady=1, padx=1)
    frame.pack()
    frame.place(relheight=1/3)

    fig = Figure(layout='tight')

    ax = fig.subplots()
    ax.hist(df[col], bins=25, density=True, stacked=False)

    ax.set_title("Probability Density vs. " + col)

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(side='left', fill='both', expand=1)

    ###

    df_h = df.groupby(df.index.hour).mean()

    frame = Frame(top, pady=1, padx=1)
    frame.pack()
    frame.place(relheight=1/3, rely=1/3)

    fig = Figure(layout='tight')

    ax = fig.subplots()
    ax.bar(df_h.index, height=df_h[col])
    ax.set_ylim(ymin=df_h[col].min(), ymax=df_h[col].max())

    ax.set_title(col + " vs. Hour of the Day")

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(side='left', fill='both', expand=1)

    ###

    df_d = df.groupby(df.index.day).mean()

    frame = Frame(top, pady=1, padx=1)
    frame.pack()
    frame.place(relheight=1/3, rely=2/3)

    fig = Figure(layout='tight')

    ax = fig.subplots()
    ax.bar(df_d.index, height=df_d[col])
    ax.set_ylim(ymin=df_d[col].min(), ymax=df_d[col].max())

    ax.set_title(col + " vs. Day")

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(side='left', fill='both', expand=1)


def display_desc(top, dataframe, col, timezone):
    df = dataframe[[col]]
    desc = df.describe(
        percentiles=[.025, .25, .5, .75, .975, .999], datetime_is_numeric=True)

    desc = desc.T
    desc["skew"] = df.skew(axis=0)[0]
    desc["kurt"] = df.kurt(axis=0)[0]
    desc = desc.T

    frame = Frame(top)
    frame.pack(side='right', expand=False)

    create_plot(top, dataframe, col, timezone)

    e = Entry(frame, width=20, fg='black')
    e.grid(row=0, column=1)
    e.insert(END, col)

    count = 1
    for name, row in desc.iterrows():
        data = row[col]

        name_entry = Entry(frame, width=20, fg='black')
        data_entry = Entry(frame, width=20, fg='black')

        name_entry.grid(row=count, column=0)
        data_entry.grid(row=count, column=1)

        name_entry.insert(END, name)
        data_entry.insert(END, data)

        count += 1


def buildDescription(root, df, col, menu, timezone_selection):
    def open_popup():
        top = Toplevel(root)
        top.geometry("950x650")
        top.title("Description")
        display_desc(top, df, col, timezone_selection["timezone"])

    menu.add_command(label="Description", command=open_popup)
