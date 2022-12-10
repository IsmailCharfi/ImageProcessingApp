import os
import tkinter
import customtkinter
from PIL import Image, ImageTk
import constant
from pgm import Pgm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from ppm import Ppm
import numpy as np

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry(f"{800}x{600}")
app.title("ImageProcessingApp")

original_pgm = None
original_ppm = None
image_type = constant.PGM
main_image_frame = None

# Button to upload image
button = customtkinter.CTkButton(master=app, text="Upload image", command=lambda: open_file())
button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
reset_button = customtkinter.CTkButton(master=app, text="reset", command=lambda: reset())
# select image type:
radiobutton_frame = customtkinter.CTkFrame(app)
radiobutton_frame.grid(row=0, column=3, padx=(
    20, 20), sticky="nsew")
radiobutton_frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
radio_var = tkinter.IntVar(value=0)
label_radio_group = customtkinter.CTkLabel(
    master=radiobutton_frame, text="choose you image file type:")
label_radio_group.grid(
    row=0, column=2, columnspan=1, padx=50, pady=10, sticky="")

radio_button_1 = customtkinter.CTkRadioButton(
    master=radiobutton_frame, variable=radio_var, value=0, text="pgm",
    command=lambda: choose_file_type(constant.PGM))
radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

radio_button_2 = customtkinter.CTkRadioButton(
    master=radiobutton_frame, variable=radio_var, value=1, text="ppm",
    command=lambda: choose_file_type(constant.PPM))
radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")


def open_file():
    global original_pgm
    global button
    global radiobutton_frame
    global image_type
    global main_image_frame
    message: string = ""
    type: string = ""
    if image_type == constant.PGM:
        message = 'Pgm File'
        type = '*.pgm'
    elif image_type == constant.PPM:
        message = 'Ppm File'
        type = '*.ppm'
    filename = customtkinter.filedialog.askopenfilename(filetypes=[(message, type)])
    file = open(filename, "r")
    file_data = file.readlines()
    file.close()

    if image_type == constant.PGM:
        original_pgm = Pgm.create_from_file(file_data)
        original_pgm.create_file("original")
        image_file = Image.open("original.pgm")
        noisy_image = original_pgm.noisify_image()
        noisy_image.display_image()
        filtered = noisy_image.apply_average_filter(3)
        # file = open("test.txt", 'w+')
        # for i in range(filtered.lines):
        #     for j in range(filtered.columns):
        #         file.write(str(filtered.data[i][j]) + ' ')
        #     if (i != filtered.lines - 1):
        #         file.write('\n')
        # file.close()
        filtered.display_image()
        filtered.create_file("filtered")
    else:
        original_ppm = Ppm.create_from_file(file_data)
        original_ppm.create_file("original")
        image_file = Image.open("original.ppm").resize((1000, 720))

    image = ImageTk.PhotoImage(image_file)
    main_image_frame = tkinter.Label(image=image)
    main_image_frame.image = image
    main_image_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    button.place_forget()
    radiobutton_frame.place_forget()
    reset_button.place(relx=0.1, rely=0.1)


def choose_file_type(type):
    global image_type
    image_type = type


def reset():
    global original_pgm
    global original_ppm
    global image_type
    global main_image_frame
    global reset_button

    main_image_frame.place_forget()
    reset_button.place_forget()
    original_ppm = None
    original_pgm = None
    radiobutton_frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
    button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)


app.mainloop()
