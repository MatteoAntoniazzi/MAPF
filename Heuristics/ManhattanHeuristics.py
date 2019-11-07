from Heuristics.Heuristics import Heuristics


class ManhattanHeuristics(Heuristics):

    def __init__(self, problem_instance):
        self._problem_instance = problem_instance

    def compute_heuristics(self, position, goal):
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])
