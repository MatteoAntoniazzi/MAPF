from IncreasingCostTreeSearch.IncreasingCostTreeNode import IncreasingCostTreeNode


class IncreasingCostTreeQueue:
    def __init__(self):
        self._queue = []

    def contains_node(self, item):
        assert isinstance(item, IncreasingCostTreeNode)
        for node in self._queue:
            if item.path_costs_vector() == node.path_costs_vector():
                return True
        return False

    def add(self, item):
        assert isinstance(item, IncreasingCostTreeNode)
        self._queue.append(item)

    def add_list_of_nodes(self, node_list):
        self._queue.extend(node_list)

    def pop(self):
        return self._queue.pop(0)

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)