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
button = customtkinter.CTkButton(
    master=app, text="Upload image", command=lambda: open_file())
button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
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

# create sidebar frame with widgets
sidebar_frame = customtkinter.CTkFrame(app, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)
logo_label = customtkinter.CTkLabel(
    sidebar_frame, text="Options", font=customtkinter.CTkFont(size=20, weight="bold"))
logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
home_button = customtkinter.CTkButton(
    sidebar_frame, text="Home", command=lambda: reset())
home_button.grid(row=1, column=0, padx=20, pady=10)
nosify_button = customtkinter.CTkButton(
    sidebar_frame, text="Nosify")
nosify_button.grid(row=2, column=0, padx=20, pady=10)
equalize_button = customtkinter.CTkButton(sidebar_frame, text="Equalizer")
equalize_button.grid(row=3, column=0, padx=20, pady=10)
home_button.configure(state="disabled")
nosify_button.configure(state="disabled")
equalize_button.configure(state="disabled")
# slider
slider_progressbar_frame = customtkinter.CTkFrame(app, fg_color="transparent")
slider_progressbar_frame.grid(
    row=8, column=5, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="sw")
slider_1 = customtkinter.CTkSlider(
    slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
slider_1.grid(row=3, column=0, padx=(200, 10), pady=(100, 10), sticky="sw")


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
    filename = customtkinter.filedialog.askopenfilename(
        filetypes=[(message, type)])
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
        # print(original_pgm.signal_to_noise(filtered.data))
    else:
        original_ppm = Ppm.create_from_file(file_data)
        original_ppm.create_file("original")
        image_file = Image.open("original.ppm").resize((1000, 720))

    image = ImageTk.PhotoImage(image_file)
    main_image_frame = tkinter.Label(image=image)
    main_image_frame.image = image
    main_image_frame.place(relx=0.3, rely=0.1, anchor=tkinter.NW)

    button.place_forget()
    radiobutton_frame.place_forget()
    home_button.configure(state="enabled")
    nosify_button.configure(state="enabled")
    nosify_button.configure(command=lambda: show_noisy(image_file))
    equalize_button.configure(state="enabled")


def show_noisy(image_file):
    image1 = ImageTk.PhotoImage(image_file)
    result_image_frame = tkinter.Label(image=image1)
    result_image_frame.place(relx=0.5, rely=0.1, anchor=tkinter.NW)


def choose_file_type(type):
    global image_type
    image_type = type


def reset():
    global original_pgm
    global original_ppm
    global image_type
    global main_image_frame
    global home_button

    main_image_frame.place_forget()
    home_button.configure(state="disabled")
    original_ppm = None
    original_pgm = None
    radiobutton_frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
    button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)


app.mainloop()
