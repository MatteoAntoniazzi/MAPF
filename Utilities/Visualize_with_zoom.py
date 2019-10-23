# ATTEMPT TO VISUALIZE WITH ZOOM --> to improve a lot

'''

import numpy as np
from macros import *
from tkinter import *


class Visualize:
    def __init__(self, grid_world):
        self.grid_world = grid_world
        self.frame = Tk()
        self.canvas = Canvas(self.frame, width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.canvas.grid()
        self.frame_width = FRAME_WIDTH
        self.frame_height = FRAME_HEIGHT
        self.avail_h = self.frame_height - 2 * FRAME_MARGIN
        self.avail_w = self.frame_width - 2 * FRAME_MARGIN
        self.n_rows, self.n_cols = self.grid_world.get_size()
        self.visible_rows, self.visible_cols = range(self.n_rows), range(self.n_cols)
        self.cell_mouse_pos_x, self.cell_mouse_pos_y = 0, 0

        self.cell_h, self.cell_w = self.get_cell_size()
        self.vis_cells = np.zeros_like(self.grid_world.grid, dtype=int)

        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button-5>', self.wheel)  # scroll down
        self.canvas.bind('<Button-4>', self.wheel)  # scroll up

    def draw_world(self):
        for visible_row, row in enumerate(self.visible_rows):
            for visible_col, col in enumerate(self.visible_cols):
                self.vis_cells[col][row] = self.canvas.create_rectangle(FRAME_MARGIN + self.cell_w * visible_col,
                                                                        FRAME_MARGIN + self.cell_h * visible_row,
                                                                        FRAME_MARGIN + self.cell_w * (visible_col + 1),
                                                                        FRAME_MARGIN + self.cell_h * (visible_row + 1))
                if self.grid_world.grid[col][row] == IS_OBSTACLE:
                    self.canvas.itemconfig(self.vis_cells[col][row], fill='gray', width=2)

    def draw_agents(self):
        for (i, ((sx, sy), (gx, gy))) in enumerate(self.grid_world.agents):
            self.canvas.itemconfig(self.vis_cells[sx][sy], fill='cyan', width=1.5)
            self.canvas.itemconfig(self.vis_cells[gx][gy], fill='pink', width=1.5)

            sx = sx - min(self.visible_cols)
            gx = gx - min(self.visible_cols)
            sy = sy - min(self.visible_rows)
            gy = gy - min(self.visible_rows)

            self.canvas.create_text(FRAME_MARGIN + self.cell_w * sx + self.cell_w/2, FRAME_MARGIN + self.cell_h * sy +
                                    self.cell_h/2,  font=("Purisa", 12), text=i)
            self.canvas.create_text(FRAME_MARGIN + self.cell_w * gx + self.cell_w / 2, FRAME_MARGIN + self.cell_h * gy +
                                    self.cell_h / 2,  font=("Purisa", 12), text=i)

    def get_cell_size(self):
        cell_h = self.avail_h / len(self.visible_rows)
        cell_w = self.avail_w / len(self.visible_cols)
        return cell_h, cell_w

    def do_loop(self):
        self.frame.mainloop()

    def motion(self, event):
        # Il mouse si può trovare nel guadrante 1, 2, 3 o 4
        x, y = event.x, event.y
        if x > FRAME_WIDTH/2:
            if y > FRAME_HEIGHT/2:
                self.quadrante = 4
            else:
                self.quadrante = 2
        else:
            if y > FRAME_HEIGHT/2:
                self.quadrante = 3
            else:
                self.quadrante = 1

    def wheel(self, event):
        if event.num == 4:
            self.zoom(True)
        if event.num == 5:
            self.zoom(False)

        self.cell_h, self.cell_w = self.get_cell_size()
        self.canvas.delete("all")
        self.draw_world()
        self.draw_agents()

    def zoom(self, increasing):
        if increasing:
            if len(self.visible_rows) > 20 and len(self.visible_cols) > 20:
                if self.quadrante == 1:
                    self.visible_rows = self.visible_rows[:-8]
                    self.visible_cols = self.visible_cols[:-8]
                if self.quadrante == 2:
                    self.visible_rows = self.visible_rows[:-8]
                    self.visible_cols = self.visible_cols[8:]
                if self.quadrante == 3:
                    self.visible_rows = self.visible_rows[8:]
                    self.visible_cols = self.visible_cols[:-8]
                if self.quadrante == 4:
                    self.visible_rows = self.visible_rows[8:]
                    self.visible_cols = self.visible_cols[8:]
        else:
            self.visible_rows = range(max(0, min(self.visible_rows)-8), min(self.n_rows, max(self.visible_rows)+8))
            self.visible_cols = range(max(0, min(self.visible_cols)-8), min(self.n_rows, max(self.visible_cols)+8))
'''
