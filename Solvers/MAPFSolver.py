import abc


class MAPFSolver:
    """
    Abstract class for any solver
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, heuristics_str):
        self._heuristics_str = heuristics_str
        self._heuristics = None

    @abc.abstractmethod
    def solve(self, problem_instance, verbose=False, print_output=True):
        """
        Compute the paths
        """