"""
This class represent the single state (node) object for the M* algorithm.
The state is a multi agent state, so it stores all the single agent states (the positions and time step) of each agent,
and in addition it keeps a collision set, which contains the agents that has a conflict in that node or in one of his
successors, and a back propagation set, which contains the set of state where back propagate the collision set.
"""
from Utilities.State import State
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
import itertools


class MStarState(State):
    def __init__(self, problem_instance, single_agents_states, heuristics, obj_function, is_edge_conflict=True,
                 parent=None, time_step=0):
        super().__init__(parent=parent, time_step=time_step)
        self._problem_instance = problem_instance
        self._single_agents_states = single_agents_states
        self._heuristics = heuristics
        self._objective_function = obj_function
        self._is_edge_conflict = is_edge_conflict
        self._back_propagation_set = []
        self._collisions_set = set()
        self.calculate_cost()
        self.compute_heuristics()

    def get_paths_to_parent(self):
        """
        Compute and return the list of paths for each agent.
        """
        paths = []
        for single_state in self._single_agents_states:
            paths.append(single_state.get_path_to_parent())
        return paths

    def expand(self, verbose=False):
        """
        Expand the current state. For each single state, if the corresponding agent is not in the collision set, the
        next single state will be the one obtained by following the optimal policy, otherwise if it is in the collision
        set all the possible moves will be considered for that agent.
        Then these states are iterated in order to obtain all the possible multi agent state combinations.
        :return: the list of possible next states.
        """
        if verbose:
            print("Expansion in progress... COLLISIONS SET {:<24}".format(str(self._collisions_set)), end=" ")

        candidate_list = []
        for i, single_state in enumerate(self._single_agents_states):
            if i in self._collisions_set:
                single_state_neighbor_list = single_state.expand()
                candidate_list.append(single_state_neighbor_list)
            else:
                next_optimal_state = single_state.expand_optimal_policy()
                candidate_list.append([next_optimal_state])

        candidate_state_list = list(itertools.product(*candidate_list))

        valid_states = []
        for i, multi_state in enumerate(candidate_state_list):
            if is_valid(multi_state):  # a shallow copy to prevent change of multi_state
                valid_states.append(multi_state)

        expanded_states = []
        for i, multi_state in enumerate(valid_states):
            m = MStarState(self._problem_instance, multi_state, self._heuristics, self._objective_function,
                           self._is_edge_conflict, parent=self, time_step=self.time_step()+1)
            m.set_back_propagation_set([self])
            m.set_collisions_set(self.colliding_robots(m))
            expanded_states.append(m)

        if verbose:
            print("DONE! Number of expanded states:", len(expanded_states))

        return expanded_states

    def colliding_robots(self, multi_state):
        """
        Return the set of robots which collide in the given multi agent state.
        Will be checked that:
        1. no agents occupy the same position in the same time step;
        2. no agent overlap (switch places).
        """
        colliding_robots = set()

        for i, next_state_i in enumerate(multi_state.get_single_agent_states()):
            for j, next_state_j in enumerate(multi_state.get_single_agent_states()):
                if i != j and next_state_i.get_position() == next_state_j.get_position() and \
                        not next_state_i.is_completed() and not next_state_j.is_completed():
                    colliding_robots.add(i)
                    colliding_robots.add(j)

        if self._is_edge_conflict:
            current_positions = self.get_positions_list()
            next_positions = multi_state.get_positions_list()

            for i, next_pos in enumerate(next_positions):
                for j, cur_pos in enumerate(current_positions):
                    if i != j:
                        if next_pos == cur_pos:
                            if next_positions[j] == current_positions[i]:
                                colliding_robots.add(i)
                                colliding_robots.add(j)

        return colliding_robots

    def goal_test(self):
        """
        Return True if all agents have arrived to the goal position. Remember that it not consider the occupation time,
        so if the agents will remain in the goal position for tot time step this will continue to occupy that position.
        """
        for single_state in self._single_agents_states:
            if not single_state.goal_test():
                return False
        return True

    def is_completed(self):
        """
        Return True if all agents have arrived to the goal position and stayed there for the time needed.
        So, all the agents will have completed and will be disappeared.
        """
        for single_state in self._single_agents_states:
            if not single_state.is_completed():
                return False
        return True

    def set_back_propagation_set(self, back_set):
        self._back_propagation_set = back_set

    def get_back_propagation_set(self):
        return self._back_propagation_set

    def set_collisions_set(self, collisions_set):
        self._collisions_set = collisions_set

    def get_collisions_set(self):
        return self._collisions_set

    def compute_heuristics(self):
        self._h = 0
        if self._objective_function == "SOC":
            for single_state in self._single_agents_states:
                self._h += single_state.h_value()
        if self._objective_function == "Makespan":
            self._h = max([single_state.h_value() for single_state in self._single_agents_states])

    def calculate_cost(self):
        self._g = 0
        if self.is_root():
            return
        if self._objective_function == "SOC":
            for single_state in self._single_agents_states:
                self._g += single_state.g_value()
        if self._objective_function == "Makespan":
            self._g = max([single_state.g_value() for single_state in self._single_agents_states])

    def get_single_agent_states(self):
        return self._single_agents_states

    def get_positions_list(self):
        return [state.get_position() for state in self._single_agents_states]

    def get_active_positions_list(self):
        pos_list = []
        for state in self._single_agents_states:
            if not state.is_completed():
                pos_list.append(state.get_position())
        return pos_list

    def clone_state(self):
        clone_states = [state.clone_state() for state in self._single_agents_states]
        return MStarState(self._problem_instance, clone_states, self._heuristics, self._objective_function,
                          parent=self._parent, time_step=self._time_step)

    def clone_states(self):
        return [state.clone_state() for state in self._single_agents_states]

    def equal_position(self, other):
        assert isinstance(other, MStarState)
        for i, single_state in enumerate(self._single_agents_states):
            if not single_state.equal_position(other.get_single_agent_states()[i]):
                return False
        return True

    def equal(self, other):
        assert isinstance(other, MStarState)
        for i, single_state in enumerate(self._single_agents_states):
            if not single_state.equal(other.get_single_agent_states()[i]):
                return False
        return True

    def __str__(self):
        string = '[F:' + str(self.f_value()) + ' TS:' + str(self.time_step())
        for s in self._single_agents_states:
            string += s.__str__()
        string += ']'
        return string


def is_valid(multi_state):
    if len(multi_state) == 1:
        return True
    for s in multi_state:
        assert isinstance(s, SingleAgentState)
    return True
