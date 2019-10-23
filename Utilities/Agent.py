class Agent(object):
    def __init__(self, id, start, goal):
        """ start and goal are (x,y) in the map"""
        self._id = id
        self._start = start
        self._goal = goal

    def get_id(self):
        return self._id

    def get_start(self):
        return self._start

    def get_goal(self):
        return self._goal

    def __lt__(self, other):
        return self._id < other.get_id()
