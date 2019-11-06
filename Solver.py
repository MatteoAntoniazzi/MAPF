import abc


class Solver:
    """
    Abstract class for any solver
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def solve(self, problem_instance):
        """
        compute the paths
        """
