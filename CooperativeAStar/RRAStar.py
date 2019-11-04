from States.SingleAgentState import SingleAgentState
from QueueStructures.SingleAgentQueue import SingleAgentQueue


class RRAStar:
    def __init__(self, map, agent):
        self._map = map
        self._agent = agent
        self._open = SingleAgentQueue()
        self._closed = SingleAgentQueue()
        starter_state = SingleAgentState(self._map, agent.get_id(), agent.get_start(), agent.get_goal(), 0, 0,
                                         heuristic="Manhattan")  # Invert start with goal
        self._open.add(starter_state)
        self.resume_rra_star(agent.get_start())

    def resume_rra_star(self, goal_node):
        while not self._open.is_empty():
            self._open.sort_by_f_value()
            cur_state = self._open.pop()
            self._closed.add(cur_state)

            if cur_state.get_position() == goal_node:
                return True

            expanded_nodes = cur_state.expand()
            for state in expanded_nodes:
                if not self._open.contains_position(state.get_position()) and \
                        not self._closed.contains_position(state.get_position()):
                    self._open.add(state)
                if self._open.contains_position(state.get_position()):
                    if state.f_value() < self._open.get_state_by_position(state.get_position()).f_value():
                        self._open.update(state)
        return False

    def abstract_distance(self, position):
        if self._closed.contains_position(position):
            return self._closed.get_state_by_position(position).g_value()
        if self.resume_rra_star(position):
            return self._closed.get_state_by_position(position).g_value()
        return 100000
