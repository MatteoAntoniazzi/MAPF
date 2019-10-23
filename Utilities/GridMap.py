# import numpy as np
#
# from Utilities.Map import Map
# from Utilities.macros import *
#
#
# class GridMap(Map):
#     def __init__(self, h, w, obstacles):
#         super().__init__(h, w, obstacles)
#         self._grid = self._create_grid()
#         self._obstacles_grid = [(y, x) for x, y in obstacles]  # In Grid Coordinates
#
#     def _create_grid(self):
#         grid = np.zeros((self._h, self._w), dtype=int)
#         if self._obstacles_xy:
#             for obstacle in self._obstacles_xy:
#                 obstacle_x, obstacle_y = obstacle[0], obstacle[1]
#                 grid[obstacle_y][obstacle_x] = IS_OBSTACLE
#         return grid
#
#     def get_neighbours_cells(self, cell_position):
#         """
#         Returns the positions of the neighbours in Grid Coordinates
#         """
#         x, y = cell_position[1], cell_position[0]
#
#         neighbours_xy = self.get_neighbours_xy(x, y)
#         neighbours_cells = [(y, x) for x, y in neighbours_xy]
#
#         return neighbours_cells
