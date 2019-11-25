import abc


class State(object):
    """
    Abstract class for singleAgent and MultiAgents
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, parent=None, time_step=0):
        self._g = None
        self._h = None
        self._time_step = time_step
        self._parent = parent

    def predecessor(self):
        return self._parent

    def g_value(self):
        return self._g

    def h_value(self):
        return self._h

    def f_value(self):
        return self._g + self._h

    def is_root(self):
        return self._parent is None

    def time_step(self):
        return self._time_step

    """
    ================== A* functions =================
    """
    @abc.abstractmethod
    def expand(self, verbose=False):
        """
        expand current state according to problemInstance
        """

    @abc.abstractmethod
    def goal_test(self):
        """
        test if state is goal state
        """

    """
    =========== functions to update member variables =========
    """
    @abc.abstractmethod
    def compute_heuristics(self):
        """
        Set hValue
        """

    @abc.abstractmethod
    def calculate_cost(self):
        """
        Calculate gValue
        """