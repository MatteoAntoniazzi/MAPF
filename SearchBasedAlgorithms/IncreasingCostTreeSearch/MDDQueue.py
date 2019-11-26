"""
Structure used as queue for the MDD nodes.
"""
from SearchBasedAlgorithms.IncreasingCostTreeSearch.MDDNode import MDDNode


class MDDQueue:
    def __init__(self):
        self._queue = []

    def contains_node(self, item):
        assert isinstance(item, MDDNode)
        for n in self._queue:
            if n.position() == item.position() and n.time_step() == item.time_step():
                return True
        return False

    def add_parent_to_node(self, item, parent):
        assert isinstance(item, MDDNode)
        for n in self._queue:
            if n.position() == item.position() and n.time_step() == item.time_step():
                n.add_parent(parent)
                return True
        return False

    def node(self, item):
        assert isinstance(item, MDDNode)
        for n in self._queue:
            if n.position() == item.position() and n.time_step() == item.time_step():
                return n
        return None

    def add(self, item):
        assert isinstance(item, MDDNode)
        self._queue.append(item)

    def add_list_of_nodes(self, node_list):
        self._queue.extend(node_list)

    def pop(self):
        return self._queue.pop(0)

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)

    def sort_by_time_step(self):
        self._queue.sort(key=lambda x: x.time_step(), reverse=False)
