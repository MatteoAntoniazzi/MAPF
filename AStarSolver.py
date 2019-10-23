from Solver import Solver
from Utilities.Node import Node


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
            print("FIND_PATHS")
            starter_node = Node(start, 0, self._heuristic(start, goal))
            frontier = [starter_node]
            closed_list = set()

            while frontier:
                frontier.sort(key=lambda x: x.f, reverse=False)
                cur = frontier.pop(0)
                closed_list.add(cur.position)

                if cur.position == goal:
                    return cur.get_path_to_parent()

                possible_moves = self._map.get_neighbours_xy(cur.position)
                possible_moves = [move for move in possible_moves if move not in closed_list]
                for i in possible_moves:
                    n = Node(i, cur.g + 1, self._heuristic(i, goal), cur)
                    frontier.append(n)

            return []



