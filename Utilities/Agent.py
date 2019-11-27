class Agent(object):
    def __init__(self, id_agent, start, goal):
        """ start and goal are (x,y) in the map"""
        self._id = id_agent
        self._start = start
        self._goal = goal

    def get_id(self):
        return self._id

    def get_start(self):
        return self._start

    def get_goal(self):
        return self._goal
