class MDDNode:
    def __init__(self, map, position, time_step=0, parent=None):
        self._map = map
        self._parent = parent
        self._position = position
        self._time_step = time_step

    def expand(self):

        possible_moves = self._map.get_neighbours_xy(self._position)
        possible_moves.append(self._position)   # Wait move

        expanded_nodes_list = []
        for pos in possible_moves:
            expanded_nodes_list.append(MDDNode(self._map, pos, time_step=self._time_step+1, parent=self))

        return expanded_nodes_list

    def position(self):
        return self._position

    def time_step(self):
        return self._time_step

    def get_path_to_parent(self):
        path = []
        node = self
        while node._parent is not None:
            path.append(node._position)
            node = node._parent
        path.append(node._position)
        path.reverse()
        return path
