from States.State import State
from Utilities.distances_functions import *


class SingleAgentState(State):
    def __init__(self, map, agent_id, goal, position, time_step, path_cost, parent=None, heuristic="Manhattan", rra=None):
        super().__init__(parent, time_step)
        self._map = map
        self._agent_id = agent_id
        self._position = position  # In (x, y) Coordinates
        self._goal = goal
        self._heuristic = heuristic
        self._g = path_cost
        self._rra = rra
        self.compute_heuristic(heuristic)

    def expand(self):
        # if self.goal_test():  # If already in goal no expansion.
        #     return [self]       # Time_step remain blocked so once arrived it doesn't block others
        if self.goal_test():
            return [SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._time_step+1,
                                     self._g, self, heuristic=self._heuristic, rra=self._rra)]
        expanded_nodes_list = [self.wait_state()]
        possible_moves = self._map.get_neighbours_xy(self._position)
        for i in possible_moves:
            expanded_nodes_list.append(SingleAgentState(self._map, self._agent_id, self._goal, i,
                                                        self._time_step + 1, self._g + 1, self,
                                                        heuristic=self._heuristic, rra=self._rra))
        return expanded_nodes_list

    def goal_test(self):
        return self._position == self._goal

    def compute_heuristic(self, mode):
        if mode == "Manhattan":
            self._h = manhattan_dist(self._position, self._goal)
        if mode == "RRA":
            self._h = self._rra.abstract_distance(self._position)

    def calculate_cost(self):
        if self.is_root():
            self._g = 0
        else:
            self._g = self.predecessor().g_value() + 1
        return

    def wait_state(self):
        return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._time_step + 1,
                                self._g + 1, self, heuristic=self._heuristic, rra=self._rra)

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

    def clone_state(self):
        return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._time_step, self._g,
                                parent=self._parent, heuristic=self._heuristic, rra=self._rra)

    def equal_position(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position

    def equal(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position and self._time_step == other._time_step

