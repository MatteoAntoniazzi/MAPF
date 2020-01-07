import numpy as np
from Utilities.macros import *
from tkinter import *
import copy


class Visualize:
    def __init__(self, start_menu, frame, map, agents):
        self._map = map
        self._agents = agents
        self.frame = frame
        self.start_menu = start_menu
        self._frame_width, self._frame_height = get_frame_dimension(map.get_height(), map.get_width())
        self.visualize_canvas = Canvas(self.frame)
        self.canvas = Canvas(self.visualize_canvas, width=self._frame_width, height=self._frame_height)
        self.canvas.pack()
        self.buttons_canvas = Canvas(self.visualize_canvas)
        start_button = Button(self.buttons_canvas, text="START", command=self.start_function)
        start_button.pack(side=LEFT)
        stop_button = Button(self.buttons_canvas, text="STOP", command=self.stop_function)
        stop_button.pack(side=LEFT)
        self.buttons_canvas.pack(anchor=E)

        self.visualize_canvas.pack(ipady=10)
        self.cell_h, self.cell_w = self.get_cell_size()
        self.vis_cells = np.zeros((self._map.get_height(), self._map.get_width()), dtype=int)
        self.agents_ovals = []
        self.agents_colors = []

        # For animation
        self.animating = True
        self._footsteps = False
        self.path_to_visit = []
        self.steps_count = [N_OF_STEPS] * len(self._agents)
        self.x_moves = [0] * len(self._agents)
        self.y_moves = [0] * len(self._agents)

    def start_function(self):
        print("ANIMATION RUNN")

    def stop_function(self):
        self.start_menu.enable_settings_buttons()
        for widget in self.frame.winfo_children():
            widget.destroy()
        print("ANIMATION RUNN")

    def draw_world(self):
        n_rows, n_cols = self._map.get_height(), self._map.get_width()
        for row in range(n_rows):
            for col in range(n_cols):
                self.vis_cells[row][col] = self.canvas.create_rectangle(FRAME_MARGIN + self.cell_w * col,
                                                                        FRAME_MARGIN + self.cell_h * row,
                                                                        FRAME_MARGIN + self.cell_w * (col + 1),
                                                                        FRAME_MARGIN + self.cell_h * (row + 1))
                if self._map.is_obstacle(col, row):
                    self.canvas.itemconfig(self.vis_cells[row][col], fill='gray', width=2)

    def draw_agents(self):
        for a in self._agents:
            s_col, s_row = a.get_start()
            g_col, g_row = a.get_goal()

            random_color = '#%02x%02x%02x' % tuple(np.random.choice(range(256), size=3))
            self.agents_colors.append(random_color)
            self.agents_ovals.append(self.canvas.create_oval(FRAME_MARGIN + self.cell_w * s_col,
                                                             FRAME_MARGIN + self.cell_h * s_row,
                                                             FRAME_MARGIN + self.cell_w * (s_col + 1),
                                                             FRAME_MARGIN + self.cell_h * (s_row + 1),
                                                             outline='black', fill=random_color))
            self.canvas.itemconfig(self.vis_cells[s_row][s_col], fill=random_color, width=1.5)
            self.canvas.itemconfig(self.vis_cells[g_row][g_col], fill=random_color, stipple="gray50", width=1.5)
            self.canvas.create_text(FRAME_MARGIN + self.cell_w * s_col + self.cell_w/2,
                                    FRAME_MARGIN + self.cell_h * s_row + self.cell_h/2, font=("Purisa", 12), text="S")
            self.canvas.create_text(FRAME_MARGIN + self.cell_w * g_col + self.cell_w/2,
                                    FRAME_MARGIN + self.cell_h * g_row + self.cell_h/2, font=("Purisa", 12), text="G")

    def draw_paths(self, paths):
        for i, path in enumerate(paths):
            color = self.agents_colors[i]
            for p in path[1:-1]:
                self.canvas.itemconfig(self.vis_cells[p[1]][p[0]], fill=color, stipple="", width=1.5)

    def draw_footsteps(self):
        self._footsteps = True

    def start_animation(self, paths):
        self.path_to_visit = copy.deepcopy(paths)  # In order to copy by value also the nested lists
        self.frame.after(2000, self.animation_function)

    def animation_function(self):
        if self.animating:
            self.frame.after(SPEED, self.animation_function)
            for i, agent in enumerate(self.agents_ovals):
                if self.steps_count[i] < N_OF_STEPS:
                    self.canvas.move(self.agents_ovals[i], self.x_moves[i], self.y_moves[i])
                    self.steps_count[i] += 1
                elif self.path_to_visit[i]:
                    current_position = self.path_to_visit[i].pop(0)
                    if self._footsteps:
                        color = self.agents_colors[i]
                        self.canvas.itemconfig(self.vis_cells[current_position[1]][current_position[0]],
                                               fill=color, stipple="", width=1.5)
                    if self.path_to_visit[i]:
                        next_position = self.path_to_visit[i][0]
                        self.x_moves[i] = float((next_position[0] - current_position[0]) * self.cell_w) / N_OF_STEPS
                        self.y_moves[i] = float((next_position[1] - current_position[1]) * self.cell_h) / N_OF_STEPS
                        self.canvas.move(self.agents_ovals[i], self.x_moves[i], self.y_moves[i])
                        self.steps_count[i] = 1
                if not self.path_to_visit[i]:
                    self.canvas.delete(self.agents_ovals[i])
            if not [i for i in self.path_to_visit if i]:  # For checking that all the arrays are empty
                self.animating = False

    def get_cell_size(self):
        avail_h = self._frame_height - 2 * FRAME_MARGIN
        avail_w = self._frame_width - 2 * FRAME_MARGIN
        n_rows, n_cols = self._map.get_height(), self._map.get_width()
        cell_h = avail_h / n_rows
        cell_w = avail_w / n_cols
        return cell_h, cell_w

    def do_loop(self):
        self.frame.mainloop()
