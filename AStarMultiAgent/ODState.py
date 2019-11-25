from AStarMultiAgent.MultiAgentState import MultiAgentState


class ODState(MultiAgentState):
    def __init__(self, problem_instance, single_agent_states, heuristics, to_move=0, pre_state=None, parent=None,
                 time_step=0):
        super().__init__(problem_instance, single_agent_states, heuristics, parent=parent, time_step=time_step)
        self._problem_instance = problem_instance
        self._heuristics = heuristics
        if pre_state is None:
            self._pre_state = self
        else:
            self._pre_state = pre_state
        self._to_move = to_move   # Next Agent To Move
        self._to_expand = self.get_single_agent_states()[self._to_move]

    def expand(self, verbose=False):
        if verbose:
            print("Expansion in progress...", end=' ')

        if self.next_to_move() == 0:
            next_pre_state = self._pre_state
            next_time_step = self.time_step()+1
        elif self.next_to_move() == 1:          # if self._to_move == 0
            next_pre_state = self
            next_time_step = self.time_step()
        else:
            next_pre_state = self._pre_state
            next_time_step = self.time_step()

        self.skip_completed_states()

        expanded_states_list = self._to_expand.expand()

        candidate_list = []
        for state in expanded_states_list:
            single_agent_states = self.clone_states()
            single_agent_states[self._to_move] = state

            s = ODState(self._problem_instance, single_agent_states, self._heuristics,
                        to_move=self.next_to_move(), pre_state=next_pre_state, parent=self,
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
        # Check if I have some single state that is already completed so I avoid to expand it.
        if self._to_move == 0:
            while self._to_expand.is_completed():
                self._to_move += 1
                self._pre_state = self
                self._to_expand = self.get_single_agent_states()[self._to_move]

        if self._to_move > 0:
            while self._to_expand.is_completed():
                if self.next_to_move() == 0:
                    return [ODState(self._problem_instance, self.get_single_agent_states(), self._heuristics,
                                    to_move=0, pre_state=self._pre_state, parent=self,
                                    time_step=self.time_step() + 1)]
                else:
                    self._to_move += 1
                    self._to_expand = self.get_single_agent_states()[self._to_move]

    def next_to_move(self):
        if self._to_move+1 >= len(self._problem_instance.get_agents()):
            return 0
        else:
            return self._to_move + 1

    def goal_test(self):
        if self.is_a_standard_state():
            return super().goal_test()
        return False

    def is_completed(self):
        if self.is_a_standard_state():
            return super().is_completed()
        return False

    def is_a_standard_state(self):
        return self._to_move == 0
