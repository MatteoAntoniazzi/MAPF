from States.State import State
from Utilities.distances_functions import *


class SingleAgentState(State):
    def __init__(self, problem_instance, agent_id, position, path_cost, parent=None):
        super().__init__(parent)
        self._problem_instance = problem_instance
        self._agent_id = agent_id
        self._position = position  # In (x, y) Coordinates
        self._time_step = 0
        self._g = path_cost
        self.compute_heuristic("manhattan")

    def expand(self):
        if self.goal_test():  # If already in goal no expansion
            return [self]
        expanded_nodes_list = [self.wait_state()]
        possible_moves = self._problem_instance.get_map().get_neighbours_xy(self._position)
        for i in possible_moves:
            expanded_nodes_list.append(SingleAgentState(self._problem_instance, self._agent_id, i, self._g + 1, self))
        return expanded_nodes_list

    def goal_test(self):
        return self._position == self._problem_instance.get_agent_by_id(self._agent_id).get_goal()

    def compute_heuristic(self, mode):
        goal_pos = self._problem_instance.get_agent_by_id(self._agent_id).get_goal()
        if mode == "manhattan":
            self._h = manhattan_dist(self._position, goal_pos)

    def calculate_cost(self):
        if self.is_root():
            self._g = 0
            return
        else:
            self._g = self.predecessor().g_value() + 1

    def wait_state(self):
        return SingleAgentState(self._problem_instance, self._agent_id, self._position, self._g + 1, self)

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

    def equal_position(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position
