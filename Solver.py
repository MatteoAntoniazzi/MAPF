import abc


class Solver:
    """
    Abstract class for any solver
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, heuristics_str):
        self._heuristics_str = heuristics_str
        self._heuristics = None

    @abc.abstractmethod
    def solve(self, problem_instance):
        """
        Compute the paths
        """