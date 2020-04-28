from MAPFSolver.SearchBasedAlgorithms.AStar.MultiAgentState import MultiAgentState
import itertools


class MStarState(MultiAgentState):
    """
    This class represent the single state (node) object for the M* algorithm.
    The state is like a multi agent state, so it stores all the single agent states (the positions and time step) of each
    agent, and in addition it keeps a collision set, which contains the agents that has a conflict in that node or in one of
    his successors, and a back propagation set, which contains the set of state where back propagate the collision set.
    """

    def __init__(self, single_agents_states, solver_settings, parent=None):
        """
        Initialize the Multi Agent State. It receives the solver settings and the list of all single agent states.
        :param single_agents_states: list of SingleAgentState instances.
        :param solver_settings: settings of the solver.
        :param parent: Eventual parent State.
        """
        super().__init__(single_agents_states, solver_settings, parent=parent)
        self._back_propagation_set = []
        self._collisions_set = set()
        self.compute_cost()
        self.compute_heuristics()

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
            if self.is_valid(multi_state):
                valid_states.append(multi_state)

        expanded_states = []
        for i, multi_state in enumerate(valid_states):
            m = MStarState(multi_state, self._solver_settings, parent=self)
            m.set_back_propagation_set([self])
            m.set_collisions_set(self.colliding_robots(m).copy())
            expanded_states.append(m)

        if verbose:
            print("DONE! Number of expanded states:", len(expanded_states))

        return expanded_states

    def set_back_propagation_set(self, back_set):
        """
        Set the back propagation set with the back_set inserted.
        :param back_set: new back propagation set.
        """
        self._back_propagation_set = back_set

    def get_back_propagation_set(self):
        """
        Returns the back propagation set of this state.
        """
        return self._back_propagation_set

    def set_collisions_set(self, collisions_set):
        """
        Set the collisions set with the collisions_set inserted.
        :param collisions_set: new collisions set.
        """
        self._collisions_set = collisions_set

    def get_collisions_set(self):
        """
        Returns the collision set of this state.
        """
        return self._collisions_set

    def equal_position(self, other):
        """
        Return True if the multi agent state and the given multi agent state has the same positions for all the single
        agent states.
        :param other: state to compare positions.
        """
        assert isinstance(other, MStarState)
        for i, single_state in enumerate(self._single_agents_states):
            if not single_state.equal_position(other.get_single_agent_states()[i]):
                return False
        return True

    def equal_position_and_time_step(self, other):
        """
        Return True if the multi agent state and the given multi agent state has the same positions for all the single
        agent states.
        :param other: state to compare positions.
        """
        assert isinstance(other, MStarState)
        for i, single_state in enumerate(self._single_agents_states):
            if not single_state.equal(other.get_single_agent_states()[i]):
                return False
        return True

    def equal(self, other):
        """
        Return True if the multi agent state and the given multi agent state has the same positions and the same time
        steps for all the single agent states.
        :param other: state to compare position.
        """
        assert isinstance(other, MStarState)
        if not self._collisions_set == other._collisions_set:
            return False
        for i, single_state in enumerate(self._single_agents_states):
            if not single_state.equal(other.get_single_agent_states()[i]):
                return False
        return True

    def __str__(self):
        string = '[F:' + str(self.f_value()) + ' G: ' + str(self.g_value()) + ' TS:' + str(self.time_step()) + ' '
        string += str(self.get_positions_list()) + ' ' + str(self.get_collisions_set()) + ']'
        return string
