from States.SingleAgentState import SingleAgentState


class StateClosedList:
    def __init__(self):
        self._close_set = []

    def __contains__(self, item):
        assert isinstance(item, SingleAgentState)
        for s in self._close_set:
            if s.get_position() == item.get_position() and s.get_timestamp() == item.get_timestamp():
                return True
        return False
        # return all([s.get_position() != item.get_position() and s.get_timestamp() != item.get_timestamp() for s in self._close_set])  # not item.equal_position_and_timestamps(s)

    def add(self, state):
        assert isinstance(state, SingleAgentState)
        self._close_set.append(state)

    def add_list_of_states(self, state_list):
        self._close_set.extend(state_list)

    def pop(self):
        return self._close_set.pop(0)

    def delete_state(self, state):
        assert isinstance(state, SingleAgentState)
        if state in self._close_set:
            self._close_set.remove(state)

    def is_empty(self):
        return len(self._close_set) == 0

    def sort_by_f_value(self):
        self._close_set.sort(key=lambda x: x.f_value(), reverse=False)

    def __str__(self):
        string = ''
        for s in self._close_set:
            string = string + '[' + str(s.get_position()) + ' TS:' + str(s.get_timestamp()) + ']'
        return string
