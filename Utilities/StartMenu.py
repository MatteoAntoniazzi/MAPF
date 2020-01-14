from Utilities.SolverSettings import SolverSettings
from Utilities.start_simulation import *
from tkinter import *
from PIL import Image, ImageTk


class StartMenu:
    """
    This class represent the GUI start menu. On the GUI you can select the desired settings in order to visualize the
    MAPF simulation.
    """
    def __init__(self):
        """
        Initialize the start menu of the GUI
        """
        # Root: root frame for the gui
        self.root = Tk()
        self.root.maxsize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.root.resizable(False, False)

        # Variables
        self.map_images_list = []
        self.random_images_list = []
        self.buttons_list = []

        # GUI selectable variables
        self.selected_algorithm_var = StringVar()
        self.independence_detection_var = BooleanVar()
        self.selected_map_var = IntVar()
        self.selected_heuristic_var = StringVar()
        self.selected_obj_fun_var = StringVar()
        self.selected_goal_occupation_time = IntVar()
        self.selected_n_of_agents = IntVar()

        self.initialize_variables()

        # Frame: external frame inside the root
        self.frame = Frame(self.root, width=MAIN_WINDOW_WIDTH, height=MAIN_WINDOW_HEIGHT)
        self.frame.pack()

        # Settings Frame: placed in the left part of the Frame, it contains all the settings that can be selected
        self.settings_frame = Frame(self.frame, width=SETTINGS_FRAME_WIDTH, height=SETTINGS_FRAME_HEIGHT)
        self.settings_frame.pack_propagate(False)
        self.settings_frame.pack(fill=Y, expand=False, side=LEFT)

        # Simulation Frame: placed in the right part of the frame, it will display the MAPF simulation
        self.simulation_frame = Frame(self.frame, width=SIMULATION_FRAME_WIDTH_AND_HEIGHT,
                                      height=SIMULATION_FRAME_WIDTH_AND_HEIGHT, highlightbackground="#AAAAAA",
                                      highlightthickness=1)
        self.simulation_frame.pack_propagate(False)
        self.simulation_frame.pack(fill=None, expand=False, side=LEFT)

        # Choose Map Frame: placed in the left part of the Settings Frame, it contains all the possible maps
        self.choose_map_frame = Frame(self.settings_frame)
        self.choose_map_frame.pack(fill=Y, padx=10, pady=2, side=LEFT)

        # Choose Map Canvas: placed inside the Choose Map Frame
        self.choose_map_canvas = Canvas(self.choose_map_frame, width="115")
        self.choose_map_canvas.pack(fill=Y, padx=10, pady=2, side=LEFT)

        self.choose_map_frame_initialization()

        # Algorithm Settings Frame: placed in the right part of the Settings Frame, it contains all the settings
        self.algorithm_settings_frame = Frame(self.settings_frame)
        self.algorithm_settings_frame.pack(fill=Y, padx=20, pady=5, side=LEFT)

        self.algorithm_settings_frame_initialization()

        self.do_loop()

    def initialize_variables(self):
        """
        Initialize the widgets values.
        """
        self.selected_algorithm_var.set("Cooperative A*")
        self.independence_detection_var.set(False)
        self.selected_map_var.set(0)
        self.selected_heuristic_var.set("Manhattan")
        self.selected_obj_fun_var.set("SOC")
        self.selected_goal_occupation_time.set(1)
        self.selected_n_of_agents.set(5)

    def choose_map_frame_initialization(self):
        """
        Initialize the Choose Map Frame, which containing the list of all the possible selectable maps as Radiobuttons
        and with a scrollbar for a better visualization.
        """
        # Set up Scrollbar
        scrollbar = Scrollbar(self.choose_map_frame, command=self.choose_map_canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')

        self.choose_map_canvas.configure(yscrollcommand=scrollbar.set)
        self.choose_map_canvas.bind('<Configure>', self.on_configure)

        # Frame that will contains all the widgets
        frame = Frame(self.choose_map_canvas)
        self.choose_map_canvas.create_window((0, 0), window=frame, anchor='nw')

        for png_path in PNG_PATH_LIST:
            load = Image.open(png_path)
            load = load.resize((70, 70), Image.ANTIALIAS)
            self.map_images_list.append(ImageTk.PhotoImage(load))

        # Map Label
        lbl_title = Label(frame, text="MAP", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        # Maps Radiobuttons
        for i, img in enumerate(self.map_images_list):
            b = Radiobutton(frame, image=img, height=80, width=10, variable=self.selected_map_var, value=i)
            # WIDTH: 10 su Linux, 100 su Ubuntu
            self.buttons_list.append(b)
            b.pack(anchor=W)

    def on_configure(self, event):
        self.choose_map_canvas.configure(scrollregion=self.choose_map_canvas.bbox('all'))

    def algorithm_settings_frame_initialization(self):
        """
        Initialize the Algorithm Settings Frame, which containing the selection of the algorithm, the independence
        detection options, the heuristics, the permanence time and the number of agents
        """
        # Algorithm Label
        lbl_title = Label(self.algorithm_settings_frame, text="ALGORITHM", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        # Algorithm Radiobuttons
        for text, mode in ALGORITHMS_MODES:
            b = Radiobutton(self.algorithm_settings_frame, text=text, variable=self.selected_algorithm_var, value=mode)
            self.buttons_list.append(b)
            b.pack(anchor=W)

        # Independence Detection
        lbl_title = Label(self.algorithm_settings_frame, text="INDEPENDENCE DETECTION", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        # Independence Detection Checkbutton
        id_button = Checkbutton(self.algorithm_settings_frame, text="Independence Detection",
                                variable=self.independence_detection_var, onvalue=True, offvalue=False,
                                height=0, width=25)
        self.buttons_list.append(id_button)
        id_button.pack(anchor=W)

        # Heuristics Label
        lbl_title = Label(self.algorithm_settings_frame, text="HEURISTICS", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        # Heuristics Radiobuttons
        for text, mode in HEURISTICS_MODES:
            b = Radiobutton(self.algorithm_settings_frame, text=text, variable=self.selected_heuristic_var, value=mode)
            self.buttons_list.append(b)

            b.pack(anchor=W)

        # Permanence in Goal Label
        lbl_title = Label(self.algorithm_settings_frame, text="PERMANENCE IN GOAL", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        # Permanence in Goal Canvas
        permanence_in_goal_canvas = Canvas(self.algorithm_settings_frame)
        permanence_in_goal_canvas.pack()
        self.initialize_permanence_in_goal_canvas(permanence_in_goal_canvas)

        # Number of Agents Label
        lbl_title = Label(self.algorithm_settings_frame, text="N OF AGENTS", font=("Helvetica", 16), fg="purple")
        lbl_title.pack(anchor=W, ipady=10)

        # Number of Agents Canvas
        number_of_agents_canvas = Canvas(self.algorithm_settings_frame)
        number_of_agents_canvas.pack()
        self.initialize_n_of_agents_canvas(number_of_agents_canvas)

        # Prepare Button
        prepare_button = Button(self.algorithm_settings_frame, text="PREPARE", command=self.prepare_simulation_function)
        self.buttons_list.append(prepare_button)
        prepare_button.pack(anchor=E, pady=20)

    def initialize_permanence_in_goal_canvas(self, canvas):
        """
        Initialize the Permancence in Goal Canvas
        """
        # Load button images
        arrow_up_img = self.load_image("Images/arrow_up.png", (30, 30))
        arrow_down_img = self.load_image("Images/arrow_down.png", (30, 30))

        # Goal Occupation Time Up Button
        goal_occupation_time_up_button = Button(canvas, image=arrow_up_img,
                                                command=self.goal_occupation_time_up_button)
        goal_occupation_time_up_button.pack(side=RIGHT, padx=(0, 20))
        self.buttons_list.append(goal_occupation_time_up_button)

        # Goal Occupation Time Text
        goal_occupation_time_txt = Label(canvas, textvariable=self.selected_goal_occupation_time,
                                         justify=LEFT, font=("Lucida Console", 10))
        goal_occupation_time_txt.pack(side=RIGHT, padx=10)

        # Goal Occupation Time Down Button
        goal_occupation_time_down_button = Button(canvas, image=arrow_down_img,
                                                  command=self.goal_occupation_time_down_button)
        goal_occupation_time_down_button.pack(side=RIGHT, padx=(20, 0))
        self.buttons_list.append(goal_occupation_time_down_button)

    def initialize_n_of_agents_canvas(self, canvas):
        """
        Initialize the Number of Agents Canvas
        """
        # Load button images
        arrow_up_img = self.load_image("Images/arrow_up.png", (30, 30))
        arrow_down_img = self.load_image("Images/arrow_down.png", (30, 30))

        # Number of Agents Up Button
        n_of_agents_up_button = Button(canvas, image=arrow_up_img, command=self.n_of_agents_up_button)
        self.buttons_list.append(n_of_agents_up_button)
        n_of_agents_up_button.pack(side=RIGHT, padx=(0, 20))

        # Number of Agents Text
        n_of_agents_txt = Label(canvas, textvariable=self.selected_n_of_agents, justify=LEFT,
                                font=("Lucida Console", 10))
        n_of_agents_txt.pack(side=RIGHT, padx=10)

        # Number of Agents Down Button
        n_of_agents_down_button = Button(canvas, image=arrow_down_img, command=self.n_of_agents_down_button)
        n_of_agents_down_button.pack(side=RIGHT, padx=(20, 0))
        self.buttons_list.append(n_of_agents_down_button)

    def prepare_simulation_function(self):
        """
        Launch the simulation and display it on the Simulation Frame.
        """
        # Disable all the Buttons
        self.disable_settings_buttons()

        # Create an instance of the class SolverSettings
        solver_settings = SolverSettings(self.selected_heuristic_var.get(), self.selected_goal_occupation_time.get())

        # Prepare to show the simulation on the given frame
        prepare_simulation(self.simulation_frame, self.selected_algorithm_var.get(),
                           self.independence_detection_var.get(), self.selected_map_var.get(), solver_settings,
                           self.selected_obj_fun_var.get(), self.selected_n_of_agents.get())

        # Enable all the Buttons
        self.enable_settings_buttons()

    def goal_occupation_time_down_button(self):
        """
        Button function to decrement the goal occupation time
        """
        if self.selected_goal_occupation_time.get() > 1:
            self.selected_goal_occupation_time.set(self.selected_goal_occupation_time.get()-1)

    def goal_occupation_time_up_button(self):
        """
        Button function to increment the goal occupation time
        """
        self.selected_goal_occupation_time.set(self.selected_goal_occupation_time.get()+1)

    def n_of_agents_down_button(self):
        """
        Button function to decrement the number of agents
        """
        if self.selected_n_of_agents.get() > 1:
            self.selected_n_of_agents.set(self.selected_n_of_agents.get()-1)

    def n_of_agents_up_button(self):
        """
         Button function to increment the number of agents
         """
        self.selected_n_of_agents.set(self.selected_n_of_agents.get()+1)

    def enable_settings_buttons(self):
        """
        # Enable all the Buttons
        """
        for radio_button in self.buttons_list:
            radio_button.configure(state=NORMAL)

    def disable_settings_buttons(self):
        """
        Disable all the Buttons
        """
        for radio_button in self.buttons_list:
            radio_button.configure(state=DISABLED)

    def load_image(self, url, size):
        """
        Load an image. It is also stored in the random_images_list otherwise is not visualized on the GUI
        :param url: local path to the image
        :param size: desired image size
        :return: the image resized
        """
        load = Image.open(url)
        load = load.resize(size, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(load)
        self.random_images_list.append(img)
        return img

    def do_loop(self):
        self.frame.mainloop()
