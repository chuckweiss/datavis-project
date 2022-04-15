from tkinter import Menu, Frame


def subjectSelect(root, menubar, dataframes):
    tkframes = {}

    filemenu = Menu(menubar, tearoff=0)
    menubar.delete("Subject")
    menubar.add_cascade(label="Subject", menu=filemenu)

    for subject_id in dataframes:
        frame = Frame(root)
        tkframes[subject_id] = frame
        # frame.grid(row=0, column=0, sticky="nsew")
        frame.pack(fill="both", expand=True)
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)

        filemenu.add_command(
            label=subject_id,
            command=lambda subject_id=subject_id: tkframes[subject_id].tkraise())

    return tkframes
