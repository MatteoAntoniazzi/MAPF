class State(object):
    def __init__(self, position, path_cost, heuristic_cost, parent=None):
        self._position = position  # In (x, y) Coordinates
        self._g = path_cost
        self._h = heuristic_cost
        self._parent = parent

    def get_path_to_parent(self):
        path = []
        node = self
        while node._parent is not None:
            path.append(node._position)
            node = node._parent
        path.append(node._position)
        path.reverse()
        return path

    def get_position(self):
        return self._position

    def get_h_value(self):
        return self._h

    def get_g_value(self):
        return self._g

    def get_f_value(self):
        return self._g + self._h

    def get_predecessor(self):
        return self._parent
