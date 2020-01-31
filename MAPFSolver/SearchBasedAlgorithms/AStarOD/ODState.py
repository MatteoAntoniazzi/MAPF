from MAPFSolver.SearchBasedAlgorithms.AStar.MultiAgentState import MultiAgentState


class ODState(MultiAgentState):
    """
    This class represent the single state (node) object for the A* algorithm with Operator Decomposition (OD).
    The state is a multi agent state, so it stores all the single agent states of each agent, and in addition it
    contains up to one move assignment for every agent. It keeps track of the next agent to move and of the previous
    standard state.
    The standard states are the ones where every agent has moved, while the intermediate states are the ones where only
    a subset of agents has moved.
    """

    def __init__(self, single_agent_states, solver_settings, parent=None, to_move=0, pre_state=None):
        """
        Initialize an OD multi agent state.
        :param single_agent_states: list of the single agent states.
        :param solver_settings: settings of the solver.
        :param parent: parent state.
        :param to_move: indicate the id of the agent that has to move during this expansion.
        :param pre_state: it indicates the previous standard state.
        """
        super().__init__(single_agent_states, solver_settings, parent=parent)
        self.set_time_step(single_agent_states[to_move].time_step())
        self._pre_state = self if pre_state is None else pre_state
        self._to_move = to_move

    def expand(self, verbose=False):
        """
        Expand the current state. It generates all the states obtained by expanding a single state (moving one agent at
        a time). So, it expands the next to move agent state and generate all the new OD states.
        :return: the list of possible next states.
        """
        if verbose:
            print("Expansion in progress...", end=' ')

        next_pre_state = self if self.next_to_move() == 1 else self._pre_state

        state_to_expand = self._single_agents_states[self._to_move]
        expanded_states_list = state_to_expand.expand()

        candidate_list = []
        for state in expanded_states_list:
            single_agent_states = [state for state in self._single_agents_states]
            single_agent_states[self._to_move] = state

            s = ODState(single_agent_states, self._solver_settings, parent=self, to_move=self.next_to_move(),
                        pre_state=next_pre_state)

            if s.is_a_standard_state():
                if not s.is_conflict(s._pre_state):
                    candidate_list.append(s)
            else:
                candidate_list.append(s)

        if verbose:
            print("DONE! Number of expanded states:", len(candidate_list))

        return candidate_list

    def next_to_move(self):
        """
        Return the next agent to move.
        """
        if self._to_move >= len(self._single_agents_states) - 1:
            return 0
        else:
            return self._to_move + 1

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
        """
        return self._to_move == 0

"""
Function to accelerate the process.
It checks if I have some single state that is already completed so I avoid to expand it.

    def skip_completed_states(self):
        if self._to_move == 0:
            while self._to_expand.is_completed():
                self._to_move += 1
                self._pre_state = self
                self._to_expand = self.get_single_agent_states()[self._to_move]

        if self._to_move > 0:
            while self._to_expand.is_completed():
                if self.next_to_move() == 0:
                    return
                else:
                    self._to_move += 1
                    self._to_expand = self.get_single_agent_states()[self._to_move]

"""