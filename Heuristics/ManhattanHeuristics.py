from Heuristics.Heuristic import Heuristic


class ManhattanHeuristic(Heuristic):

    def __init__(self, problem_instance):
        self._problem_instance = problem_instance

    def compute_heuristic(self, position, goal):
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])
