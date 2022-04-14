from tkinter import *
import matplotlib.pyplot as plt


def descriptionButton(root, figure, coords):
    def desc_popup(_):
        top = Toplevel(root)
        top.geometry("750x250")
        top.title("Description")
        Label(top, text="Hello World!", font=(
            'Mistral 18 bold')).place(x=150, y=80)

    axes = figure.add_axes(coords)
    b = plt.Button(axes, label='Description', color="yellow")
    b.on_clicked(desc_popup)
    b.ax.patch.set_visible(False)
    b.label.set_visible(False)
    b.ax.axis('off')

    return b
