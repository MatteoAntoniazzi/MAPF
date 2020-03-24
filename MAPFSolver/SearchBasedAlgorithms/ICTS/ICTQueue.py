from MAPFSolver.SearchBasedAlgorithms.ICTS.ICTNode import ICTNode


class ICTQueue:
    """
    Structure used as queue for the Increasing Cost Tree Nodes.
    """

    def __init__(self):
        """
        Initialize a new queue.
        """
        self._queue = []

    def contains_node(self, item):
        """
        Return True if the queue already contains the same node.
        :param item: instance of ICTSNode.
        """
        assert isinstance(item, ICTNode)
        for node in self._queue:
            if item.path_costs_vector() == node.path_costs_vector():
                return True
        return False

    def add(self, item):
        """
        Add an item node to the queue.
        :param item: node to add.
        """
        assert isinstance(item, ICTNode)
        self._queue.append(item)

    def add_list_of_nodes(self, node_list):
        """
        Add a list of nodes to the queue.
        :param node_list: node list to add.
        """
        self._queue.extend(node_list)

    def pop(self):
        """
        Pop the first element of the Queue and return it.
        """
        return self._queue.pop(0)

    def is_empty(self):
        """
        Return True if the queue is empty.
        """
        return len(self._queue) == 0

    def sort_by_cost(self):
        """
        Sort the queue by the node costs.
        """
        self._queue.sort(key=lambda x: x.total_cost(), reverse=False)
