import abc


class Heuristics(object):

    __metaclass__ = abc.ABCMeta

    """
    ================== A* functions =================
    """
    @abc.abstractmethod
    def compute_heuristics(self, position, goal):
        """
        Compute the value of the heuristic in that position
        """
