import abc


class MAPFSolver:
    """
    Abstract class for any solver
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, solver_settings):
        self._solver_settings = solver_settings

    @abc.abstractmethod
    def solve(self, problem_instance, verbose=False, print_output=True):
        """
        Compute the paths
        """