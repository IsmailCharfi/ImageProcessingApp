import os
import tkinter
import customtkinter
from PIL import Image, ImageTk
import constant
from pgm import Pgm
from ppm import Ppm


class App:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.app = customtkinter.CTk()
        self.app.geometry(f"{800}x{600}")
        self.app.title("ImageProcessingApp")

        self.original_pgm: Pgm | None = None
        self.noisy_pgm: Pgm | None = None
        self.filtered_pgm: Pgm | None = None
        self.original_ppm: Ppm | None = None
        self.main_image_frame = tkinter.Label()
        self.second_image_frame = tkinter.Label()
        self.third_image_frame = tkinter.Label()
        self.image_type = tkinter.IntVar(value=constant.PGM)
        self.avg_filter_value = tkinter.IntVar(value=3)

        self.upload_button = customtkinter.CTkButton(master=self.app, text="Upload image", command=self.open_file)
        self.sidebar_frame = customtkinter.CTkFrame(self.app, width=140, corner_radius=0)
        self.radiobutton_frame = customtkinter.CTkFrame(self.app)
        self.home_button = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.reset)
        self.nosify_button = customtkinter.CTkButton(self.sidebar_frame, text="Nosify")
        self.equalize_button = customtkinter.CTkButton(self.sidebar_frame, text="Equalizer")
        self.filter_slider_frame = customtkinter.CTkFrame(self.app, fg_color="transparent")
        self.filter_slider = customtkinter.CTkSlider(self.filter_slider_frame, from_=1, to=4, number_of_steps=3,
                                                     command=self.change_filter_slider)
        self.init_upload_button_position()
        self.init_radio_button_content()
        self.init_radiobutton_position()
        self.init_sidebar_frame()
        self.init_filter_slider()

        self.app.mainloop()

    def open_file(self):
        message = ""
        _type = ""
        _image_type = self.image_type.get()
        if _image_type == constant.PGM:
            message = 'Pgm File'
            _type = '*.pgm'
        elif _image_type == constant.PPM:
            message = 'Ppm File'
            _type = '*.ppm'
        filename = customtkinter.filedialog.askopenfilename(filetypes=[(message, _type)])
        file = open(filename, "r")
        file_data = file.readlines()
        file.close()

        if _image_type == constant.PGM:
            self.original_pgm = Pgm.create_from_file(file_data)
            self.original_pgm.create_file("original")
            image_file = Image.open("original.pgm").resize((600, 400))
            self.nosify_button.configure(state="enabled")
            self.equalize_button.configure(state="enabled")

        else:
            self.original_ppm = Ppm.create_from_file(file_data)
            self.original_ppm.create_file("original")
            image_file = Image.open("original.ppm").resize((600, 400))

        image = ImageTk.PhotoImage(image_file)
        self.main_image_frame = tkinter.Label(image=image)
        self.main_image_frame.image = image
        self.main_image_frame.place(relx=0.2, rely=0.1, anchor=tkinter.NW)

        self.upload_button.place_forget()
        self.radiobutton_frame.place_forget()
        self.home_button.configure(state="enabled")

        self.nosify_button.configure(command=self.show_noisy)

    def show_noisy(self):
        self.noisy_pgm = self.original_pgm.noisify_image()
        self.noisy_pgm.create_file("noisy")
        image = ImageTk.PhotoImage(Image.open("noisy.pgm").resize((600, 400)))
        self.second_image_frame = tkinter.Label(image=image)
        self.second_image_frame.image = image
        self.second_image_frame.place(relx=0.6, rely=0.1, anchor=tkinter.NW)

    def init_upload_button_position(self):
        self.upload_button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

    def init_radio_button_content(self):
        label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Image file type:")
        label_radio_group.grid(row=0, column=2, columnspan=1, padx=50, pady=10, sticky="")
        pgm_radio_button = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame, variable=self.image_type, value=constant.PGM, text="pgm")
        pgm_radio_button.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        ppm_radio_button = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame, variable=self.image_type, value=constant.PPM, text="ppm")
        ppm_radio_button.grid(row=2, column=2, pady=10, padx=20, sticky="n")

    def init_radiobutton_position(self):
        self.radiobutton_frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

    def init_sidebar_frame(self):
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.home_button.grid(row=1, column=0, padx=20, pady=10)
        self.nosify_button.grid(row=2, column=0, padx=20, pady=10)
        self.equalize_button.grid(row=3, column=0, padx=20, pady=10)
        self.home_button.configure(state="disabled")
        self.nosify_button.configure(state="disabled")
        self.equalize_button.configure(state="disabled")

    def init_filter_slider(self):
        self.filter_slider_frame.grid(
            row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="sw")
        self.filter_slider.grid(row=1, column=0, padx=(20, 10), pady=(100, 10), sticky="sw")

    def reset(self):
        self.main_image_frame.place_forget()
        self.home_button.configure(state="disabled")
        self.original_ppm = None
        self.original_pgm = None
        self.init_radiobutton_position()
        self.init_upload_button_position()

    def change_filter_slider(self, value):
        self.filtered_pgm = self.noisy_pgm.apply_average_filter(5)
        self.filtered_pgm.create_file("filtered")
        image = ImageTk.PhotoImage(Image.open("filtered.pgm"))
        self.third_image_frame = tkinter.Label(image=image)
        self.third_image_frame.image = image
        self.third_image_frame.place(relx=0.8, rely=0.1, anchor=tkinter.NW)


App()
