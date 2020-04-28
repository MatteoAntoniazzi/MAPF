class MDDQueue:
    """
    Structure used as queue for the MDD nodes.
    """

    def __init__(self):
        """
        Initialize a new queue.
        """
        self._queue = []

    def contains_node(self, item):
        """
        Return True if the queue already contains the same node.
        :param item: instance of MDDNode.
        """
        for n in self._queue:
            if n.equal(item):
                return True
        return False

    def add_parent_to_node(self, item, parent):
        """
        Add a parent to the item node.
        :param item: node where add a parent.
        :param parent: parent node to add to the item.
        :return: True if the operation is done successfully.
        """
        for n in self._queue:
            if n.equal(item):
                n.add_parent(parent)
                return True
        return False

    def add(self, item):
        """
        Add an item node to the queue.
        :param item: node to add.
        """
        self._queue.append(item)

    def add_list(self, item_list):
        """
        Add a list of item node  to the queue.
        :param item_list: list of nodes to add.
        """
        for item in item_list:
            self.add(item)

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

    def sort_by_time_step(self):
        """
        Sort the queue by the node time steps.
        """
        self._queue.sort(key=lambda x: x.time_step(), reverse=False)

    def size(self):
        """
        Return the size of the queue.
        """
        return len(self._queue)
