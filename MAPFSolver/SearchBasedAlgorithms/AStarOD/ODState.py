from MAPFSolver.SearchBasedAlgorithms.AStar.MultiAgentState import MultiAgentState


class ODState(MultiAgentState):
    """
    This class represent a state for the A* algorithm with Operator Decomposition (OD).
    The state is a multi agent state, so it stores all the single agent states of each agent, and in addition it keeps
    track of the next agent to move.
    """

    def __init__(self, single_agents_states, solver_settings, parent=None, to_move=0):
        """
        Initialize an OD multi agent state.
        :param single_agents_states: list of the single agent states.
        :param solver_settings: settings of the solver.
        :param parent: parent state.
        :param to_move: indicate the id of the agent that has to move during this expansion.
        """
        super().__init__(single_agents_states, solver_settings, parent=parent)
        self.set_time_step(max([state.time_step() for state in single_agents_states]))
        self._to_move = to_move

    def expand(self, verbose=False):
        """
        Expand the current state. It generates all the states obtained by expanding a single state (moving one agent at
        a time). So, it expands the next to move agent state and generate all the new OD states.
        :return: the list of possible next states.
        """
        if verbose:
            print("Expansion in progress...", end=' ')

        state_to_expand = self._single_agents_states[self._to_move]
        expanded_states_list = state_to_expand.expand()

        candidate_list = []
        for state in expanded_states_list:
            single_agent_states = [state for state in self._single_agents_states]
            single_agent_states[self._to_move] = state

            s = ODState(single_agent_states, self._solver_settings, parent=self, to_move=self.next_to_move())

            if not s.is_conflict_only_on_moved_agents():
                candidate_list.append(s)

        if verbose:
            print("DONE! Number of expanded states:", len(candidate_list))

        return candidate_list

    def is_conflict_only_on_moved_agents(self):
        """
        Return True if a conflict occur in the given multi agent state. This checks only the agents that has already
        moved, in order to guarantee to find the optimal solution.
        Will be checked that:
        1. no agents occupy the same position in the same time step;
        2. no agent overlap (switch places).
        """
        pre_state = self.get_previous_standard_state()

        # Cast the two states in order to consider only the agents already moved.
        pre_positions = pre_state.get_first_x_positions_list(self._to_move)
        next_positions = self.get_first_x_positions_list(self._to_move)
        next_active_positions = self.get_first_x_active_positions_list(self._to_move)

        if len(next_active_positions) != len(set(next_active_positions)):
            return True

        if self._solver_settings.is_edge_conflict():
            for i, next_pos in enumerate(next_positions):
                for j, cur_pos in enumerate(pre_positions):
                    if i != j:
                        if next_pos == cur_pos:
                            if next_positions[j] == pre_positions[i]:
                                return True
        return False

    def get_first_x_positions_list(self, x):
        """
        Return the list of the positions of the single agent states considering the first x single agent states.
        """
        if x == 0:
            return [state.get_position() for state in self._single_agents_states]
        else:
            return [state.get_position() for state in self._single_agents_states[:x]]

    def get_first_x_active_positions_list(self, x):
        """
        Return the list of the positions of the single agent states considering the first x single agent states.
        Considering only the ones really occupied.
        """
        pos_list = []
        if x == 0:
            for state in self._single_agents_states:
                if not state.is_gone():
                    pos_list.append(state.get_position())
        else:
            for state in self._single_agents_states[:x]:
                if not state.is_gone():
                    pos_list.append(state.get_position())

        return pos_list

    def goal_test(self):
        """
        Return True if all agents have arrived to the goal position. Remember that it not consider the occupation time,
        so if the agents will remain in the goal position for tot time step this will continue to occupy that position.
        The state must be a standard state.
        """
        if self.is_a_standard_state():
            return super().goal_test()
        return False

    def is_completed(self):
        """
        Return True if all agents have arrived to the goal position and stayed there for the time needed.
        So, all the agents will have completed and will be disappeared.
        The state must be a standard state.
        """
        if self.is_a_standard_state():
            return super().is_completed()
        return False

    def is_a_standard_state(self):
        """
        Return True if it is a standard state.
        The standard states are the ones where every agent has moved, while the intermediate states are the ones where
        only a subset of agents has moved.
        """
        return self._to_move == 0

    def get_previous_standard_state(self):
        """
        Return the previous standard state. It is useful to check edge conflicts.
        """
        if self.is_root():
            return self
        state = self._parent
        while not state.is_root():
            if state.is_a_standard_state():
                return state
            state = state.parent()
        return state

    def next_to_move(self):
        """
        Return the next agent to move.
        """
        if self._to_move >= len(self._single_agents_states) - 1:
            return 0
        else:
            return self._to_move + 1
