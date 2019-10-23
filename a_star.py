from Utilities.Node import *


def manhattan_dist(a, b):
    """
    Returns the Manhattan distance between two points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(grid_world, start, goal, heuristic=manhattan_dist):
    """
    Returns the path between two nodes as a list of nodes using the A* algorithm.
    If no path could be found, an empty list is returned.

    grid -> is the map with obstacles
    start -> is the robot starting position (sx, sy)
    end -> is the robot ending position (gx, gy)

    return the path as list of Grid positions
    """

    starter_node = Node(start, 0, manhattan_dist(start, goal))
    frontier = [starter_node]
    closed_list = set()

    while frontier:
        frontier.sort(key=lambda x: x.f, reverse=False)
        cur = frontier.pop(0)
        closed_list.add(cur.position)

        if cur.position == goal:
            return cur.get_path_to_parent()

        possible_moves = grid_world.get_possible_moves_cells(cur.position)
        possible_moves = [move for move in possible_moves if move not in closed_list]
        for i in possible_moves:
            n = Node(i, cur.g+1, manhattan_dist(i, goal), cur)
            frontier.append(n)

    return []
