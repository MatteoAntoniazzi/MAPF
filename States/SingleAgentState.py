from States.State import State
from Utilities.distances_functions import *


class SingleAgentState(State):
    def __init__(self, map, agent_id, agent_goal, position, time_step, path_cost, parent=None):
        super().__init__(parent)
        self._map = map
        self._agent_id = agent_id
        self._agent_goal = agent_goal
        self._position = position  # In (x, y) Coordinates
        self._time_step = time_step
        self._g = path_cost
        self.compute_heuristic("manhattan")

    def expand(self):
        if self.goal_test():  # If already in goal no expansion.
            return [self]       # Time_step remain blocked so once arrived it doesn't block others
        expanded_nodes_list = [self.wait_state()]
        possible_moves = self._map.get_neighbours_xy(self._position)
        for i in possible_moves:
            expanded_nodes_list.append(SingleAgentState(self._map, self._agent_id, self._agent_goal, i,
                                                        self._time_step+1, self._g+1, self))
        return expanded_nodes_list

    def goal_test(self):
        return self._position == self._agent_goal

    def compute_heuristic(self, mode):
        if mode == "manhattan":
            self._h = manhattan_dist(self._position, self._agent_goal)

    def calculate_cost(self):
        if self.is_root():
            self._g = 0
            return
        else:
            self._g = self.predecessor().g_value() + 1

    def wait_state(self):
        return SingleAgentState(self._map, self._agent_id, self._agent_goal, self._position, self._time_step+1,
                                self._g+1, self)

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

    def get_timestamp(self):
        return self._time_step

    def equal_position(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position

    def equal_position_and_timestamps(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position and self._time_step == other._time_step

