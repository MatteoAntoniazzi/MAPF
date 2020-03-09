from .Heuristic import Heuristic


class ManhattanDistanceHeuristic(Heuristic):
    """
    Standard heuristic for a square grid is the Manhattan distance.
    In Manhattan distance the distance between two points measured along axes at right angles.
    """

    def __init__(self, problem_instance):
        """
        Initialize the heuristic.
        """
        self._problem_instance = problem_instance

    def compute_heuristic(self, position, goal):
        """
        Compute the value of the heuristic in that position to the goal position.
        """
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])
