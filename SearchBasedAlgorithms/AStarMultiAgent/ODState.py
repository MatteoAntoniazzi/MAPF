"""
This class represent the single state (node) object for the A* algorithm with OD.
The state is a multi agent state, so it stores all the single agent states (the positions and time step) of each agent,
and in addition it contains up to one move assignment for every agent. It keeps track of the next agent to move and of
the previous standard state.

The standard states are the ones where each agent has moved, while the intermediate states are the ones where only a
subset of agents has moved.
"""
from SearchBasedAlgorithms.AStarMultiAgent.MultiAgentState import MultiAgentState


class ODState(MultiAgentState):
    def __init__(self, problem_instance, single_agent_states, heuristics, obj_function, is_edge_conflict=True, to_move=0, pre_state=None,
                 parent=None, time_step=0):
        super().__init__(problem_instance, single_agent_states, heuristics, obj_function,
                         is_edge_conflict=is_edge_conflict, parent=parent, time_step=time_step)
        self._problem_instance = problem_instance
        if pre_state is None:
            self._pre_state = self
        else:
            self._pre_state = pre_state
        self._to_move = to_move
        self._to_expand = self.get_single_agent_states()[self._to_move]

    def expand(self, verbose=False):
        """
        Expand the current state. It generates all the states obtained by expanding a single state (moving one agent at
        a time). So, it expands the next to move agent state and generate all the new OD states.
        :return: the list of possible next states.
        """
        if verbose:
            print("Expansion in progress...", end=' ')

        self.skip_completed_states()

        if self.next_to_move() == 0:
            next_pre_state = self._pre_state
            next_time_step = self.time_step()+1
        elif self.next_to_move() == 1:
            next_pre_state = self
            next_time_step = self.time_step()
        else:
            next_pre_state = self._pre_state
            next_time_step = self.time_step()

        expanded_states_list = self._to_expand.expand()

        candidate_list = []
        for state in expanded_states_list:
            single_agent_states = self.clone_states()
            single_agent_states[self._to_move] = state

            s = ODState(self._problem_instance, single_agent_states, self._heuristics, self._objective_function,
                        is_edge_conflict=self._is_edge_conflict, to_move=self.next_to_move(), pre_state=next_pre_state, parent=self,
                        time_step=next_time_step)

            if s.is_a_standard_state():
                if not s.is_conflict(s._pre_state):
                    candidate_list.append(s)
            else:
                candidate_list.append(s)

        if verbose:
            print("DONE! Number of expanded states:", len(candidate_list))

        return candidate_list

    def skip_completed_states(self):
        """
        Function to accelerate the process.
        It checks if I have some single state that is already completed so I avoid to expand it.
        """
        if self._to_move == 0:
            while self._to_expand.is_completed():
                self._to_move += 1
                self._pre_state = self
                self._to_expand = self.get_single_agent_states()[self._to_move]

        if self._to_move > 0:
            while self._to_expand.is_completed():
                if self.next_to_move() == 0:
                    return '''[ODState(self._problem_instance, self.get_single_agent_states(), self._heuristics,
                                    self._objective_function, to_move=0, pre_state=self._pre_state, parent=self,
                                    time_step=self.time_step()+1)]'''
                    # Non serve a nulla potrei anche non ritornare nulla
                else:
                    self._to_move += 1
                    self._to_expand = self.get_single_agent_states()[self._to_move]

    def next_to_move(self):
        """
        Return the next agent to move
        """
        if self._to_move+1 >= len(self._problem_instance.get_agents()):
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
