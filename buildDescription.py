from tkinter import Toplevel, Entry, END, Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_plot(top, df, col):
    frame = Frame(top, pady=1, padx=1)
    frame.pack(side="left")

    fig = Figure()
    # fig.tight_layout(rect=[0, 0, .8, 1])

    ax = fig.subplots()
    # ax.autoscale()

    ax.hist(df[col], bins=12)
    ax.set_title("Density vs. " + col)

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(side='left', fill='both', expand=1)
    # canvas.draw()


def display_desc(top, df, col):
    df = df[[col]]
    desc = df.describe(
        percentiles=[.025, .25, .5, .75, .975, .999], datetime_is_numeric=True)

    create_plot(top, df, col)

    desc = desc.T
    desc["skew"] = df.skew(axis=0)[0]
    desc["kurt"] = df.kurt(axis=0)[0]
    desc = desc.T

    frame = Frame(top)
    frame.pack(side='right', expand=True)

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


def buildDescription(root, df, col, menu):
    def open_popup():
        top = Toplevel(root)
        top.geometry("950x650")
        top.title("Description")
        display_desc(top, df, col)

    menu.add_command(label="Description", command=open_popup)
