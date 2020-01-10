import numpy as np
import PIL.Image, PIL.ImageTk
from Utilities.macros import *
from tkinter import *
import copy


class Visualize:
    def __init__(self, problem_instance, start_menu, frame, map, agents, paths, output_infos):
        self._problem_instance = problem_instance
        self._map = map
        self._agents = agents
        self._paths = paths
        self._output_infos = output_infos
        self.frame = frame
        self.start_menu = start_menu

        self.animation_speed = SPEED_1X

        self._frame_width, self._frame_height = get_frame_dimension(map.get_height(), map.get_width())

        self.visualize_frame = Frame(self.frame)
        self.visualize_frame.pack(ipady=5)

        self.visualize_canvas = Canvas(self.visualize_frame)
        self.visualize_canvas.pack(ipady=5)

        self.map_canvas = Canvas(self.visualize_canvas, width=self._frame_width, height=self._frame_height)

        self.xsb = Scrollbar(self.visualize_canvas, orient="horizontal", command=self.map_canvas.xview)
        self.ysb = Scrollbar(self.visualize_canvas, orient="vertical", command=self.map_canvas.yview)
        self.map_canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.map_canvas.configure(scrollregion=(0, 0, 100, 100))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.map_canvas.grid(row=0, column=0, sticky="nsew")
        self.map_canvas.grid_rowconfigure(0, weight=1)
        self.map_canvas.grid_columnconfigure(0, weight=1)

        # This is what enables using the mouse:
        self.map_canvas.bind("<ButtonPress-1>", self.move_start)
        self.map_canvas.bind("<B1-Motion>", self.move_move)
        # linux scroll
        self.map_canvas.bind("<Button-4>", self.zoomerP)
        self.map_canvas.bind("<Button-5>", self.zoomerM)
        # windows scroll
        self.map_canvas.bind("<MouseWheel>", self.zoomer)

        self.infos_and_buttons_canvas = Canvas(self.visualize_frame)
        self.infos_and_buttons_canvas.pack(fill=X)
        self.infos_txt_var = StringVar()
        self.infos = Label(self.infos_and_buttons_canvas, textvariable=self.infos_txt_var, justify=LEFT, padx=5, pady=2,
                           font=("Lucida Console", 10))
        self.infos_txt_var.set("\n\n")
        self.set_infos_txt()
        self.infos.pack(side=LEFT)

        self.quit_button = Button(self.infos_and_buttons_canvas, text="QUIT", command=self.quit_function)
        self.quit_button.pack(side=RIGHT)

        self.start_button = Button(self.infos_and_buttons_canvas, text="START", command=self.start_function)
        self.start_button.pack(side=RIGHT)

        self.reset_button = Button(self.infos_and_buttons_canvas, text="RESET", command=self.reset_function)
        self.reset_button.configure(state=DISABLED)
        self.reset_button.pack(side=RIGHT)

        load = PIL.Image.open("Images/speed_up.png")
        load = load.resize((30, 30), PIL.Image.ANTIALIAS)
        self.speed_up_img = PIL.ImageTk.PhotoImage(load)
        self.speed_up_button = Button(self.infos_and_buttons_canvas, image=self.speed_up_img,
                                      command=self.speed_up_button)
        self.speed_up_button.pack(side=RIGHT, padx=(0, 20))

        self.speed_txt_var = StringVar()
        self.speed_txt = Label(self.infos_and_buttons_canvas, textvariable=self.speed_txt_var, justify=LEFT,
                           font=("Lucida Console", 10))
        self.speed_txt_var.set("1X")
        self.speed_txt.pack(side=RIGHT, padx=10)

        load = PIL.Image.open("Images/speed_down.png")
        load = load.resize((30, 30), PIL.Image.ANTIALIAS)
        self.speed_down_img = PIL.ImageTk.PhotoImage(load)
        self.speed_down_button = Button(self.infos_and_buttons_canvas, image=self.speed_down_img,
                                        command=self.speed_down_button)
        self.speed_down_button.pack(side=RIGHT, padx=(20, 0))

        self.time_step_counter = -1
        self.time_step_txt_var = StringVar()
        self.time_step_txt = Label(self.infos_and_buttons_canvas, textvariable=self.time_step_txt_var, justify=LEFT,
                                   font=("Lucida Console", 10))
        self.time_step_txt_var.set("TS: " + str(self.time_step_counter))
        self.time_step_txt.pack(side=RIGHT, padx=2)

        self.cell_h, self.cell_w = self.get_cell_size()
        self.dinamic_cell_h, self.dinamic_cell_w = self.cell_h, self.cell_w
        self.vis_cells = np.zeros((self._map.get_height(), self._map.get_width()), dtype=int)
        self.agents_ovals = []
        self.agents_colors = []
        self.text_list = []

        # For animation
        self.animating = True
        self._footsteps = False
        self.path_to_visit = []
        self.steps_count = [N_OF_STEPS] * len(self._agents)
        self.x_moves = [0] * len(self._agents)
        self.y_moves = [0] * len(self._agents)

    # move
    def move_start(self, event):
        self.map_canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.map_canvas.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    def zoomer(self, event):
        if (event.delta > 0):
            self.map_canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.map_canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.map_canvas.configure(scrollregion=self.map_canvas.bbox("all"))

    # linux zoom
    def zoomerP(self, event):
        self.map_canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.map_canvas.configure(scrollregion=self.map_canvas.bbox("all"))
        self.dinamic_cell_w *= 1.1
        self.dinamic_cell_h *= 1.1

        for i, x in enumerate(self.x_moves):
            self.x_moves[i] *= 1.1

        for i, y in enumerate(self.y_moves):
            self.y_moves[i] *= 1.1

        for i, txt in enumerate(self.text_list):
            self.map_canvas.itemconfig(self.text_list[i], font=("Purisa", get_font_dimension(self.dinamic_cell_w, self.dinamic_cell_h)))

    def zoomerM(self, event):
        self.map_canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.map_canvas.configure(scrollregion=self.map_canvas.bbox("all"))
        self.dinamic_cell_w *= 0.9
        self.dinamic_cell_h *= 0.9

        for i, x in enumerate(self.x_moves):
            self.x_moves[i] *= 0.9

        for i, y in enumerate(self.y_moves):
            self.y_moves[i] *= 0.9

        for i, txt in enumerate(self.text_list):
            self.map_canvas.itemconfig(self.text_list[i], font=("Purisa", get_font_dimension(self.dinamic_cell_w, self.dinamic_cell_h)))

    def initialize_window(self):
        self.draw_world()
        self.draw_agents()
        self.do_loop()

    def speed_down_button(self):
        if not self.animation_speed <= (SPEED_1X/10):
            self.animation_speed = self.animation_speed - SPEED_1X/10
            self.speed_txt_var.set(str(self.animation_speed/SPEED_1X)+"X")

    def speed_up_button(self):
        if not self.animation_speed >= (SPEED_1X*2):
            self.animation_speed = self.animation_speed + SPEED_1X/10
            self.speed_txt_var.set(str(self.animation_speed/SPEED_1X)+"X")

    def start_function(self):
        self.start_button.configure(state=DISABLED)
        self.quit_button.configure(state=DISABLED)

        if self._paths is not None:
            # window.draw_paths(paths)
            self.draw_footsteps()
            self.start_animation(self._paths)

    def set_infos_txt(self):
        self.infos_txt_var.set("SUM OF COSTS: " + str(self._output_infos["sum_of_costs"]) + "\nMAKESPAN: " +
                               str(self._output_infos["makespan"]) + "\nN° OF EXPANDED NODES: " +
                               str(self._output_infos["expanded_nodes"]))

    def reset_function(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self._problem_instance.plot_on_gui(self.start_menu, self.frame, self._paths, self._output_infos)

    def quit_function(self):
        self.start_menu.enable_settings_buttons()
        for widget in self.frame.winfo_children():
            widget.destroy()

    def draw_world(self):
        n_rows, n_cols = self._map.get_height(), self._map.get_width()
        for row in range(n_rows):
            for col in range(n_cols):
                self.vis_cells[row][col] = self.map_canvas.create_rectangle(FRAME_MARGIN + self.cell_w * col,
                                                                            FRAME_MARGIN + self.cell_h * row,
                                                                            FRAME_MARGIN + self.cell_w * (col + 1),
                                                                            FRAME_MARGIN + self.cell_h * (row + 1))
                if self._map.is_obstacle(col, row):
                    self.map_canvas.itemconfig(self.vis_cells[row][col], fill='gray', width=2)

    def draw_agents(self):
        for a in self._agents:
            s_col, s_row = a.get_start()
            g_col, g_row = a.get_goal()

            random_color = '#%02x%02x%02x' % tuple(np.random.choice(range(256), size=3))
            self.agents_colors.append(random_color)
            self.agents_ovals.append(self.map_canvas.create_oval(FRAME_MARGIN + self.cell_w * s_col,
                                                                 FRAME_MARGIN + self.cell_h * s_row,
                                                                 FRAME_MARGIN + self.cell_w * (s_col + 1),
                                                                 FRAME_MARGIN + self.cell_h * (s_row + 1),
                                                                 outline='black', fill=random_color))
            self.map_canvas.itemconfig(self.vis_cells[s_row][s_col], fill=random_color, width=1.5)
            self.map_canvas.itemconfig(self.vis_cells[g_row][g_col], fill=random_color, stipple="gray50", width=1.5)
            self.text_list.append(self.map_canvas.create_text(FRAME_MARGIN + self.cell_w * s_col + self.cell_w / 2,
                                        FRAME_MARGIN + self.cell_h * s_row + self.cell_h / 2,
                                        font=("Purisa", get_font_dimension(self.dinamic_cell_w, self.dinamic_cell_h)),
                                        text="S"))
            self.text_list.append(self.map_canvas.create_text(FRAME_MARGIN + self.cell_w * g_col + self.cell_w / 2,
                                        FRAME_MARGIN + self.cell_h * g_row + self.cell_h / 2,
                                        font=("Purisa", get_font_dimension(self.dinamic_cell_w, self.dinamic_cell_h)),
                                        text="G"))

    def draw_paths(self, paths):
        for i, path in enumerate(paths):
            color = self.agents_colors[i]
            for p in path[1:-1]:
                self.map_canvas.itemconfig(self.vis_cells[p[1]][p[0]], fill=color, stipple="", width=1.5)

    def draw_footsteps(self):
        self._footsteps = True

    def start_animation(self, paths):
        self.path_to_visit = copy.deepcopy(paths)  # In order to copy by value also the nested lists
        self.frame.after(2000, self.animation_function)

    def animation_function(self):
        if self.animating:
            self.frame.after(int(MAX_SPEED - self.animation_speed), self.animation_function)
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
                        self.map_canvas.itemconfig(self.vis_cells[current_position[1]][current_position[0]],
                                                   fill=color, stipple="", width=1.5)
                    if self.path_to_visit[i]:
                        next_position = self.path_to_visit[i][0]
                        self.x_moves[i] = float((next_position[0] - current_position[0]) * self.dinamic_cell_w) / N_OF_STEPS
                        self.y_moves[i] = float((next_position[1] - current_position[1]) * self.dinamic_cell_h) / N_OF_STEPS
                        self.map_canvas.move(self.agents_ovals[i], self.x_moves[i], self.y_moves[i])
                        self.steps_count[i] = 1
                if not self.path_to_visit[i]:
                    self.map_canvas.delete(self.agents_ovals[i])

            if not [i for i in self.path_to_visit if i]:  # For checking that all the arrays are empty
                self.animating = False

        else:
            # Animation ended
            self.start_button.configure(state=NORMAL)
            self.reset_button.configure(state=NORMAL)
            self.quit_button.configure(state=NORMAL)

    def get_cell_size(self):
        avail_h = self._frame_height - 2 * FRAME_MARGIN
        avail_w = self._frame_width - 2 * FRAME_MARGIN
        n_rows, n_cols = self._map.get_height(), self._map.get_width()
        cell_h = avail_h / n_rows
        cell_w = avail_w / n_cols
        return cell_h, cell_w

    def do_loop(self):
        self.frame.mainloop()
