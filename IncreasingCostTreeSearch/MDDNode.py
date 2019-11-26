"""
This class represent a node of the MDD diagram.
Every node s represent a position and a time step. Remember that a node here can have multiple parents.
"""
from Utilities.macros import *


class MDDNode:
    def __init__(self, map, position, time_step=0, parent=None):
        self._map = map
        self._parent = parent
        self._position = position
        self._time_step = time_step

    def expand(self):
        """
        Expand the current state. It computes all the possible moves from that position.
        :return: the list of possible next states.
        """
        possible_moves = self._map.get_neighbours_xy(self._position)
        possible_moves.insert(0, self._position)   # Wait move

        expanded_nodes_list = []
        for pos in possible_moves:
            expanded_nodes_list.append(MDDNode(self._map, pos, time_step=self._time_step+1, parent=[self]))

        return expanded_nodes_list

    def get_paths_to_parent(self):
        """
        Return a list of all the possible paths from the start to the goal. It builds the paths starting from the goal
        and going up following all the possible parents alternatives.
        """
        paths = self.get_paths_to_parent_fun()

        for path in paths:
            path.reverse()
            goal = path[len(path)-1]

            for i in range(GOAL_OCCUPATION_TIME-1):
                path.append(goal)

        return paths

    def parent(self):
        return self._parent

    def position(self):
        return self._position

    def time_step(self):
        return self._time_step

    def add_parent(self, parent):
        self._parent.append(parent)

    def get_paths_to_parent_fun(self):
        paths = []
        path = []
        node = self

        path.append(node._position)

        while node.parent() is not None and len(node.parent()) == 1:
            path.append(node.parent()[0].position())
            node = node.parent()[0]

        if node.parent() is not None:
            if len(node.parent()) > 1:
                for parent in node.parent():
                    parent_paths = parent.get_paths_to_parent_fun()
                    for parent_path in parent_paths:
                        new_path = path.copy()
                        new_path.extend(parent_path)
                        paths.append(new_path)

        if not paths:
            return [path]
        else:
            return paths
