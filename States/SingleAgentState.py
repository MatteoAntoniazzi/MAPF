from States.State import State


class SingleAgentState(State):
    def __init__(self, map, agent_id, goal, position, path_cost, heuristics, parent=None, time_step=0):
        super().__init__(parent, time_step)
        self._map = map
        self._agent_id = agent_id
        self._position = position  # In (x, y) Coordinates
        self._goal = goal
        self._heuristics = heuristics
        self._g = path_cost
        self.compute_heuristics()

    def expand(self, verbose=False):
        # if self.goal_test():  # If already in goal no expansion.
        #     return [self]       # Time_step remain blocked so once arrived it doesn't block others
        if self.goal_test():
            return [SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g, self._heuristics,
                                     parent=self, time_step=self._time_step+1)]
        expanded_nodes_list = [self.wait_state()]
        possible_moves = self._map.get_neighbours_xy(self._position)
        for i in possible_moves:
            expanded_nodes_list.append(SingleAgentState(self._map, self._agent_id, self._goal, i, self._g + 1,
                                                        self._heuristics, parent=self, time_step=self._time_step + 1))
        return expanded_nodes_list

    def goal_test(self):
        return self._position == self._goal

    def compute_heuristics(self):
        self._h = self._heuristics.compute_heuristics(self._position, self._goal)

    def calculate_cost(self):
        if self.is_root():
            self._g = 0
        else:
            self._g = self.predecessor().g_value() + 1
        return

    def wait_state(self):
        return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g+1, self._heuristics,
                                parent=self, time_step=self._time_step + 1)

    def get_position(self):
        return self._position

    def get_path_to_parent(self):
        path = []
        node = self
        while node._parent is not None:
            path.append(node._position)
            node = node._parent
        path.append(node._position)
        path.reverse()
        return path

    def get_agent_id(self):
        return self._agent_id

    def clone_state(self):
        return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g, self._heuristics,
                                parent=self._parent, time_step=self._time_step)

    def equal_position(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position

    def equal(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position and self._time_step == other._time_step

