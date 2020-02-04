from MAPFSolver.Utilities.Agent import Agent
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
from MAPFSolver.Utilities.StatesQueue import StatesQueue


class AStar:
    """
    This class represents a single agent A* solver.
    """
    def __init__(self, solver_settings):
        self._solver_settings = solver_settings
        self._heuristics = None
        self._frontier = None
        self._closed_list = None  # Keep all the states already expanded
        self._closed_list_of_positions = None  # Keep all the positions already visited

    def find_path(self, problem_map, start_pos, goal_pos):
        """
        It computes the path from his start position to his goal position using the A* algorithm.
        It return the path as list of (x, y) positions. If stay in goal is True it will return the goal position once,
        otherwise it will return the goal position as many times as the value of goal occupation time.
        """
        self.initialize_problem(problem_map, start_pos, goal_pos)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.goal_test():
                path = cur_state.get_path_to_root()
                goal = cur_state.get_position()
                if not self._solver_settings.stay_in_goal():
                    for i in range(self._solver_settings.get_goal_occupation_time()-1):
                        path.append(goal)
                return path

            if cur_state.get_position() not in self._closed_list_of_positions:
                self._closed_list_of_positions.append(cur_state.get_position())
                expanded_nodes = cur_state.expand()
                self._frontier.add_list_of_states(expanded_nodes)

        return []

    def find_path_with_reservation_table(self, problem_map, start_pos, goal_pos, reservation_table, completed_pos=None):
        """
        It computes the path from his start position to his goal position using the A* algorithm with reservation table.
        It return the path as list of (x, y) positions. Closed lists are used to accelerate the process.
        :param problem_map: map of the problem.
        :param start_pos: starting position of the agent.
        :param goal_pos: goal position of the agent.
        :param reservation_table: it's a dictionary that keeps for each position the list of busy time steps.
        :param completed_pos: is the list of all the goal positions. So, we know the positions where the agent in the
        goal are placed and those positions will be busy from the last time step in the reservation table forever.
        This is used only if the option stay in goal is active.
        :return: the path for the agent, if found any.
        """
        self.initialize_problem(problem_map, start_pos, goal_pos)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                return cur_state.get_path_to_root()

            if not self._closed_list.contains_state(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand()

                expanded_nodes_no_conflicts = []
                for state in expanded_nodes:
                    busy_times = reservation_table.get(state.get_position(), [])
                    cur_pos_busy_times = reservation_table.get(cur_state.get_position(), [])

                    # If the position is already occupied.
                    conflict_with_other_agent = state.time_step() in busy_times

                    if self._solver_settings.stay_in_goal():
                        # If True means that the position is busy due to an agent that occupy his goal forever.
                        conflict_with_goal = state.get_position() in completed_pos and \
                                             state.time_step() >= busy_times[len(busy_times) - 1]
                        # If True means exists another agent already planned that will pass on this position in future.
                        block_previous_agents_when_in_goal = state.goal_test() and not (len(busy_times) == 0) and \
                                                             not (any(y < state.time_step() for y in busy_times))
                        conflict_with_other_agent = conflict_with_other_agent and conflict_with_goal and \
                                                    block_previous_agents_when_in_goal

                    if not conflict_with_other_agent:
                        if self._solver_settings.is_edge_conflict():
                            if not (state.time_step()-1 in busy_times and state.time_step() in cur_pos_busy_times):
                                # not(if the time step before the position was busy and the before position is busy now)
                                expanded_nodes_no_conflicts.append(state)
                        else:
                            expanded_nodes_no_conflicts.append(state)

                self._frontier.add_list_of_states(expanded_nodes_no_conflicts)

        return []

    def find_path_with_constraints(self, problem_map, start_pos, goal_pos, vertex_constraints, edge_constraints=None):
        """
        It computes the path from his start position to his goal position using the A* algorithm with reservation table.
        It return the path as list of (x, y) positions. Closed lists are used to accelerate the process.
        :param problem_map: map of the problem.
        :param start_pos: start position of the agent.
        :param goal_pos: goal position of the agent.
        :param vertex_constraints: list of vertex constraints.
        :param edge_constraints: list of edge constraints.
        :return: solution path.
        """
        self.initialize_problem(problem_map, start_pos, goal_pos)
        if edge_constraints is None:
            edge_constraints = []

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                return cur_state.get_path_to_root()

            if not self._closed_list.contains_state(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand()

                expanded_nodes_no_conflicts = []
                for state in expanded_nodes:
                    if (state.get_position(), state.time_step()) not in vertex_constraints:
                        if (state.predecessor().get_position(), state.get_position(), state.time_step()) not in \
                                edge_constraints or edge_constraints is None:
                            expanded_nodes_no_conflicts.append(state)
                self._frontier.add_list_of_states(expanded_nodes_no_conflicts)

        return []

    def initialize_problem(self, problem_map, start_pos, goal_pos):
        """
        Initialize the A* problem. Initialize the frontier and the closed lists.
        :param problem_map: map of the problem.
        :param start_pos: start position of the agent.
        :param goal_pos: goal position of the agent.
        """
        problem_instance = ProblemInstance(problem_map, [Agent(0, start_pos, goal_pos)])
        self._solver_settings.initialize_heuristic(problem_instance)

        self._frontier = StatesQueue()
        self._closed_list = StatesQueue()
        self._closed_list_of_positions = []

        starter_state = SingleAgentState(problem_map, goal_pos, start_pos, self._solver_settings)
        self._frontier.add(starter_state)


"""
prob_map = generate_random_map(8, 8, 0)
solver_settings = SolverSettings(objective_function="SOC", stay_in_goal=True,  goal_occupation_time=4,
                                 is_edge_conflict=True)
solver = AStar(solver_settings)

solution_path = solver.find_path_with_constraints(prob_map, (6, 6), (0, 4), [((4, 6), 3)], [((5, 6), (4, 6), 2)])
print(solution_path)
"""