from colorama import Fore


FRAME_HEIGHT = 800
FRAME_WIDTH = 1200

FRAME_MARGIN = 10

UNOCCUPIED = 0
IS_OBSTACLE = -999

FORES = [Fore.BLACK, Fore.LIGHTBLACK_EX, Fore.RED, Fore.LIGHTRED_EX, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.YELLOW,
         Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.CYAN,
         Fore.LIGHTCYAN_EX, Fore.WHITE, Fore.LIGHTWHITE_EX]

N_OF_STEPS = 20  # N of step for a move. (From a cell to another)

GOAL_OCCUPATION_TIME = 5    # Means that stay 5 time_step and at the end of the fifth is already completely removed.
                            # Graphically it goes away at the start of the fifth.
                            # The minimum value is 1 which means that at the time step in which an agent arrive in the
                            # goal that position can be occupied only by him in that time step
