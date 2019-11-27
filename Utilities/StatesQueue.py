"""
Structure used as queue of states.
"""


class StatesQueue:
    def __init__(self):
        self._queue = []

    def contains_state(self, item):
        for state in self._queue:
            if state.equal(item):
                return True
        return False

    def contains_state_same_positions(self, item):
        for state in self._queue:
            if state.equal_position(item):
                return True
        return False

    def contains_position(self, position):
        for s in self._queue:
            if s.get_position() == position:
                return True
        return False

    def add(self, item):
        self._queue.append(item)

    def add_list_of_states(self, state_list):
        self._queue.extend(state_list)

    def pop(self):
        return self._queue.pop(0)

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)

    def get_state_by_position(self, position):
        for s in self._queue:
            if s.get_position() == position:
                return s
        return None

    def sort_by_f_value(self):
        self._queue.sort(key=lambda x: x.f_value(), reverse=False)

    def __str__(self):
        string = ''
        for s in self._queue[:5]:
            string = string + ' [F: ' + str(s.f_value()) + ' ' + str(s.get_positions_list()) + \
                     ' TS:' + str(s.time_step()) + '] '
        return string
