class Agent:
    """
    This class represents an Agent, with his id, start and goal position.
    """

    def __init__(self, id_agent, start, goal):
        """
        Initialize an agent with an id and a start and a goal position.
        :param id_agent: id of the agent.
        :param start: starting position of the agent. It's a tuple (x, y) representing a position in the map.
        :param goal: goal position of the agent. It's a tuple (x, y) representing a position in the map.
        """
        self._id = id_agent
        self._start = start
        self._goal = goal

    def get_id(self):
        """
        Returns the agent id.
        """
        return self._id

    def get_start(self):
        """
        Returns the start position.
        """
        return self._start

    def get_goal(self):
        """
        Return the goal position.
        """
        return self._goal

    def __str__(self):
        return "Agent(id=" + str(self._id) + ", start=" + str(self._start) + ", goal=" + str(self._goal) + ")"
