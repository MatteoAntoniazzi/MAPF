import abc


class MAPFSolver:
    """
    Abstract class for any solver
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, heuristics_str, objective_function, goal_occupation_time):
        self._heuristics_str = heuristics_str
        self._objective_function = objective_function
        self._heuristics = None
        self._goal_occupation_time = goal_occupation_time

    @abc.abstractmethod
    def solve(self, problem_instance, verbose=False, print_output=True):
        """
        Compute the paths
        """