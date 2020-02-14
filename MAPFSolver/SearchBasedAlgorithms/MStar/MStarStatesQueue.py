class MStarStatesQueue:
    """
    Structure used as queue of states.
    """
    def __init__(self):
        """
        Initialize a new queue.
        """
        self._queue = []

    def get_node(self, item):
        """
        Return the node that has the same positions and time step of the one inserted. The collision set can be
        different.
        :param item: node that I want to return
        """
        for state in self._queue:
            if state.equal_position_and_time_step(item):
                return state
        return None

    def contains_state(self, item):
        """
        Return True if the queue already contains the same state. That is if exists already a state with the same
        positions and same time steps.
        :param item: instance of State.
        """
        for state in self._queue:
            if state.equal(item):
                return True
        return False

    def contains_position_and_time_step(self, item):
        """
        Return True if the queue already contains a state with the same position.
        (Only if the queue contains SingleAgentState instances)
        :param item: instance of State.
        """
        for state in self._queue:
            if state.equal_position_and_time_step(item):
                return True
        return False

    def contains_position(self, position):
        """
        Return True if the queue already contains a state with the same position.
        (Only if the queue contains SingleAgentState instances)
        :param position: (x,y) position.
        """
        for s in self._queue:
            if s.get_position() == position:
                return True
        return False

    def add(self, item):
        """
        Add an item state to the queue.
        :param item: state to add.
        """
        self._queue.append(item)

    def add_list_of_states(self, state_list):
        """
        Add a list of states to the queue.
        :param state_list: state list to add.
        """
        self._queue.extend(state_list)

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

    def get_state_by_position(self, position):
        """
        Return the state, if exists, that has the same given position.
        """
        for s in self._queue:
            if s.get_position() == position:
                return s
        return None

    def update(self, state):
        """
        Check if exists a state in the queue with same position of the given one. In that case he removes that state and
        append the given one.
        :param state: new state.
        :return: True if the state has been updated, False if the state was not present in the queue.
        """
        for s in self._queue:
            if s.get_position() == state.get_position():
                self._queue.remove(s)
                self.add(state)
                return True
        return False

    def sort_by_f_value(self):
        """
        Sort the queue by the f-value. Sorting also on the h-value as second index it speed up the process.
        """
        self._queue.sort(key=lambda x: (x.f_value(), x.h_value()), reverse=False)

    def __str__(self):
        string = ''
        for s in self._queue[:5]:
            string = string + s.__str__()
        return string
