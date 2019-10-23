from Solver import Solver
from Utilities.State import State


def manhattan_dist(a, b):
    """
    Returns the Manhattan distance between two points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class AStarSolver(Solver):
    def __init__(self, problem_instance, heuristic=manhattan_dist):
        super().__init__(problem_instance)
        self._heuristic = heuristic

    def compute_paths(self):
        paths = []
        for a in self._agents:
            path = self.find_path(a.get_start(), a.get_goal())
            paths.append(path)
        return paths

    def find_path(self, start, goal):
        """
        Returns the path between two nodes as a list of nodes using the A* algorithm.
        If no path could be found, an empty list is returned.

        grid -> is the map with obstacles
        start -> is the robot starting position (sx, sy)
        end -> is the robot ending position (gx, gy)

        return the path as list of (x, y) positions
        """
        starter_state = State(start, 0, self._heuristic(start, goal))
        frontier = [starter_state]
        closed_list = set()

        while frontier:
            frontier.sort(key=lambda x: x.get_f_value(), reverse=False)
            cur_state = frontier.pop(0)
            closed_list.add(cur_state)

            if cur_state.get_position() == goal:
                return cur_state.get_path_to_parent()

            possible_moves = self._map.get_neighbours_xy(cur_state.get_position())
            possible_moves = [move for move in possible_moves if move not in closed_list]
            for i in possible_moves:
                n = State(i, cur_state.get_g_value() + 1, self._heuristic(i, goal), cur_state)
                frontier.append(n)

        return []
