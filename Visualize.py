import numpy as np
from macros import *
from tkinter import *


class Visualize:
    def __init__(self, grid_world):
        self.grid_world = grid_world
        self.frame = Tk()
        self.canvas = Canvas(self.frame, width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.canvas.grid()
        self.cell_h, self.cell_w = self.get_cell_size()
        self.vis_cells = np.zeros_like(self.grid_world.grid, dtype=int)

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
            self.canvas.itemconfig(self.vis_cells[s_row][s_col], fill=random_color, width=1.5)
            self.canvas.itemconfig(self.vis_cells[g_row][g_col], fill=random_color, width=1.5)
            self.canvas.create_text(FRAME_MARGIN + self.cell_w * s_col + self.cell_w/2,
                                    FRAME_MARGIN + self.cell_h * s_row + self.cell_h/2, font=("Purisa", 12), text="S")
            self.canvas.create_text(FRAME_MARGIN + self.cell_w * g_col + self.cell_w/2,
                                    FRAME_MARGIN + self.cell_h * g_row + self.cell_h/2, font=("Purisa", 12), text="G")

    def get_cell_size(self):
        avail_h = FRAME_HEIGHT - 2 * FRAME_MARGIN
        avail_w = FRAME_WIDTH - 2 * FRAME_MARGIN
        n_rows, n_cols = self.grid_world.get_size()
        cell_h = avail_h / n_rows
        cell_w = avail_w / n_cols
        return cell_h, cell_w

    def do_loop(self):
        self.frame.mainloop()
