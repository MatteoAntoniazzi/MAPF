from States.State import State
from States.SingleAgentState import SingleAgentState

import itertools
import time, sys


class MultiAgentState(State):
    def __init__(self, problem_instance, single_agents_states, parent=None):
        super().__init__(parent)
        self._problem_instance = problem_instance
        self._single_agents_states = single_agents_states
        self.calculate_cost()
        self.compute_heuristic("manhattan")

    def get_paths_to_parent(self):
        paths = []
        for single_state in self._single_agents_states:
            paths.append(single_state.get_path_to_parent())
        return paths

    def expand(self):
        candidate_list = []
        for single_state in self._single_agents_states:
            single_state_neighbor_list = single_state.expand()
            if len(single_state_neighbor_list) == 0:
                return []
            candidate_list.append(single_state_neighbor_list)

        candidate_state_list = itertools.product(*candidate_list)

        valid_states = []
        for i, multi_state in enumerate(candidate_state_list):
            if is_valid(multi_state):  # a shallow copy to prevent change of multi_state
                valid_states.append(MultiAgentState(self._problem_instance, multi_state, self))
        return valid_states

    def goal_test(self):
        for single_state in self._single_agents_states:
            if not single_state.goal_test():
                return False
        return True

    def compute_heuristic(self, mode):
        self._h = 0
        for single_state in self._single_agents_states:
            self._h += single_state.h_value()

    def calculate_cost(self):
        self._g = 0
        if self.predecessor() is None:
            return
        for single_state in self._single_agents_states:
            self._g += single_state.g_value()

    def get_g_value(self):
        return self._g

    def get_h_value(self):
        return self._h

    def get_f_value(self):
        return self._g + self._h

    def get_single_agent_states(self):
        return self._single_agents_states

    def get_positions_list(self):
        return [state.get_position() for state in self._single_agents_states]

    def get_state_by_agent_id(self, agent_id):
        for single_state in self._single_agents_states:
            if single_state.get_agent_id() == agent_id:
                return single_state
        print("The state of that agent doesn't exist!")
        return

    def print_infos(self):
        print("gValue=", self.get_g_value(), "hValue=", self.get_h_value(), "fValue=", self.get_f_value(), end=' ')
        for agent_state in self._single_agents_states:
            print(" ID:", agent_state.get_agent_id(), " POS:", agent_state.get_position(), end=' ')
        print('')

    def equal_positions(self, other):
        assert isinstance(other, MultiAgentState)
        for single_state in self._single_agents_states:
            if not single_state.equal_position(other.get_state_by_agent_id(single_state.get_agent_id())):
                return False
        return True


def is_valid(multi_state):
    if len(multi_state) == 1:
        return True
    for s in multi_state:
        assert isinstance(s, SingleAgentState)
    return True


# start_time = time.time()
# start_time_print_batch = start_time
#
# if (time.time() - start_time_print_batch) > 5:
#     print("Processed {} ( {:.2f}% ) in {:.2f} minutes.".format(
#         single_state.get_agent_id(),
#         100.0 * float(single_state.get_agent_id()) / len(self._single_agents_states),
#         (time.time() - start_time) / 60, ))
#     sys.stdout.flush()
#     sys.stderr.flush()
#     start_time_print_batch = time.time()