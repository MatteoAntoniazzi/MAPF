from GUI.macros import *
from tkinter import *
import numpy as np
import PIL.ImageTk
import PIL.Image
import pathlib
import copy


class Visualize:
    """
    This class takes care of the visualization of the simulation of the MAPF solution.
    """

    def __init__(self, problem_instance, solver_settings, frame, paths, output_infos):
        """
        Initialize the frame.
        :param problem_instance:
        :param solver_settings:
        :param frame:
        :param paths:
        :param output_infos:
        """
        self._problem_instance = problem_instance
        self._solver_settings = solver_settings
        self._frame = frame
        self._paths = paths
        self._output_infos = output_infos
        self.random_images_list = []
        self._goals_list = [a.get_goal() for a in self._problem_instance.get_agents()]

        self.animation_speed = SPEED_1X
        self._frame_width, self._frame_height = get_frame_dimension(self._problem_instance.get_map().get_height(),
                                                                    self._problem_instance.get_map().get_width())

        # Visualize Frame: external frame
        self.visualize_frame = Frame(self._frame)
        self.visualize_frame.pack(ipady=5)

        # Visualize Canvas: inside the Visualize Frame
        self.visualize_canvas = Canvas(self.visualize_frame)
        self.visualize_canvas.pack(ipady=5)

        # Map Canvas: inside the Visualize Canvas
        self.map_canvas = Canvas(self.visualize_canvas, width=self._frame_width, height=self._frame_height)

        # Scrollbar Set Up
        self.set_up_scrollbar()

        # Infos and Buttons Canvas
        self.infos_and_buttons_canvas = Canvas(self.visualize_frame)
        self.infos_and_buttons_canvas.pack(fill=X)
        if self._output_infos is not None:
            self.infos_txt_var = StringVar()
            self.infos = Label(self.infos_and_buttons_canvas, textvariable=self.infos_txt_var, justify=LEFT,
                               padx=5, pady=2, font=("Lucida Console", 10))
            self.set_infos_txt()
            self.infos.pack(side=LEFT)

        # Quit Button
        self.quit_button = Button(self.infos_and_buttons_canvas, text="QUIT", command=self.quit_function)
        self.quit_button.pack(side=RIGHT)

        # Start Button
        self.start_button = Button(self.infos_and_buttons_canvas, text="START", command=self.start_function)
        self.start_button.pack(side=RIGHT)

        # Reset Button
        self.reset_button = Button(self.infos_and_buttons_canvas, text="RESET", command=self.reset_function)
        self.reset_button.configure(state=DISABLED)
        self.reset_button.pack(side=RIGHT)

        # Speed Regulation Widgets
        self.speed_txt_var = StringVar()
        self.initialize_speed_regulation_widgets()

        # Time Step Counter
        self.time_step_counter = -1
        self.time_step_txt_var = StringVar()
        self.time_step_txt = Label(self.infos_and_buttons_canvas, textvariable=self.time_step_txt_var, justify=LEFT,
                                   font=("Lucida Console", 10))
        self.time_step_txt_var.set("TS: " + str(self.time_step_counter))
        self.time_step_txt.pack(side=RIGHT, padx=2)

        # Initialize Variables for Map draiwing
        self.cell_h, self.cell_w = self.get_cell_size()
        self.dynamic_cell_h, self.dynamic_cell_w = self.cell_h, self.cell_w
        self.vis_cells = np.zeros((self._problem_instance.get_map().get_height(),
                                   self._problem_instance.get_map().get_width()), dtype=int)
        self.agents_ovals = []
        self.agents_colors = []
        self.text_list = []

        # For animation
        self.animating = True
        self._footsteps = False
        self.path_to_visit = []
        self.steps_count = [N_OF_STEPS] * len(self._problem_instance.get_agents())
        self.x_moves = [0] * len(self._problem_instance.get_agents())
        self.y_moves = [0] * len(self._problem_instance.get_agents())

    def initialize_window(self):
        """
        Initialize the Window with the World and the agents.
        """
        self.draw_world()
        self.draw_agents()
        if not self._paths:
            self.start_button.configure(state=DISABLED)

            self.map_canvas.create_text(self._frame_width / 2, self._frame_height / 2, justify=CENTER,
                                        font=("Purisa", get_font_dimension(self.dynamic_cell_w,
                                                                           self.dynamic_cell_h)),
                                        fill="Red", text="PATHS NOT COMPUTED\nThe program is not able to compute the "
                                                         "solution\nin the given timeout")
        self.do_loop()

    def set_up_scrollbar(self):
        """
        Set up the Scrollbar for the visualization of the map
        """
        xsb = Scrollbar(self.visualize_canvas, orient="horizontal", command=self.map_canvas.xview)
        ysb = Scrollbar(self.visualize_canvas, orient="vertical", command=self.map_canvas.yview)
        self.map_canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.map_canvas.configure(scrollregion=(0, 0, 100, 100))

        xsb.grid(row=1, column=0, sticky="ew")
        ysb.grid(row=0, column=1, sticky="ns")
        self.map_canvas.grid(row=0, column=0, sticky="nsew")
        self.map_canvas.grid_rowconfigure(0, weight=1)
        self.map_canvas.grid_columnconfigure(0, weight=1)

        # This is what enables using the mouse:
        self.map_canvas.bind("<ButtonPress-1>", self.move_start)
        self.map_canvas.bind("<B1-Motion>", self.move_move)
        # Linux scroll
        self.map_canvas.bind("<Button-4>", self.linux_zoom_p)
        self.map_canvas.bind("<Button-5>", self.linux_zoom_m)
        # Windows scroll
        self.map_canvas.bind("<MouseWheel>", self.windows_zoom)

    def move_start(self, event):
        self.map_canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.map_canvas.scan_dragto(event.x, event.y, gain=1)

    def linux_zoom_p(self, event):
        self.map_canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.map_canvas.configure(scrollregion=self.map_canvas.bbox("all"))
        self.dynamic_cell_w *= 1.1
        self.dynamic_cell_h *= 1.1
        for i, x in enumerate(self.x_moves):
            self.x_moves[i] *= 1.1
        for i, y in enumerate(self.y_moves):
            self.y_moves[i] *= 1.1
        for i, txt in enumerate(self.text_list):
            self.map_canvas.itemconfig(self.text_list[i], font=("Purisa", get_font_dimension(self.dynamic_cell_w, self.dynamic_cell_h)))

    def linux_zoom_m(self, event):
        self.map_canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.map_canvas.configure(scrollregion=self.map_canvas.bbox("all"))
        self.dynamic_cell_w *= 0.9
        self.dynamic_cell_h *= 0.9
        for i, x in enumerate(self.x_moves):
            self.x_moves[i] *= 0.9
        for i, y in enumerate(self.y_moves):
            self.y_moves[i] *= 0.9
        for i, txt in enumerate(self.text_list):
            self.map_canvas.itemconfig(self.text_list[i], font=("Purisa", get_font_dimension(self.dynamic_cell_w, self.dynamic_cell_h)))

    def windows_zoom(self, event):
        if event.delta > 0:
            self.linux_zoom_p(event)
        elif event.delta < 0:
            self.linux_zoom_m(event)

    def start_function(self):
        """
        Start Button behaviour: start the Path Animation.
        """
        self.start_button.configure(state=DISABLED)
        self.quit_button.configure(state=DISABLED)
        if self._paths is not None:
            # window.draw_paths(paths)
            self.draw_footsteps()
            self.start_animation(self._paths)

    def reset_function(self):
        """
        Reset Button behaviour: reset the Path Animation.
        """
        for widget in self._frame.winfo_children():
            widget.destroy()
        self.__init__(self._problem_instance, self._solver_settings, self._frame, self._paths, self._output_infos)
        self.draw_world()
        self.draw_agents()

    def quit_function(self):
        """
        Quit Button behaviour: close the Frame.
        """
        for widget in self._frame.winfo_children():
            widget.destroy()
        self._frame.quit()

    def initialize_speed_regulation_widgets(self):
        """
        Insert the speed widgets in the frame.
        """
        # Load Images
        root_path = pathlib.Path(__file__).parent

        speed_up_img = self.load_image(root_path / "Images/speed_up.png", (30, 30))
        speed_down_img = self.load_image(root_path / "Images/speed_down.png", (30, 30))

        # Speed Up Button
        speed_up_button = Button(self.infos_and_buttons_canvas, image=speed_up_img, command=self.speed_up_function)
        speed_up_button.pack(side=RIGHT, padx=(0, 20))

        # Speed Text
        speed_txt = Label(self.infos_and_buttons_canvas, textvariable=self.speed_txt_var, justify=LEFT,
                          font=("Lucida Console", 10))
        self.speed_txt_var.set("1X")
        speed_txt.pack(side=RIGHT, padx=10)

        # Speed Down Button
        speed_down_button = Button(self.infos_and_buttons_canvas, image=speed_down_img,
                                   command=self.speed_down_function)
        speed_down_button.pack(side=RIGHT, padx=(20, 0))

    def speed_down_function(self):
        """
        Decrease the speed of the animation.
        """
        if not self.animation_speed <= (SPEED_1X/10):
            self.animation_speed = self.animation_speed - SPEED_1X/10
            self.speed_txt_var.set(str(self.animation_speed/SPEED_1X)+"X")

    def speed_up_function(self):
        """
        Increase the speed of the animation.
        """
        if not self.animation_speed >= (SPEED_1X*1.9):
            self.animation_speed = self.animation_speed + SPEED_1X/10
            self.speed_txt_var.set(str(self.animation_speed/SPEED_1X)+"X")

    def set_infos_txt(self):
        """
        Set the text inside the infos with the output infos.
        """
        self.infos_txt_var.set("SUM OF COSTS: " + str(self._output_infos["sum_of_costs"]) + "\nMAKESPAN: " +
                               str(self._output_infos["makespan"]) + "\nN° OF GENERATED NODES: " +
                               str(self._output_infos["generated_nodes"]) + "\nN° OF EXPANDED NODES: " +
                               str(self._output_infos["expanded_nodes"]) + "\nCOMPUTATIONAL TIME: " +
                               str(round(self._output_infos["computation_time"], 2)))

    def draw_world(self):
        """
        Draw the Map World.
        """
        n_rows, n_cols = self._problem_instance.get_map().get_height(), self._problem_instance.get_map().get_width()
        for row in range(n_rows):
            for col in range(n_cols):
                self.vis_cells[row][col] = self.map_canvas.create_rectangle(FRAME_MARGIN + self.cell_w * col,
                                                                            FRAME_MARGIN + self.cell_h * row,
                                                                            FRAME_MARGIN + self.cell_w * (col + 1),
                                                                            FRAME_MARGIN + self.cell_h * (row + 1))
                if self._problem_instance.get_map().is_obstacle((col, row)):
                    self.map_canvas.itemconfig(self.vis_cells[row][col], fill='black', width=2)

    def draw_agents(self):
        """
        Draw the agents inside the map.
        """
        for i, a in enumerate(self._problem_instance.get_agents()):
            s_col, s_row = a.get_start()
            g_col, g_row = a.get_goal()

            agent_color = COLORS_LIST[i % len(COLORS_LIST)]
            # random_color = '#%02x%02x%02x' % tuple(np.random.choice(range(256), size=3))
            self.agents_colors.append(agent_color)
            self.agents_ovals.append(self.map_canvas.create_oval(FRAME_MARGIN + self.cell_w * s_col,
                                                                 FRAME_MARGIN + self.cell_h * s_row,
                                                                 FRAME_MARGIN + self.cell_w * (s_col + 1),
                                                                 FRAME_MARGIN + self.cell_h * (s_row + 1),
                                                                 outline='black', fill=agent_color))
            self.map_canvas.itemconfig(self.vis_cells[s_row][s_col], fill=agent_color, width=1.5)
            self.map_canvas.itemconfig(self.vis_cells[g_row][g_col], fill=agent_color, stipple="gray75", width=1.5)
            self.text_list.append(self.map_canvas.create_text(FRAME_MARGIN + self.cell_w * s_col + self.cell_w / 2,
                                                              FRAME_MARGIN + self.cell_h * s_row + self.cell_h / 2,
                                                              font=("Purisa", get_font_dimension(self.dynamic_cell_w,
                                                                                                 self.dynamic_cell_h)),
                                                              text="S"))
            self.text_list.append(self.map_canvas.create_text(FRAME_MARGIN + self.cell_w * g_col + self.cell_w / 2,
                                                              FRAME_MARGIN + self.cell_h * g_row + self.cell_h / 2,
                                                              font=("Purisa", get_font_dimension(self.dynamic_cell_w,
                                                                                                 self.dynamic_cell_h)),
                                                              text="G"))

    def draw_paths(self, paths):
        """
        Color the paths.
        """
        for i, path in enumerate(paths):
            color = self.agents_colors[i]
            for p in path[1:-1]:
                self.map_canvas.itemconfig(self.vis_cells[p[1]][p[0]], fill=color, stipple="", width=1.5)

    def start_animation(self, paths):
        """
        Start the Path Animation.
        :param paths: Paths to be displayed.
        """
        self.path_to_visit = copy.deepcopy(paths)  # In order to copy by value also the nested lists
        self._frame.after(2000, self.animation_function)

    def animation_function(self):
        """
        Function for the Path Animation.
        """
        if self.animating:
            self._frame.after(int(MAX_SPEED - self.animation_speed), self.animation_function)
            inc_time_step = True
            for i, agent in enumerate(self.agents_ovals):
                if self.steps_count[i] < N_OF_STEPS:
                    self.map_canvas.move(self.agents_ovals[i], self.x_moves[i], self.y_moves[i])
                    self.steps_count[i] += 1
                elif self.path_to_visit[i]:
                    if inc_time_step:
                        self.time_step_counter += 1
                        self.time_step_txt_var.set("TS: " + str(self.time_step_counter))

                        inc_time_step = False
                    current_position = self.path_to_visit[i].pop(0)
                    if self._footsteps:
                        color = self.agents_colors[i]
                        if current_position not in self._goals_list:  # To not overwrite others goals
                            self.map_canvas.itemconfig(self.vis_cells[current_position[1]][current_position[0]],
                                                       fill=color, stipple="", width=1.5)
                    if self.path_to_visit[i]:
                        next_position = self.path_to_visit[i][0]
                        self.x_moves[i] = float((next_position[0] - current_position[0]) * self.dynamic_cell_w) / N_OF_STEPS
                        self.y_moves[i] = float((next_position[1] - current_position[1]) * self.dynamic_cell_h) / N_OF_STEPS
                        self.map_canvas.move(self.agents_ovals[i], self.x_moves[i], self.y_moves[i])
                        self.steps_count[i] = 1
                if not self._solver_settings.stay_at_goal() and not self.path_to_visit[i]:
                    self.map_canvas.delete(self.agents_ovals[i])

            if not [i for i in self.path_to_visit if i]:  # For checking that all the arrays are empty
                self.animating = False

        else:
            # Animation ended
            self.start_button.configure(state=DISABLED)
            self.reset_button.configure(state=NORMAL)
            self.quit_button.configure(state=NORMAL)

    def draw_footsteps(self):
        """
        Set the footstep variable to True.
        """
        self._footsteps = True

    def get_cell_size(self):
        """
        Return the cell height and width
        """
        avail_h = self._frame_height - 2 * FRAME_MARGIN
        avail_w = self._frame_width - 2 * FRAME_MARGIN
        n_rows, n_cols = self._problem_instance.get_map().get_height(), self._problem_instance.get_map().get_width()
        cell_h = avail_h / n_rows
        cell_w = avail_w / n_cols
        return cell_h, cell_w

    def load_image(self, url, size):
        """
        Load an image. It is also stored in the random_images_list otherwise is not visualized on the GUIdd
        :param url: local path to the image
        :param size: desired image size
        :return: the image resized
        """
        load = PIL.Image.open(url)
        load = load.resize(size, PIL.Image.LANCZOS)
        img = PIL.ImageTk.PhotoImage(load)
        self.random_images_list.append(img)
        return img

    def do_loop(self):
        self._frame.mainloop()
