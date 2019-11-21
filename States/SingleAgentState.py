from States.State import State
from Utilities.macros import *


class SingleAgentState(State):
    def __init__(self, map, agent_id, goal, position, path_cost, heuristics, parent=None, time_step=0,
                 time_remained_in_goal=GOAL_OCCUPATION_TIME):
        super().__init__(parent, time_step)
        self._map = map
        self._agent_id = agent_id
        self._position = position  # In (x, y) Coordinates
        self._goal = goal
        self._time_remained_in_goal = time_remained_in_goal
        self._heuristics = heuristics
        self._g = path_cost
        self.compute_heuristics()

    def expand(self, verbose=False):
        if self.goal_test():
            if self.is_completed():
                return [self.clone_state()]   # Time_step remain blocked so once arrived it doesn't block others
            elif self._time_remained_in_goal == 1:
                return [SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g,
                                         self._heuristics, parent=self, time_step=self._time_step+1,
                                         time_remained_in_goal=0)]
            else:
                return [SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g,
                                         self._heuristics, parent=self, time_step=self._time_step+1,
                                         time_remained_in_goal=self._time_remained_in_goal-1)]
        expanded_nodes_list = [self.wait_state()]
        possible_moves = self._map.get_neighbours_xy(self._position)
        for i in possible_moves:
            expanded_nodes_list.append(SingleAgentState(self._map, self._agent_id, self._goal, i, self._g + 1,
                                                        self._heuristics, parent=self, time_step=self._time_step + 1))
        return expanded_nodes_list

    def expand_optimal_policy(self):
        if self.goal_test():
            if self.is_completed():
                return self.clone_state()   # Time_step remain blocked so once arrived it doesn't block others
            elif self._time_remained_in_goal == 1:
                return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g,
                                        self._heuristics, parent=self, time_step=self._time_step+1,
                                        time_remained_in_goal=0)
            else:
                return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g,
                                        self._heuristics, parent=self, time_step=self._time_step+1,
                                        time_remained_in_goal=self._time_remained_in_goal-1)

        next_node = self.get_next_optimal_state()

        return next_node

    def get_next_optimal_state(self):
        from AStar import AStar
        solver = AStar()
        path = solver.find_path(self._map, self._position, self._goal)
        next_pos = path[1]
        return SingleAgentState(self._map, self._agent_id, self._goal, next_pos, self._g+1, self._heuristics,
                                parent=self, time_step=self._time_step+1)

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
                                parent=self, time_step=self._time_step+1)

    def is_completed(self):
        return self._time_remained_in_goal == 0

    def get_position(self):
        return self._position

    def get_path_to_parent(self):
        path = []
        node = self
        while node._parent is not None:
            if not node.is_completed():
                path.append(node._position)
            node = node._parent
        path.append(node._position)
        path.reverse()
        return path

    def get_agent_id(self):
        return self._agent_id

    def clone_state(self):
        return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g, self._heuristics,
                                parent=self._parent, time_step=self._time_step,
                                time_remained_in_goal=self._time_remained_in_goal)

    def equal_position(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position

    def equal(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position and self._time_step == other._time_step

    def __str__(self):
        string = ''
        string = string + ' [AGENT ID: ' + str(self._agent_id) + ' F: ' + str(self.f_value()) + ' ' + str(self._position) + ' TS:' + str(self.time_step()) \
                        + '] '
        return string
