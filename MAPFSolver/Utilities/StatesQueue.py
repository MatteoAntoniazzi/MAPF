from MAPFSolver.Utilities.SingleAgentState import SingleAgentState


class StatesQueue:
    """
    Structure used as queue of states. Can be used for both the single-agent state and the multi-agent state.
    """

    def __init__(self):
        """
        Initialize a new queue.
        """
        self._queue = []

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

    def contains_state(self, item):
        """
        Return True if the queue already contains the exact same state. That is if exists already a state with the same
        position(s) and same time step(s).
        :param item: instance of State.
        :return: True if the queue contains the same state.
        """
        for state in self._queue:
            if state.equal(item):
                return True
        return False

    def contains_state_same_positions(self, item):
        """
        If the queue already contains a state with the same position(s) then returns it. Otherwise it returns None.
        It is different from the previous since it considers equals two states that has the same list of positions but
        different time steps.
        :param item: instance of State.
        :return: the first equal state if present, otherwise None.
        """
        for state in self._queue:
            if state.equal_position(item):
                return state
        return None

    def update(self, state):
        """
        Check if exists a state in the queue with same position(s) of the given one. In that case he updates that state
        with the given one.
        :param state: new state.
        :return: True if the state has been updated, False if the state was not present in the queue.
        """
        for s in self._queue:
            if s.equal_position(state):
                self._queue.remove(s)
                self.add(state)
                return True
        return False

    def contains_position(self, position):
        """
        If the queue already contains a state with the same given position then returns it. Otherwise it returns None.
        (Only if the queue contains SingleAgentState instances)
        :param position: (x,y) position.
        :return: the first equal state if present, otherwise None.
        """
        if self._queue:
            assert isinstance(self._queue[0], SingleAgentState), "It can be called only in the single-agent case."
            for s in self._queue:
                if s.get_position() == position:
                    return s
        return None

    def sort_by_f_value(self):
        """
        Sort the queue by the f-value. Sorting also on the h-value as second index in order to speed up the process.
        """
        self._queue.sort(key=lambda x: (x.f_value(), x.h_value()), reverse=False)

    def __str__(self):
        string = ''
        for s in self._queue[:5]:
            string = string + s.__str__()
        return string
