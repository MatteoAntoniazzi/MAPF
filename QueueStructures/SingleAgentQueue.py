from States.SingleAgentState import SingleAgentState


class SingleAgentQueue:
    def __init__(self):
        self._queue = []

    def contains_state(self, item):
        assert isinstance(item, SingleAgentState)
        for s in self._queue:
            if s.get_position() == item.get_position() and s.time_step() == item.time_step():
                return True
        return False

    def contains_position(self, position):
        for s in self._queue:
            if s.get_position() == position:
                return True
        return False

    def add(self, state):
        assert isinstance(state, SingleAgentState)
        self._queue.append(state)

    def add_list_of_states(self, state_list):
        self._queue.extend(state_list)

    def pop(self):
        return self._queue.pop(0)

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)

    def sort_by_f_value(self):
        self._queue.sort(key=lambda x: x.f_value(), reverse=False)

    def get_state_by_position(self, position):
        for s in self._queue:
            if s.get_position() == position:
                return s
        return None

    def update(self, state):
        for s in self._queue:
            if s.get_position() == state.get_position():
                self._queue.remove(s)
                self.add(state)
                return True
        return False

    def __str__(self):
        string = ''
        for s in self._queue:
            string = string + '[' + str(s.get_position()) + ' TS:' + str(s.time_step()) + ']'
        return string
