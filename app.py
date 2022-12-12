import os
import tkinter
import customtkinter
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import constant
from pgm import Pgm
from ppm import Ppm


class App:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.app = customtkinter.CTk()
        self.app.geometry("{0}x{1}+0+0".format(self.app.winfo_screenwidth(), self.app.winfo_screenheight()))
        self.app.title("ImageProcessingApp")

        self.original_pgm: Pgm | None = None
        self.noisy_pgm: Pgm | None = None
        self.equalized_pgm: Pgm | None = None
        self.filtered_pgm: Pgm | None = None
        self.original_ppm: Ppm | None = None
        self.current_pgm: Pgm | None = None
        self.post_threshold_ppm: Ppm | None = None
        self.post_and_threshold_ppm: Ppm | None = None
        self.post_or_threshold_ppm: Ppm | None = None
        self.current_second_pgm: Pgm | None = None
        self.current_image = None
        self.r = tkinter.StringVar(value="150")
        self.g = tkinter.StringVar(value="88")
        self.b = tkinter.StringVar(value="100")
        self.threshold_mode = 1

        self.main_image_frame = tkinter.Label()
        self.second_image_frame = tkinter.Label()
        self.third_image_frame = tkinter.Label()

        self.image_type = tkinter.IntVar(value=constant.PGM)
        self.avg_filter_value = tkinter.IntVar(value=0)
        self.median_filter_value = tkinter.IntVar(value=0)

        self.upload_button = customtkinter.CTkButton(master=self.app, text="Upload image", command=self.open_file)
        self.sidebar_frame = customtkinter.CTkFrame(self.app, width=140, corner_radius=0)
        self.radiobutton_frame = customtkinter.CTkFrame(self.app)
        self.original_frame = customtkinter.CTkFrame(self.app, corner_radius=0)
        self.second_frame = customtkinter.CTkFrame(self.app, corner_radius=0)

        self.home_button = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.reset)
        self.nosify_button = customtkinter.CTkButton(self.sidebar_frame, text="Nosify", command=self.show_noisy)
        self.equalize_button = customtkinter.CTkButton(self.sidebar_frame, text="Equalizer", command=self.show_equalize)
        self.threshold_button = customtkinter.CTkButton(self.sidebar_frame, text="Threshold",
                                                        command=self.open_threshold)
        self.and_threshold_button = customtkinter.CTkButton(self.sidebar_frame, text="And Threshold",
                                                            command=self.open_and_threshold)
        self.or_threshold_button = customtkinter.CTkButton(self.sidebar_frame, text="Or Threshold",
                                                           command=self.open_or_threshold)
        self.original_image_button = customtkinter.CTkButton(self.original_frame, text="Original image",
                                                             command=lambda: self.change_current_image(1))
        self.second_image_button = customtkinter.CTkButton(self.second_frame, text="Second image",
                                                           command=lambda: self.change_current_image(2))

        self.slider_average_frame = customtkinter.CTkFrame(self.app, fg_color="black")
        self.filter_slider_frame = customtkinter.CTkFrame(self.app, fg_color="transparent")
        self.avg_filter_slider = customtkinter.CTkSlider(self.slider_average_frame, from_=0, to=4,
                                                         number_of_steps=4,
                                                         command=self.change_average_filter_slider,
                                                         variable=self.avg_filter_value)
        self.avg_filter_label = customtkinter.CTkLabel(
            self.slider_average_frame, text="No Average filter",
            font=customtkinter.CTkFont(size=15))
        self.slider_median_frame = customtkinter.CTkFrame(self.app, fg_color="black")
        self.filter_slider_frame = customtkinter.CTkFrame(self.app, fg_color="transparent")
        self.median_filter_slider = customtkinter.CTkSlider(self.slider_median_frame, from_=0, to=4,
                                                            number_of_steps=4,
                                                            command=self.change_median_filter_slider,
                                                            variable=self.median_filter_value)
        self.median_filter_label = customtkinter.CTkLabel(
            self.slider_median_frame, text="No Median filter",
            font=customtkinter.CTkFont(size=15))

        self.snr_frame = customtkinter.CTkFrame(self.app, fg_color="transparent")
        self.snr_button = customtkinter.CTkButton(self.snr_frame, text="calculate snr",
                                                  command=lambda: self.show_snr())

        self.snr_label = customtkinter.CTkLabel(
            self.snr_frame, text="...", font=customtkinter.CTkFont(size=18))

        self.rgb_form_frame = customtkinter.CTkFrame(self.app, fg_color="black", width=400)
        self.r_input = customtkinter.CTkEntry(self.rgb_form_frame, placeholder_text="R", textvariable=self.r)
        self.g_input = customtkinter.CTkEntry(self.rgb_form_frame, placeholder_text="G", textvariable=self.g)
        self.b_input = customtkinter.CTkEntry(self.rgb_form_frame, placeholder_text="B", textvariable=self.b)

        self.r.trace_add('write', self.handle_rgb_change)
        self.g.trace_add('write', self.handle_rgb_change)
        self.b.trace_add('write', self.handle_rgb_change)

        self.init_upload_button_position()
        self.init_radio_button_content()
        self.init_radiobutton_position()
        self.init_sidebar_frame()
        self.init_filter_slider_position()
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
            self.init_original_frame_button()

        else:
            self.original_ppm = Ppm.create_from_file(file_data)
            self.original_ppm.create_file("original")
            image_file = Image.open("original.ppm").resize((600, 400))
            self.threshold_button.configure(state="enabled")
            self.and_threshold_button.configure(state="enabled")
            self.or_threshold_button.configure(state="enabled")

        self.current_pgm = self.original_pgm

        image = ImageTk.PhotoImage(image_file)
        self.main_image_frame = tkinter.Label(image=image)
        self.main_image_frame.image = image
        self.main_image_frame.place(relx=0.2, rely=0.1, anchor=tkinter.NW)
        self.main_image_frame.configure(highlightbackground="red", highlightthickness=4)

        self.upload_button.place_forget()
        self.radiobutton_frame.place_forget()
        self.home_button.configure(state="enabled")

    def show_noisy(self):
        self.second_image_frame.place_forget()
        self.second_image_frame.configure(highlightthickness=0)
        self.noisy_pgm = self.current_pgm.noisify_image()
        self.noisy_pgm.create_file("noisy")
        image = ImageTk.PhotoImage(Image.open("noisy.pgm").resize((600, 400)))
        self.second_image_frame = tkinter.Label(image=image)
        self.second_image_frame.image = image
        self.second_image_frame.place(relx=0.6, rely=0.1, anchor=tkinter.NW)
        self.second_image_button.grid(row=2, column=0)
        self.current_second_pgm = self.noisy_pgm
        self.init_second_frame_button()
        self.init_sliders_position()
        self.current_second_pgm = self.noisy_pgm
        self.change_current_image(2)

    def show_equalize(self):
        self.second_image_frame.place_forget()
        self.second_image_frame.configure(highlightthickness=0)
        self.equalized_pgm = self.current_pgm.equalize_image()
        self.equalized_pgm.create_file("equalize")
        image = ImageTk.PhotoImage(Image.open("equalize.pgm").resize((600, 400)))
        self.second_image_frame = tkinter.Label(image=image)
        self.second_image_frame.image = image
        self.second_image_frame.place(relx=0.6, rely=0.1, anchor=tkinter.NW)
        self.current_second_pgm = self.equalized_pgm
        self.init_second_frame_button()
        self.init_sliders_position()
        self.current_second_pgm = self.equalized_pgm
        self.change_current_image(2)

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
        self.home_button.grid(row=1, column=0, padx=20, pady=5)
        self.nosify_button.grid(row=2, column=0, padx=20, pady=5)
        self.equalize_button.grid(row=3, column=0, padx=20, pady=5)

        self.threshold_button.grid(row=4, column=0, padx=20, pady=5)
        self.and_threshold_button.grid(row=5, column=0, padx=20, pady=5)
        self.or_threshold_button.grid(row=6, column=0, padx=20, pady=5)

        self.nosify_button.configure(state="disabled")
        self.equalize_button.configure(state="disabled")
        self.threshold_button.configure(state="disabled")
        self.and_threshold_button.configure(state="disabled")
        self.or_threshold_button.configure(state="disabled")

    def init_filter_slider_position(self):
        self.avg_filter_slider.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="sw")
        self.avg_filter_label.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.median_filter_slider.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="sw")
        self.median_filter_label.grid(row=0, column=0, padx=10, pady=(10, 0))

    def init_sliders_position(self):
        self.slider_average_frame.grid(row=15, column=5, columnspan=2, padx=(80, 0), pady=(250, 0), sticky="n")
        self.slider_average_frame.grid_columnconfigure(0, weight=1)
        self.slider_average_frame.grid_rowconfigure(15, weight=1)
        self.slider_median_frame.grid(row=15, column=5, columnspan=2, padx=(80, 0), pady=(350, 0), sticky="n")
        self.slider_median_frame.grid_columnconfigure(0, weight=1)
        self.slider_median_frame.grid_rowconfigure(15, weight=1)

    def init_snr_button_position(self):
        self.snr_frame.grid(row=15, column=7, columnspan=5, padx=(10, 0), pady=(250, 0), sticky="n")
        self.snr_frame.grid_columnconfigure(0, weight=1)
        self.snr_frame.grid_rowconfigure(15, weight=1)
        self.snr_button.grid(row=4, column=0)

    def init_original_frame_button(self):
        self.original_frame.configure(width=250)
        self.original_frame.grid(row=0, column=10, sticky="e", padx=0)
        self.original_image_button.grid(row=1, column=5)

    def init_second_frame_button(self):
        self.second_frame.configure(width=250)
        self.second_frame.grid(row=0, column=30, sticky="e", padx=400)
        self.second_image_button.grid(row=1, column=5)

    def init_rgb_form_position(self):
        self.rgb_form_frame.grid(row=15, column=55, columnspan=55, padx=(450, 0), pady=(250, 0), sticky="nsew")
        self.r_input.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.g_input.grid(row=1, column=3, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.b_input.grid(row=1, column=5, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def reset(self):
        self.main_image_frame.place_forget()
        self.original_ppm = None
        self.original_pgm = None
        self.current_pgm = None
        self.filtered_pgm = None
        self.current_second_pgm = None
        self.noisy_pgm = None
        self.post_threshold_ppm = None
        self.post_and_threshold_ppm = None
        self.post_or_threshold_ppm = None
        self.main_image_frame.place_forget()
        self.second_image_frame.place_forget()
        self.third_image_frame.place_forget()
        self.third_image_frame.grid_forget()
        self.third_image_frame.pack_forget()
        self.slider_average_frame.grid_forget()
        self.slider_median_frame.grid_forget()
        self.snr_frame.grid_forget()
        self.original_frame.grid_forget()
        self.second_frame.grid_forget()
        self.nosify_button.configure(state="disabled")
        self.equalize_button.configure(state="disabled")
        self.threshold_button.configure(state="disabled")
        self.and_threshold_button.configure(state="disabled")
        self.or_threshold_button.configure(state="disabled")
        self.avg_filter_value.set(0)
        self.median_filter_value.set(0)
        self.rgb_form_frame.grid_forget()
        self.change_average_filter_slider(0)
        self.change_median_filter_slider(0)
        self.init_radiobutton_position()
        self.init_upload_button_position()

    def change_average_filter_slider(self, value):
        self.third_image_frame.place_forget()
        self.third_image_frame.grid_forget()
        self.third_image_frame.pack_forget()
        if value != 0:
            self.median_filter_value.set(0)
            self.change_median_filter_slider(0)
            self.filtered_pgm = self.current_pgm.apply_average_filter(int(2 * value + 1))
            f = Figure()
            a = f.add_subplot(111)
            a.imshow(self.filtered_pgm.data, cmap='gray')
            self.third_image_frame = customtkinter.CTkFrame(self.app, width=140, corner_radius=0)
            self.third_image_frame.place(relx=0.6, rely=0.50, anchor=tkinter.NW)
            canvas = FigureCanvasTkAgg(f, master=self.third_image_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
            self.avg_filter_label.configure(text="Average filter: " + str(int(self.avg_filter_value.get() * 2 + 1)))
            self.init_snr_button_position()

        else:
            self.avg_filter_label.configure(text="No Average filter")

    def change_median_filter_slider(self, value):
        self.third_image_frame.place_forget()
        self.third_image_frame.grid_forget()
        self.third_image_frame.pack_forget()
        if value != 0:
            self.avg_filter_value.set(0)
            self.change_average_filter_slider(0)
            self.filtered_pgm = self.current_pgm.apply_median(int(2 * value + 1))
            f = Figure()
            a = f.add_subplot(111)
            a.imshow(self.filtered_pgm.data, cmap='gray')
            self.third_image_frame = customtkinter.CTkFrame(self.app, width=140, corner_radius=0)
            self.third_image_frame.place(relx=0.6, rely=0.50, anchor=tkinter.NW)
            canvas = FigureCanvasTkAgg(f, master=self.third_image_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
            self.median_filter_label.configure(
                text="Median filter: " + str(int(self.median_filter_value.get() * 2 + 1)))
            self.init_snr_button_position()
        else:
            self.median_filter_label.configure(text="No Median filter")

    def change_current_image(self, value):
        self.current_image = value
        if self.current_image == 1:
            self.current_pgm = self.original_pgm
            self.main_image_frame.configure(highlightbackground="red", highlightthickness=4)
            self.second_image_frame.configure(highlightthickness=0)

        else:
            self.current_pgm = self.current_second_pgm
            self.main_image_frame.configure(highlightthickness=0)
            self.second_image_frame.configure(highlightbackground="red", highlightthickness=4)

    def show_snr(self):
        self.snr_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.snr_label.configure(text=str(self.current_pgm.signal_to_noise(self.filtered_pgm.data)))

    def open_threshold(self):
        self.init_rgb_form_position()
        self.threshold_mode = 1
        self.show_threshold()

    def open_and_threshold(self):
        self.init_rgb_form_position()
        self.threshold_mode = 2
        self.show_and_threshold()

    def open_or_threshold(self):
        self.init_rgb_form_position()
        self.threshold_mode = 3
        self.show_or_threshold()

    def show_threshold(self):
        self.second_image_frame.place_forget()
        self.post_threshold_ppm = self.original_ppm.threshold(int(self.r.get()), int(self.g.get()), int(self.b.get()))
        self.post_threshold_ppm.create_file("threshold")
        image = ImageTk.PhotoImage(Image.open("threshold.ppm").resize((600, 400)))
        self.second_image_frame = tkinter.Label(image=image)
        self.second_image_frame.image = image
        self.second_image_frame.place(relx=0.6, rely=0.1, anchor=tkinter.NW)

    def show_and_threshold(self):
        self.second_image_frame.place_forget()
        self.post_and_threshold_ppm = self.original_ppm.and_threshold(int(self.r.get()), int(self.g.get()),
                                                                      int(self.b.get()))
        self.post_and_threshold_ppm.create_file("and_threshold")
        image = ImageTk.PhotoImage(Image.open("and_threshold.ppm").resize((600, 400)))
        self.second_image_frame = tkinter.Label(image=image)
        self.second_image_frame.image = image
        self.second_image_frame.place(relx=0.6, rely=0.1, anchor=tkinter.NW)

    def show_or_threshold(self):
        self.second_image_frame.place_forget()
        self.post_or_threshold_ppm = self.original_ppm.or_threshold(int(self.r.get()), int(self.g.get()),
                                                                    int(self.b.get()))
        self.post_or_threshold_ppm.create_file("or_threshold")
        image = ImageTk.PhotoImage(Image.open("or_threshold.ppm").resize((600, 400)))
        self.second_image_frame = tkinter.Label(image=image)
        self.second_image_frame.image = image
        self.second_image_frame.place(relx=0.6, rely=0.1, anchor=tkinter.NW)

    def handle_rgb_change(self, x, y, z):
        self.get_rgb()
        if self.threshold_mode == 1:
            self.show_threshold()
        elif self.threshold_mode == 2:
            self.show_and_threshold()
        else:
            self.show_or_threshold()

    def get_rgb(self):
        if self.r.get().isnumeric():
            if int(self.r.get()) < 0:
                self.r.set("0")
            elif int(self.r.get()) > 255:
                self.r.set("255")
        else:
            self.r.set("0")

        if self.g.get().isnumeric():
            if int(self.g.get()) < 0:
                self.g.set("0")
            elif int(self.g.get()) > 255:
                self.g.set("255")
        else:
            self.g.set("0")

        if self.b.get().isnumeric():
            if int(self.b.get()) < 0:
                self.b.set("0")
            elif int(self.b.get()) > 255:
                self.b.set("255")
        else:
            self.b.set("0")

        return int(self.r.get()), int(self.g.get()), int(self.b.get())


App()
