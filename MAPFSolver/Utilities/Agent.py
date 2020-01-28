class Agent:
    """
    This class represents an Agent, with his id, start and goal position.
    """

    def __init__(self, id_agent, start, goal):
        """
        Initialize an agent. Start and goal are (x,y) in the map.
        """
        self._id = id_agent
        self._start = start
        self._goal = goal

    def get_id(self):
        """
        Return his agent id.
        """
        return self._id

    def get_start(self):
        """
        Return his start position.
        """
        return self._start

    def get_goal(self):
        """
        Return his goal position.
        """
        return self._goal

    def __str__(self):
        return "ID: " + str(self._id) + ". START: " + str(self._start) + ". GOAL: " + str(self._goal)
