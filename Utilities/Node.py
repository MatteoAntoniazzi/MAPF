class Node(object):
    def __init__(self, position, path_cost, heuristic_cost, parent=None):
        self.position = position  # In Grid coordinates
        self.g = path_cost
        self.h = heuristic_cost
        self.f = self.g + self.h
        self.parent = parent

    def get_path_to_parent(self):
        path = []
        node = self
        while node.parent is not None:
            path.append(node.position)
            node = node.parent
        path.append(node.position)
        path.reverse()

        return path
