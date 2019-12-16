from tkinter import *
from PIL import Image, ImageTk
from Utilities.macros import *
from Utilities.start_simulation import *


class StartMenu:
    def __init__(self):
        self.frame = Tk()
        self.images_list = []

        self.selected_algorithm_var = StringVar()
        self.selected_algorithm_var.set("Cooperative A*")  # initialize

        self.independence_detection_var = BooleanVar()
        self.independence_detection_var.set(False)  # initialize

        self.selected_map_var = IntVar()
        self.selected_map_var.set(0)  # initialize

        self.selected_heuristic_var = StringVar()
        self.selected_heuristic_var.set("Manhattan")  # initialize

        self.selected_obj_fun_var = IntVar()
        self.selected_obj_fun_var.set(0)  # initialize

        self.initialize_menu_bar()
        self.initialize_menu()
        self.do_loop()

    def do_nothing(self):
        filewin = Toplevel(self.frame)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def initialize_menu(self):
        w = Canvas()
        self.initialize_left_part(w)
        w.pack(fill=Y, padx=20, pady=5, side=LEFT)

        w = Canvas()
        self.initialize_center_part(w)
        w.pack(fill=Y, padx=20, pady=5, side=LEFT)

        w = Canvas()
        self.initialize_right_part(w)
        w.pack(fill=Y, padx=20, pady=5, side=LEFT)

    def initialize_left_part(self, canvas):

        lbl_title = Label(canvas, text="ALGORITHM", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for text, mode in ALGORITHMS_MODES:
            b = Radiobutton(canvas, text=text, variable=self.selected_algorithm_var, value=mode,
                            command=self.algorithm_selection)
            b.pack(anchor=W)

        lbl_title = Label(canvas, text="INDEPENDENCE DETECTION", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        id_button = Checkbutton(canvas, text="Independence Detection", variable=self.independence_detection_var,
                                onvalue=True, offvalue=False, height=0, width=25, command=self.independence_selection)
        id_button.pack(anchor=W)

    def algorithm_selection(self):
        print(self.selected_algorithm_var.get())

    def independence_selection(self):
        print(self.independence_detection_var.get())

    def initialize_center_part(self, canvas):

        for png_path in PNG_PATH_LIST:
            load = Image.open(png_path)
            load = load.resize((90, 90), Image.ANTIALIAS)
            self.images_list.append(ImageTk.PhotoImage(load))

        lbl_title = Label(canvas, text="MAP", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for i, img in enumerate(self.images_list):
            b = Radiobutton(canvas, image=img, height=100, width=10, variable=self.selected_map_var,
                            value=i, command=self.map_selection)  # WIDTH: 10 su Linux, 100 su Ubuntu
            b.pack(anchor=W)

    def map_selection(self):
        pass

    def initialize_right_part(self, canvas):
        lbl_title = Label(canvas, text="HEURISTIC", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for text, mode in HEURISTICS_MODES:
            b = Radiobutton(canvas, text=text, variable=self.selected_heuristic_var, value=mode)
            b.pack(anchor=W)

        lbl_title = Label(canvas, text="OBJECTIVE FUNCTION", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for text, mode in OBJECTIVE_FUNCTION_MODES:
            b = Radiobutton(canvas, text=text, variable=self.selected_obj_fun_var, value=mode)
            b.pack(anchor=W)

        start_button = Button(canvas, text="START", command=self.start_function)

        start_button.pack(anchor=E)

    def start_function(self):
        start_simulation(self.selected_algorithm_var.get(), self.independence_detection_var.get(),
                         self.selected_map_var.get(), self.selected_heuristic_var.get(),
                         self.selected_obj_fun_var.get())

    def initialize_menu_bar(self):
        menubar = Menu(self.frame)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.do_nothing)
        filemenu.add_command(label="Open", command=self.do_nothing)
        filemenu.add_command(label="Save", command=self.do_nothing)
        filemenu.add_command(label="Save as...", command=self.do_nothing)
        filemenu.add_command(label="Close", command=self.do_nothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.frame.quit)
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

        self.frame.config(menu=menubar)

    def do_loop(self):
        self.frame.mainloop()
