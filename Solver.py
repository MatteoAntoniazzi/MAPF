import abc


class Solver:
    """
    Abstract class for any solver
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, problem_instance):
        self._problem_instance = problem_instance

    @abc.abstractmethod
    def compute_paths(self):
        """
        compute the paths
        """
