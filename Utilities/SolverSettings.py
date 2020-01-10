class SolverSettings:

    def __init__(self, heuristics="Manhattan", goal_occupation_time=1):
        self._heuristics_str = heuristics
        self._goal_occupation_time = goal_occupation_time

    def get_heuristics_str(self):
        return self._heuristics_str

    def get_goal_occupation_time(self):
        return self._goal_occupation_time

    def set_goal_occupation_time(self, time):
        self._goal_occupation_time = time

    def __str__(self):
        return "Heuristics: " + self._heuristics_str + ".\tGoal occupation time: " + str(self._goal_occupation_time)
