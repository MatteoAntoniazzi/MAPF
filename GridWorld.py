from Visualize import *
from macros import *
from colorama import Fore, Back
from random import choice

# We have 2 types of coordinates:
# X,Y Coordinates
# Grid Coordinates


class GridWorld:
    def __init__(self, h, w, obstacles):    # obstacles are in X,Y Coordinates
        self.h = h
        self.w = w
        self.obstacles = convert_obstacles_in_grid_coordinates(obstacles)  # in Grid Coordinates
        self.grid = np.zeros((h, w), dtype=int)
        self.add_obstacles(self.obstacles)
        self.agents = []    # in Grid Coordinates

    def add_obstacles(self, obstacles):
        if obstacles:
            for obstacle in obstacles:
                obstacle_x, obstacle_y = obstacle[0], obstacle[1]
                self.grid[obstacle_x][obstacle_y] = IS_OBSTACLE

    def add_agents(self, agents):   # agents are in X,Y Coordinates
        self.agents = convert_agents_in_grid_coordinates(agents)
        if agents:
            for (i, ((s_row, s_col), (g_row, g_col))) in enumerate(self.agents):
                if not self.grid[s_row][s_col] == IS_OBSTACLE and not self.grid[g_row][g_col] == IS_OBSTACLE:
                    self.grid[s_row][s_col] = i
                    self.grid[g_row][g_col] = i
                else:
                    raise Exception('An agent position or goal position is on an obstacle')

    def print_grid_on_terminal(self):
        grid = [[Fore.BLACK + Back.RESET + '·' for i in range(self.w)] for j in range(self.h)]
        for i, j in self.obstacles:
            grid[i][j] = Fore.LIGHTWHITE_EX + Back.LIGHTWHITE_EX + '#'
        for ((s_row, s_col), (g_row, g_col)) in self.agents:
            color = choice(FORES)
            grid[s_row][s_col] = color + Back.RESET + '⚉'
            grid[g_row][g_col] = color + Back.RESET + '⚇'
        for i in range(len(grid)):
            print(*grid[i], Fore.BLUE + Back.RESET + '', sep='')
        print(Fore.RESET + Back.RESET + '')

    def print_on_gui(self):
        window = Visualize(self)
        window.draw_world()
        window.draw_agents()
        window.do_loop()

    def get_size(self):
        return self.h, self.w

    def get_possible_moves_cells(self, cell_pos):
        neighbour_cells = []
        row, col = cell_pos[0], cell_pos[1]

        # WAIT
        neighbour_cells.append((row, col))
        # MOVE LEFT
        if col > 0 and not self.grid[row][col-1] == IS_OBSTACLE:
            neighbour_cells.append((row, col-1))
        # MOVE RIGHT
        if col < self.w-1 and not self.grid[row][col+1] == IS_OBSTACLE:
            neighbour_cells.append((row, col+1))
        # MOVE UP
        if row > 0 and not self.grid[row-1][col] == IS_OBSTACLE:
            neighbour_cells.append((row-1, col))
        # MOVE DOWN
        if row < self.h-1 and not self.grid[row+1][col] == IS_OBSTACLE:
            neighbour_cells.append((row+1, col))

        return neighbour_cells


def convert_obstacles_in_grid_coordinates(obstacles):
    return [(y, x) for x, y in obstacles]


def convert_agents_in_grid_coordinates(agents):
    return [((sy, sx), (gy, gx)) for (sx, sy), (gx, gy) in agents]
