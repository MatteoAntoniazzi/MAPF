from colorama import Fore


MAIN_WINDOW_WIDTH = 1300
MAIN_WINDOW_HEIGHT = 700

SETTINGS_FRAME_WIDTH = 600
SETTINGS_FRAME_HEIGHT = 700

SIMULATION_FRAME_WIDTH_AND_HEIGHT = 700

MAP_FRAME_WIDTH_AND_HEIGHT = SIMULATION_FRAME_WIDTH_AND_HEIGHT-120


def get_frame_dimension(n_row, n_col):
    if n_row > n_col:
        frame_height = MAP_FRAME_WIDTH_AND_HEIGHT
        frame_width = (MAP_FRAME_WIDTH_AND_HEIGHT/n_row) * n_col
    elif n_row < n_col:
        frame_height = (MAP_FRAME_WIDTH_AND_HEIGHT/n_col) * n_row
        frame_width = MAP_FRAME_WIDTH_AND_HEIGHT
    else:
        frame_height = MAP_FRAME_WIDTH_AND_HEIGHT
        frame_width = MAP_FRAME_WIDTH_AND_HEIGHT
    return frame_width, frame_height


def get_font_dimension(cell_w, cell_h):
    if cell_w < 3 or cell_h < 3:
        return 2
    elif cell_w < 6 or cell_h < 6:
        return 4
    elif cell_w < 11 or cell_h < 11:
        return 6
    elif cell_w < 30 or cell_h < 30:
        return 10
    else:
        return 14


ALGORITHMS_MODES = [
    ("Cooperative A*", "Cooperative A*"),
    ("A*", "A*"),
    ("A* with Operator Decomposition", "A* with Operator Decomposition"),
    ("Increasing Cost Tree Search", "Increasing Cost Tree Search"),
    ("Conflict Based Search", "Conflict Based Search"),
    ("M*", "M*"),
]

COLORS_LIST =["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#800000",
              "#808000", "#008000", "#800080", "#008080", "#000080", "#FF7F50", "#FF8C00", "#9ACD32", "#FFC0CB",
              "#F5DEB3", "#D2691E"]

HEURISTICS_MODES = [
    ("Manhattan Distance", "Manhattan"),
    ("Abstract Distance with RRA*", "AbstractDistance")
]

OBJECTIVE_FUNCTION_MODES = [
    ("Sum the costs", "SOC"),
    ("Makespan", "Makespan")
]

FRAME_MARGIN = 10

UNOCCUPIED = 0
IS_OBSTACLE = -999

FORES = [Fore.BLACK, Fore.LIGHTBLACK_EX, Fore.RED, Fore.LIGHTRED_EX, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.YELLOW,
         Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.CYAN,
         Fore.LIGHTCYAN_EX, Fore.WHITE, Fore.LIGHTWHITE_EX]

N_OF_STEPS = 50  # N of step for a move. (From a cell to another)
SPEED_1X = 20      # Speed of moving (Higher is the value slower robots will move
MAX_SPEED = SPEED_1X * 2

'''
GOAL_OCCUPATION_TIME ->     # Means that stay 5 time_step and at the end of the fifth is already completely removed.
                            # Graphically it goes away at the start of the fifth.
                            # The minimum value is 1 which means that at the time step in which an agent arrive in the
                            # goal that position can be occupied only by him in that time step
'''