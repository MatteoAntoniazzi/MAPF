from tkinter import *


class StartMenu:
    def __init__(self):
        self.frame = Tk()
        self.initialize_menu()
        self.do_loop()

    def do_nothing(self):
        filewin = Toplevel(self.frame)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def initialize_menu(self):
        w = Canvas()
        self.initialize_left_part(w)
        w.pack(padx=5, pady=10, side=LEFT)
        w = Label(self.frame, text="green", bg="green", fg="black")
        w.pack(padx=5, pady=20, side=LEFT)
        w = Label(self.frame, text="blue", bg="blue", fg="white")
        w.pack(padx=5, pady=20, side=LEFT)

    def initialize_left_part(self, canvas):
        MODES = [
            ("Cooperative A*", "1"),
            ("A*", "2"),
            ("A* with Operator Decomposition", "3"),
            ("Increasing Cost Tree Search", "RGB"),
            ("Conflict Based Search", "CMYK"),
            ("M*", "Mstar"),
        ]

        self.var = StringVar()
        self.var.set("2")  # initialize

        for text, mode in MODES:
            b = Radiobutton(canvas, text=text, variable=self.var, value=mode, command=self.selection)
            b.pack(anchor=W)

        self.label = Label(canvas)
        self.label.pack()

    def selection(self):
        selection = "You selected the option " + str(self.var.get())
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
