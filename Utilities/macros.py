from colorama import Fore


MAIN_WINDOW_WIDTH = 1300
MAIN_WINDOW_HEIGHT = 700

SETTINGS_FRAME_WIDTH = 600
SETTINGS_FRAME_HEIGHT = 700

SIMULATION_FRAME_WIDTH_AND_HEIGHT = 700

MAP_FRAME_WIDTH_AND_HEIGHT = SIMULATION_FRAME_WIDTH_AND_HEIGHT-50


def get_frame_dimension(n_row, n_col):
    if n_row > n_col:
        frame_height = MAP_FRAME_WIDTH_AND_HEIGHT
        frame_width = (MAP_FRAME_WIDTH_AND_HEIGHT/n_row) * n_col
    elif n_row < n_col:
        frame_height = (MAP_FRAME_WIDTH_AND_HEIGHT/n_col) * n_row
        frame_width = MAP_FRAME_WIDTH_AND_HEIGHT
    else:
        frame_height = 650
        frame_width = 650
    return frame_width, frame_height

    #
    # if n_row < 15 and n_col < 24:
    #     frame_height = 50 * n_row
    #     frame_width = 50 * n_col
    # elif n_row < 25 and n_col < 40:
    #     frame_height = 30 * n_row
    #     frame_width = 30 * n_col
    # else:
    #     frame_height = 750
    #     frame_width = 1200


ALGORITHMS_MODES = [
    ("Cooperative A*", "Cooperative A*"),
    ("A*", "A*"),
    ("A* with Operator Decomposition", "A* with Operator Decomposition"),
    ("Increasing Cost Tree Search", "Increasing Cost Tree Search"),
    ("Conflict Based Search", "Conflict Based Search"),
    ("M*", "M*"),
]

PNG_PATH_LIST = ["./Maps/pngs/room-32-32-4.png", "./Maps/pngs/Berlin_1_256.png"]

HEURISTICS_MODES = [
    ("Manhattan Distance", "Manhattan"),
    ("Reverse Resumable A*", "RRA")
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

N_OF_STEPS = 20  # N of step for a move. (From a cell to another)
SPEED = 50      # Speed of moving (Higher is the value slower robots will move

GOAL_OCCUPATION_TIME = 5    # Means that stay 5 time_step and at the end of the fifth is already completely removed.
                            # Graphically it goes away at the start of the fifth.
                            # The minimum value is 1 which means that at the time step in which an agent arrive in the
                            # goal that position can be occupied only by him in that time step
