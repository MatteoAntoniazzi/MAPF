from .State import State


class SingleAgentState(State):
    """
    Class representing a single agent state. It stores the agent position at a specific time step. As superclass of
    State it has a g-value, an h-value, and the sum f-value, and the time step of the state.
    """

    def __init__(self, problem_map, goal, position, solver_settings, parent=None):
        """
        Initialize a single-agent state.
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
        position. We can see that even if an agent has reached his goal the expansion is still possible. He will be able
        to move from the goal with an increase of the cost or stay in the goal without increase the cost.
        :return: the list of possible next states.
        """
        expanded_nodes_list = [self.wait_state()]
        possible_moves = self._map.neighbours(self._position)
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
            return self.wait_state()

        next_node = self.get_next_optimal_state()

        return next_node

    def get_next_optimal_state(self):
        """
        Compute the next optimal state following the optimal policy.
        :return: the next state following the optimal policy
        """
        from MAPFSolver.Utilities.AStar import AStar
        from MAPFSolver.Utilities.SolverSettings import SolverSettings
        solver = AStar(SolverSettings())
        path = solver.find_path(self._map, self._position, self._goal)
        next_pos = path[1]
        return SingleAgentState(self._map, self._goal, next_pos, self._solver_settings, parent=self)

    def compute_heuristics(self):
        """
        Compute the heuristic value for this state using the set heuristic. (h-value)
        """
        self._h = self._solver_settings.get_heuristic_object().compute_heuristic(self._position, self._goal)

    def compute_cost(self):
        """
        Compute the cost of the current state. (g-value)
        For the case in which the agent need to stay in the goal for a goal occupation time, the time spent in the goal
        is not count in the cost.
        """
        if self.is_root():
            self._g = 0
        else:
            list_of_states = [self]
            state = self
            while not state.is_root():
                state = state.parent()
                list_of_states.append(state)

            self._g = 0
            for i, s in enumerate(list_of_states):
                if not s.goal_test():
                    if i == 0:
                        self._g = len(list_of_states) - 1
                    else:
                        self._g = len(list_of_states) - i
                    break

    def goal_test(self):
        """
        Return True if the agent is on the goal position.
        """
        return self._position == self._goal

    def is_completed(self):
        """
        Return True if the current state is completed. If stay at goal assumption is set it just check that the agent
        has reached his goal, otherwise it checks that the agent has reached his goal and has already spent the goal
        occupation time there.
        If the settings requires that agents stays in goal also after arrived we just check the goal test, otherwise we
        check that the agent has already spent the needed time stopped in the goal.
        This function not means that the agent is already gone. It just tells if it has been completed or be in the
        time step of completion.
        """
        if self._solver_settings.stay_at_goal():
            return self.goal_test()
        else:
            state = self
            for i in range(self._solver_settings.get_goal_occupation_time()):
                if not state.goal_test():
                    return False
                state = state.parent()
                if not state:
                    return False
            return True

    def is_gone(self):
        """
        Return True if the agent has completed his task and he is already been removed from his goal at the given time
        step. If the stay_at_goal assumption is set than the agent will never be gone so it always returns False.
        Is different from is_completed because an agent can be completed but he disappear the next time_step.
        Se, we have to check that he's already spent the needed time in the goal before this state.
        """
        if self._solver_settings.stay_at_goal():
            return False
        else:
            state = self
            for i in range(self._solver_settings.get_goal_occupation_time()+1):
                if not state.goal_test():
                    return False
                state = state.parent()
                if not state:
                    return False
            return True

    def get_position(self):
        """
        Return the state position.
        """
        return self._position

    def get_positions_list(self):
        """
        Return the list of the positions of the single agent states. Since it is a single state only one
        """
        return [self.get_position()]

    def get_path_to_root(self):
        """
        Compute and return the path to the root. If stay_at_goal is True I truncate the repeated end goals.
        """
        path = []
        node = self

        if not self._solver_settings.stay_at_goal():  # Add to the list the goal position "goal_occ_time" times.
            counter = self._solver_settings.get_goal_occupation_time()
            while node.goal_test() and counter > 0:
                path.append(node._position)
                node = node.parent()
                counter -= 1

        while node.parent() is not None:  # Delete the extra states we don't need.
            if node.parent().goal_test():
                node = node.parent()
            else:
                break

        while node.parent() is not None:
            path.append(node._position)
            node = node.parent()
        path.append(node._position)
        path.reverse()
        return path

    def equal_position(self, other):
        """
        Return True if the state and the other state has the same position.
        :param other: state to compare position.
        """
        assert isinstance(other, SingleAgentState)
        return self._position == other._position

    def equal(self, other):
        """
        Return True if the state and the other state has the same position and the same time step.
        :param other: state to compare position.
        """
        assert isinstance(other, SingleAgentState)
        return self._position == other._position and self.time_step() == other.time_step()

    def __str__(self):
        return '[STATE -> F:' + str(self.f_value()) + ' G:' + str(self.g_value()) + ' H:' + str(self.h_value()) + ' '\
               + str(self._position) + ' TS:' + str(self.time_step()) + ']'
