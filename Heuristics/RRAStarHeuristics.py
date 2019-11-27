from Heuristics.Heuristics import Heuristics
from Heuristics.ManhattanHeuristics import ManhattanHeuristics
from Utilities.SingleAgentState import SingleAgentState
from Utilities.StatesQueue import StatesQueue


class RRAStarHeuristics(Heuristics):

    def __init__(self, problem_instance):
        self._problem_instance = problem_instance
        self._open_lists = dict()  # Key is the goal position of the agent and the value is the open list.
        self._closed_lists = dict()  # Instead of using the agent as key, we use his goal position
        self.initialize_table()

    def resume_rra_star(self, goal_node, goal_pos):
        while not self._open_lists[goal_pos].is_empty():
            self._open_lists[goal_pos].sort_by_f_value()
            cur_state = self._open_lists[goal_pos].pop()
            self._closed_lists[goal_pos].add(cur_state)

            if cur_state.get_position() == goal_node:
                return True

            expanded_nodes = cur_state.expand()
            for state in expanded_nodes:
                if not self._open_lists[goal_pos].contains_position(state.get_position()) and \
                        not self._closed_lists[goal_pos].contains_position(state.get_position()):
                    self._open_lists[goal_pos].add(state)
                if self._open_lists[goal_pos].contains_position(state.get_position()):
                    if state.f_value() < self._open_lists[goal_pos].get_state_by_position(state.get_position()).f_value():
                        self._open_lists[goal_pos].update(state)
        return False

    def compute_heuristics(self, position, goal):
        if self._closed_lists[goal].contains_position(position):
            return self._closed_lists[goal].get_state_by_position(position).g_value()
        if self.resume_rra_star(position, goal):
            return self._closed_lists[goal].get_state_by_position(position).g_value()
        return 10000

    def initialize_table(self):
        for agent in self._problem_instance.get_agents():
            goal_pos = agent.get_goal()

            self._open_lists[goal_pos] = StatesQueue()
            self._closed_lists[goal_pos] = StatesQueue()

            # Invert start with goal
            starter_state = SingleAgentState(self._problem_instance.get_map(), agent.get_id(), agent.get_start(),
                                             agent.get_goal(), 0, ManhattanHeuristics(self._problem_instance))

            self._open_lists[goal_pos].add(starter_state)
            self.resume_rra_star(agent.get_start(), goal_pos)
