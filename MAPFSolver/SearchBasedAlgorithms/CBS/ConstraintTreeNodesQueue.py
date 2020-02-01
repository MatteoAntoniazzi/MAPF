from MAPFSolver.SearchBasedAlgorithms.CBS.ConstraintTreeNode import ConstraintTreeNode


class ConstraintTreeNodesQueue:
    """
    Structure used as queue for the Constraint Tree Nodes.
    """

    def __init__(self):
        """
        Initialize a new queue.
        """
        self._queue = []

    def contains_node(self, item):
        """
        Check if in the queue is already present the same item, i.e. a node with the same constraints.
        :param item: node to check if already present.
        :return: True if the node is already present in the queue.
        """
        assert isinstance(item, ConstraintTreeNode)
        for node in self._queue:
            if node.vertex_constraints() == item.vertex_constraints():
                return True
        return False

    def add(self, item):
        """
        Add a node to the queue.
        :param item: node to add.
        """
        assert isinstance(item, ConstraintTreeNode)
        self._queue.append(item)

    def add_list_of_nodes(self, node_list):
        """
        Add a list of nodes to the queue.
        :param node_list: list of nodes to add.
        """
        self._queue.extend(node_list)

    def pop(self):
        """
        Pop the first element of the queue and return it.
        """
        return self._queue.pop(0)

    def is_empty(self):
        """
        Return True if the queue is empty.
        """
        return len(self._queue) == 0

    def sort_by_cost(self):
        """
        Sort the queue by the nodes costs.
        """
        self._queue.sort(key=lambda x: x.total_cost(), reverse=False)
