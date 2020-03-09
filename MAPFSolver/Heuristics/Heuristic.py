import abc


class Heuristic(object):

    __metaclass__ = abc.ABCMeta

    """
    ================== A* functions =================
    """
    @abc.abstractmethod
    def compute_heuristic(self, position, goal):
        """
        Compute the value of the heuristic in that position from that goal.
        """
