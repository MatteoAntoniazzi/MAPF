class ODState:
    def __init__(self, single_agents_states, next_to_move=0, parent=None):
        self._parent = parent
        self._single_agents_states = single_agents_states
        self._g = 0
        self._h = 0
        self._next_to_move = next_to_move
        self.compute_costs()

    def compute_costs(self):
        for single_state in self._single_agents_states:
            self._g += single_state.get_g_value()
            self._h += single_state.get_h_value()

    def get_h_value(self):
        return self._h

    def get_g_value(self):
        return self._g

    def get_f_value(self):
        return self._g + self._h

    def get_single_agent_states(self):
        return self._single_agents_states

    def get_next_to_move(self):
        return self._next_to_move