import numpy as np
from macros import *
from tkinter import *
import time
import copy


class Visualize:
    def __init__(self, grid_world):
        self.grid_world = grid_world
        self.frame = Tk()
        self.canvas = Canvas(self.frame, width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.canvas.grid()
        self.cell_h, self.cell_w = self.get_cell_size()
        self.vis_cells = np.zeros_like(self.grid_world.grid, dtype=int)
        self.agents_ovals = []
        self.agents_colors = []

        # For animation
        self.animating = True
        self.path_to_visit = copy.deepcopy(self.grid_world.paths)  # In order to copy by value also the nested lists
        self.steps_count = [N_OF_STEPS] * self.grid_world.n_of_agents
        self.x_moves = [0] * self.grid_world.n_of_agents
        self.y_moves = [0] * self.grid_world.n_of_agents

    def draw_world(self):
        n_rows, n_cols = self.grid_world.get_size()
        for row in range(n_rows):
            for col in range(n_cols):
                self.vis_cells[row][col] = self.canvas.create_rectangle(FRAME_MARGIN + self.cell_w * col,
                                                                        FRAME_MARGIN + self.cell_h * row,
                                                                        FRAME_MARGIN + self.cell_w * (col + 1),
                                                                        FRAME_MARGIN + self.cell_h * (row + 1))
                if self.grid_world.grid[row][col] == IS_OBSTACLE:
                    self.canvas.itemconfig(self.vis_cells[row][col], fill='gray', width=2)

    def draw_agents(self):
        for (i, ((s_row, s_col), (g_row, g_col))) in enumerate(self.grid_world.agents):
            random_color = '#%02x%02x%02x' % tuple(np.random.choice(range(256), size=3))
            self.agents_colors.append(random_color)
            self.agents_ovals.append(self.canvas.create_oval(FRAME_MARGIN + self.cell_w * s_col + self.cell_w/2 - self.cell_h/2,
                                                             FRAME_MARGIN + self.cell_h * s_row,
                                                             FRAME_MARGIN + self.cell_w * (s_col + 1) - self.cell_w/2 + self.cell_h/2,
                                                             FRAME_MARGIN + self.cell_h * (s_row + 1),
                                                             outline='black', fill=random_color))
            self.canvas.itemconfig(self.vis_cells[s_row][s_col], fill=random_color, width=1.5)
            self.canvas.itemconfig(self.vis_cells[g_row][g_col], fill=random_color, width=1.5)
            self.canvas.create_text(FRAME_MARGIN + self.cell_w * s_col + self.cell_w/2,
                                    FRAME_MARGIN + self.cell_h * s_row + self.cell_h/2, font=("Purisa", 12), text="S")
            self.canvas.create_text(FRAME_MARGIN + self.cell_w * g_col + self.cell_w/2,
                                    FRAME_MARGIN + self.cell_h * g_row + self.cell_h/2, font=("Purisa", 12), text="G")

    def draw_paths(self):
        for i, path in enumerate(self.grid_world.paths):
            color = self.agents_colors[i]
            for p in path[1:-1]:
                self.canvas.itemconfig(self.vis_cells[p[0]][p[1]], fill=color, width=1.5)

    def start_animation(self):
        self.frame.after(2000, self.animation_function)

    def animation_function(self):
        if self.animating:
            self.frame.after(150, self.animation_function)
            for i, agent in enumerate(self.agents_ovals):
                if self.steps_count[i] < N_OF_STEPS:
                    self.canvas.move(self.agents_ovals[i], self.x_moves[i], self.y_moves[i])
                    self.steps_count[i] += 1
                elif self.path_to_visit[i]:
                    current_position = self.path_to_visit[i].pop(0)
                    if self.path_to_visit[i]:
                        next_position = self.path_to_visit[i][0]
                        self.x_moves[i] = int((next_position[1] - current_position[1]) * self.cell_w) / N_OF_STEPS
                        self.y_moves[i] = int((next_position[0] - current_position[0]) * self.cell_h) / N_OF_STEPS
                        self.canvas.move(self.agents_ovals[i], self.x_moves[i], self.y_moves[i])
                        self.steps_count[i] = 1
            if not [i for i in self.path_to_visit if i]:  # For checking that all the arrays are empty
                self.animating = False

    def get_cell_size(self):
        avail_h = FRAME_HEIGHT - 2 * FRAME_MARGIN
        avail_w = FRAME_WIDTH - 2 * FRAME_MARGIN
        n_rows, n_cols = self.grid_world.get_size()
        cell_h = avail_h / n_rows
        cell_w = avail_w / n_cols
        return cell_h, cell_w

    def do_loop(self):
        self.frame.mainloop()
