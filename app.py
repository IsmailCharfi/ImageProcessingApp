import os
import tkinter
import customtkinter
from PIL import Image, ImageTk

from pgm import Pgm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry(f"{800}x{600}")
app.title("ImageProcessingApp")

original_pgm = None

button = customtkinter.CTkButton(master=app, text="Click me", command=lambda: open_file())
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


def open_file():
    global original_pgm
    global button

    filename = customtkinter.filedialog.askopenfilename(filetypes=[('Pgm Files', '*.pgm')])
    file = open(filename, "r")
    file_data = file.readlines()
    file.close()
    original_pgm = create_pgm_from_file(file_data)
    original_pgm.create_pgm_file("original")
    image_file = Image.open("original.pgm").resize((1000, 720))
    image = ImageTk.PhotoImage(image_file)
    label = tkinter.Label(image=image)
    label.image = image
    label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    button.place_forget()


def display_pgm_image(filename):
    img_read = mpimg.imread(filename + ".pgm")
    plt.imshow(img_read, cmap='gray')
    plt.show()


def create_pgm_from_file(file_data):
    words = file_data[2].split()
    columns = int(words[0])
    lines = int(words[1])
    magic_number = file_data[0]
    comment = file_data[1]
    max_value = file_data[3]
    data = [[0 for x in range(columns)] for y in range(lines)]
    for i in range(4, len(file_data)):
        ll = file_data[i].split()
        for j in range(0, len(ll)):
            data[i - 4][j] = int(ll[j])
    return Pgm(magic_number, comment, columns, lines, max_value, data)


app.mainloop()
