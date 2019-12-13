from tkinter import *
from PIL import Image, ImageTk
from Utilities.macros import *
from SearchBasedAlgorithms.AStarMultiAgent.SolverAStarMultiAgent import SolverAStarMultiAgent
from SearchBasedAlgorithms.CooperativeAStar.SolverCooperativeAStar import SolverCooperativeAStar
from SearchBasedAlgorithms.ConflictBasedSearch.SolverConflictBasedSearch import SolverConflictBasedSearch
from SearchBasedAlgorithms.IndependenceDetection.SolverIndependenceDetection import SolverIndependenceDetection
from SearchBasedAlgorithms.IncreasingCostTreeSearch.SolverIncreasingCostTreeSearch import SolverIncreasingCostTreeSearch
from SearchBasedAlgorithms.MStar.SolverMStar import SolverMStar


class StartMenu:
    def __init__(self):
        self.frame = Tk()
        self.images_list = []

        self.selected_algorithm_number = StringVar()
        self.selected_algorithm_number.set(0)  # initialize

        self.selected_map_number = StringVar()
        self.selected_map_number.set(0)  # initialize

        self.selected_obj_fun_number = StringVar()
        self.selected_obj_fun_number.set(0)  # initialize

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
            b = Radiobutton(canvas, text=text, variable=self.selected_algorithm_number, value=mode,
                            command=self.algorithm_selection)
            b.pack(anchor=W)

    def algorithm_selection(self):
        pass

    def initialize_center_part(self, canvas):

        for png_path in PNG_PATH_LIST:
            load = Image.open(png_path)
            load = load.resize((90, 90), Image.ANTIALIAS)
            self.images_list.append(ImageTk.PhotoImage(load))

        lbl_title = Label(canvas, text="MAP", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for i, img in enumerate(self.images_list):
            b = Radiobutton(canvas, image=img, height=100, width=100, variable=self.selected_map_number,
                            value=i, command=self.map_selection)
            b.pack(anchor=W)

    def map_selection(self):
        pass

    def initialize_right_part(self, canvas):
        lbl_title = Label(canvas, text="OBJECTIVE FUNCTION", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        for text, mode in OBJECTIVE_FUNCTION_MODES:
            b = Radiobutton(canvas, text=text, variable=self.selected_obj_fun_number, value=mode,
                            command=self.objective_function_selection)
            b.pack(anchor=W)

        self.label = Label(canvas)
        self.label.pack()

    def objective_function_selection(self):
        selection = "You selected the option " + str(self.selected_obj_fun_number.get())
        self.label.config(text=selection)

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


menu = StartMenu()
