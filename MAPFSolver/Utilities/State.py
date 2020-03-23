import abc


class State(object):
    """
    Abstract class for singleAgent and MultiAgents
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, parent=None):
        """
        Initialize the state. If it is a child node, the parent state must be passed.
        :param parent:
        """
        self._g = None
        self._h = None
        self._time_step = parent.time_step()+1 if parent is not None else 0
        self._parent = parent

    def parent(self):
        """
        Return the parent state.
        """
        return self._parent

    def g_value(self):
        """
        Return the g-value of the state.
        """
        return self._g

    def h_value(self):
        """
        Return the h-value of the state.
        """
        return self._h

    def f_value(self):
        """
        Return the f-value of the state.
        """
        return self._g + self._h

    def is_root(self):
        """
        Return True if the state is a root state.
        """
        return self._parent is None

    def set_time_step(self, ts):
        """
        Modify the time step value with ts.
        :param ts: time step to set.
        """
        self._time_step = ts

    def time_step(self):
        """
        Return the time step of the state.
        """
        return self._time_step

    """
    =================================== A* functions ===============================
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
    ======================= Functions to update member variables ===================
    """
    @abc.abstractmethod
    def compute_heuristics(self):
        """
        Set hValue
        """

    @abc.abstractmethod
    def compute_cost(self):
        """
        Calculate gValue
        """