from tkinter import *

import PIL
from PIL import Image, ImageTk

from Utilities.SolverSettings import SolverSettings
from Utilities.macros import *
from Utilities.start_simulation import *


class StartMenu:
    def __init__(self):
        # ROOT
        self.root = Tk()
        self.root.maxsize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        # EXTERNAL FRAME
        self.frame = Frame(self.root, width=MAIN_WINDOW_WIDTH, height=MAIN_WINDOW_HEIGHT)
        self.frame.pack()

        # SETTINGS FRAME
        self.settings_frame = Frame(self.frame, width=SETTINGS_FRAME_WIDTH, height=SETTINGS_FRAME_HEIGHT)
        self.settings_frame.pack_propagate(False)
        self.settings_frame.pack(fill=Y, expand=False, side=LEFT)

        # SIMULATION FRAME
        self.simulation_frame = Frame(self.frame, width=SIMULATION_FRAME_WIDTH_AND_HEIGHT,
                                      height=SIMULATION_FRAME_WIDTH_AND_HEIGHT, highlightbackground="#AAAAAA",
                                      highlightthickness=1)
        self.simulation_frame.pack_propagate(False)
        self.simulation_frame.pack(fill=None, expand=False, side=LEFT)

        self.choose_map_frame = Frame(self.settings_frame)
        self.choose_map_frame.pack(fill=Y, padx=10, pady=2, side=LEFT)

        self.choose_map_canvas = Canvas(self.choose_map_frame, width="115")
        self.choose_map_canvas.pack(fill=Y, padx=10, pady=2, side=LEFT)

        self.images_list = []

        self.selected_algorithm_var = StringVar()
        self.selected_algorithm_var.set("Cooperative A*")  # initialize

        self.independence_detection_var = BooleanVar()
        self.independence_detection_var.set(False)  # initialize

        self.selected_map_var = IntVar()
        self.selected_map_var.set(0)  # initialize

        self.selected_heuristic_var = StringVar()
        self.selected_heuristic_var.set("Manhattan")  # initialize

        self.selected_obj_fun_var = StringVar()
        self.selected_obj_fun_var.set("SOC")  # initialize

        self.selected_goal_occupation_time = IntVar()
        self.selected_goal_occupation_time.set(1)

        self.buttons_list = []

        self.initialize_menu_bar()
        self.initialize_menu()
        self.do_loop()

    def do_nothing(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def initialize_menu(self):
        self.first_column_frame_initialization()

        w = Frame(self.settings_frame)
        self.second_column_frame_initialization(w)
        w.pack(fill=Y, padx=20, pady=5, side=LEFT)

        # w = Frame(self.settings_frame)
        # self.initialize_right_part(w)
        # w.pack(fill=Y, padx=20, pady=5, side=LEFT)

    def first_column_frame_initialization(self):

        scrollbar = Scrollbar(self.choose_map_frame, command=self.choose_map_canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')

        self.choose_map_canvas.configure(yscrollcommand=scrollbar.set)

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.choose_map_canvas.bind('<Configure>', self.on_configure)

        # --- put frame in canvas ---

        frame = Frame(self.choose_map_canvas)
        self.choose_map_canvas.create_window((0, 0), window=frame, anchor='nw')

        for png_path in PNG_PATH_LIST:
            load = Image.open(png_path)
            load = load.resize((70, 70), Image.ANTIALIAS)
            self.images_list.append(ImageTk.PhotoImage(load))

        lbl_title = Label(frame, text="MAP", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for i, img in enumerate(self.images_list):
            b = Radiobutton(frame, image=img, height=80, width=10, variable=self.selected_map_var, value=i)
            # WIDTH: 10 su Linux, 100 su Ubuntu
            self.buttons_list.append(b)

            b.pack(anchor=W)

    def on_configure(self, event):
        self.choose_map_canvas.configure(scrollregion=self.choose_map_canvas.bbox('all'))

    def second_column_frame_initialization(self, frame):
        lbl_title = Label(frame, text="ALGORITHM", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for text, mode in ALGORITHMS_MODES:
            b = Radiobutton(frame, text=text, variable=self.selected_algorithm_var, value=mode)
            self.buttons_list.append(b)
            b.pack(anchor=W)

        lbl_title = Label(frame, text="INDEPENDENCE DETECTION", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        id_button = Checkbutton(frame, text="Independence Detection", variable=self.independence_detection_var,
                                onvalue=True, offvalue=False, height=0, width=25)
        self.buttons_list.append(id_button)
        id_button.pack(anchor=W)

        lbl_title = Label(frame, text="HEURISTIC", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for text, mode in HEURISTICS_MODES:
            b = Radiobutton(frame, text=text, variable=self.selected_heuristic_var, value=mode)
            self.buttons_list.append(b)

            b.pack(anchor=W)

        lbl_title = Label(frame, text="PERMANENCE IN GOAL", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        permanence_in_goal_canvas = Canvas(frame)
        permanence_in_goal_canvas.pack()

        load = PIL.Image.open("Images/speed_up.png")
        load = load.resize((30, 30), PIL.Image.ANTIALIAS)
        self.goal_occupation_time_up_img = PIL.ImageTk.PhotoImage(load)
        self.goal_occupation_time_up_button = Button(permanence_in_goal_canvas, image=self.goal_occupation_time_up_img,
                                                     command=self.goal_occupation_time_up_button)
        self.goal_occupation_time_up_button.pack(side=RIGHT, padx=(0, 20))

        self.goal_occupation_time_txt = Label(permanence_in_goal_canvas, textvariable=self.selected_goal_occupation_time, justify=LEFT,
                                              font=("Lucida Console", 10))
        self.goal_occupation_time_txt.pack(side=RIGHT, padx=10)

        load = PIL.Image.open("Images/speed_down.png")
        load = load.resize((30, 30), PIL.Image.ANTIALIAS)
        self.goal_occupation_time_down_img = PIL.ImageTk.PhotoImage(load)
        self.goal_occupation_time_down_button = Button(permanence_in_goal_canvas, image=self.goal_occupation_time_down_img,
                                                       command=self.goal_occupation_time_down_button)
        self.goal_occupation_time_down_button.pack(side=RIGHT, padx=(20, 0))

        prepare_button = Button(frame, text="PREPARE", command=self.prepare_simulation_function)
        prepare_button.pack(anchor=E, pady=20)

    # def initialize_right_part(self, frame):
    #     lbl_title = Label(frame, text="OBJECTIVE FUNCTION", font=("Helvetica", 16), fg="purple")
    #     lbl_title.pack(anchor=W, ipady=10)
    #
    #     for text, mode in OBJECTIVE_FUNCTION_MODES:
    #         b = Radiobutton(frame, text=text, variable=self.selected_obj_fun_var, value=mode)
    #         self.buttons_list.append(b)
    #         b.pack(anchor=W)

    def goal_occupation_time_down_button(self):
        if self.selected_goal_occupation_time.get() > 1:
            self.selected_goal_occupation_time.set(self.selected_goal_occupation_time.get()-1)

    def goal_occupation_time_up_button(self):
        self.selected_goal_occupation_time.set(self.selected_goal_occupation_time.get()+1)

    def prepare_simulation_function(self):
        print(self.selected_algorithm_var.get(), self.independence_detection_var.get(),
              self.selected_map_var.get(), self.selected_heuristic_var.get(),
              self.selected_obj_fun_var.get())
        for radio_button in self.buttons_list:
            radio_button.configure(state=DISABLED)
        solver_settings = SolverSettings(heuristics=self.selected_heuristic_var.get(),
                                         goal_occupation_time=self.selected_goal_occupation_time.get())
        prepare_simulation(self, self.simulation_frame, self.selected_algorithm_var.get(),
                           self.independence_detection_var.get(), self.selected_map_var.get(), solver_settings,
                           self.selected_obj_fun_var.get())

    def initialize_menu_bar(self):
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.do_nothing)
        filemenu.add_command(label="Open", command=self.do_nothing)
        filemenu.add_command(label="Save", command=self.do_nothing)
        filemenu.add_command(label="Save as...", command=self.do_nothing)
        filemenu.add_command(label="Close", command=self.do_nothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.do_nothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.do_nothing)
        editmenu.add_command(label="Copy", command=self.do_nothing)
        editmenu.add_command(label="Paste", command=self.do_nothing)
        editmenu.add_command(label="Delete", command=self.do_nothing)
        editmenu.add_command(label="Select All", command=self.do_nothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.do_nothing)
        helpmenu.add_command(label="About...", command=self.do_nothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def enable_settings_buttons(self):
        for radio_button in self.buttons_list:
            radio_button.configure(state=NORMAL)

    def do_loop(self):
        self.frame.mainloop()
