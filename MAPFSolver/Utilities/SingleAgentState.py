from MAPFSolver.Utilities.SolverSettings import SolverSettings
from Utilities.State import State


class SingleAgentState(State):
    def __init__(self, problem_map, goal, position, solver_settings, parent=None):
        """
        Class representing a single agent state. It stores the agent position at a specific time step. As superclass of
        State it has a g-value, an h-value, and the sum f-value, and the time step of the state.
        :param problem_map: problem map.
        :param goal: goal position of the agent involved.
        :param position: position of the agent in the current state.
        :param solver_settings: settings of the solver we're using.
        :param parent: parent state.
        """
        super().__init__(parent)
        self._map = problem_map
        self._position = position
        self._goal = goal
        self._solver_settings = solver_settings
        self.compute_cost()
        self.compute_heuristics()

    def expand(self, verbose=False):
        """
        Expand the current state. It computes the possible neighbour positions and creates a state for each new possible
        position. In addition of the neighbours we add the possibility to remain in the same position, obviously the
        time-step will be incremented and the cost of the wait move is equal to the cost to move, that is 1.
        If the state is a goal state or not we allow i both cases all the possible node expansions. So, even if the
        agent is in the goal state we allow him to be expanded and maybe return to a non goal state.
        Even if the state is completed we can expand it, this why we want to allow the agent to move from the goal if
        other agents for example need to pass from there. In this case we append itself to the expansion.
        :return: the list of possible next states.
        """
        expanded_nodes_list = []

        if self.is_completed():
            expanded_nodes_list.append(self)

        expanded_nodes_list.append(self.wait_state())
        possible_moves = self._map.get_neighbours_xy(self._position)
        for i in possible_moves:
            expanded_nodes_list.append(SingleAgentState(self._map, self._goal, i, self._solver_settings, parent=self))
        return expanded_nodes_list

    def wait_state(self):
        """
        Return a new state in the same position child of this.
        """
        return SingleAgentState(self._map, self._goal, self._position, self._solver_settings, parent=self)

    def expand_optimal_policy(self):
        """
        Compute the next state if we follow the optimal policy, so without keep account of conflicts with other agents.
        If the state is a goal state we start decrementing a variable which keep count of the time spent in the goal.
        If the state is a goal state and the agent has been in the goal for the time needed (defined by
        GOAL_OCCUPATION_TIME) the state is a completed state and the expansion return itself.
        :return: the next state following the optimal policy
        """
        if self.goal_test():
            if self.is_completed():
                return self   # Time_step remain blocked so once arrived it doesn't block others
            else:
                return SingleAgentState(self._map, self._goal, self._position,
                                        self._solver_settings, parent=self)

        next_node = self.get_next_optimal_state()

        return next_node

    def get_next_optimal_state(self):
        """
        Compute the next optimal state following the optimal policy.
        :return: the next state following the optimal policy
        """
        from Utilities.AStar import AStar
        solver = AStar(SolverSettings())  # Forse serve il goal occupation time generale
        path = solver.find_path(self._map, self._position, self._goal)
        next_pos = path[1]
        return SingleAgentState(self._map, self._goal, next_pos, self._solver_settings,
                                parent=self)

    def compute_heuristics(self):
        """
        Compute the heuristic value for this state using the set heuristic. (h-value)
        """
        self._h = self._solver_settings.get_heuristic_object().compute_heuristic(self._position, self._goal)

    def compute_cost(self):
        """
        Compute the cost of the current state. (g-value)
        For the case in which the agent need to stay in the goal for a goal occupation time, the time spent in the goal
        is not count in the cost. If the agent stays more than the goal occupation time needed the difference time is
        instead counted.
        """
        if self.is_root():
            self._g = 0
        else:
            list_of_states = [self]
            state = self
            while not state.is_root():
                state = state.predecessor()
                list_of_states.append(state)

            self._g = 0
            for i, s in enumerate(list_of_states):
                if not s.goal_test() or (s.goal_test() and i >= self._solver_settings.get_goal_occupation_time()):
                    self._g += len(list_of_states) - i
                    break

    def goal_test(self):
        """
        Return True if the agent is on the goal position.
        """
        return self._position == self._goal

    def is_completed(self):
        """
        Return True if the current state is completed.
        If the settings requires that agents stays in goal also after arrived we just check the goal test, otherwise we
        check that the agent has already spent the needed time stopped in the goal.
        """
        if self._solver_settings.stay_in_goal():
            return self.goal_test()
        else:
            state = self
            for i in range(self._solver_settings.get_goal_occupation_time()):
                if not state.goal_test():
                    return False
                state = state.predecessor()
            return True

    def get_position(self):
        """
        Return the state position.
        """
        return self._position

    def get_path_to_root(self):
        """
        Compute and return the path to the root.
        """
        path = []
        node = self
        while node._parent is not None:
            path.append(node._position)
            node = node._parent
        path.append(node._position)
        path.reverse()
        return path

    def clone_state(self):
        return self

    def equal_position(self, other):
        """
        Return True if the state and the given state has the same position.
        :param other: state to compare position.
        """
        assert isinstance(other, SingleAgentState)
        return self._position == other._position

    def equal(self, other):
        """
        Return True if the state and the given state has the same position and the same time step.
        :param other: state to compare position.
        """
        assert isinstance(other, SingleAgentState)
        return self._position == other._position and self.time_step() == other.time_step()

    def __str__(self):
        return '[STATE -> F: ' + str(self.f_value()) + ' ' + str(self._position) + ' TS:' + str(self.time_step()) + ']'
