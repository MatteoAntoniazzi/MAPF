from Heuristics.initialize_heuristics import initialize_heuristics
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
from Utilities.StatesQueue import StatesQueue
from Utilities.Agent import Agent


class AStar:
    def __init__(self, solver_settings):
        self._solver_settings = solver_settings
        self._heuristics = None
        self._frontier = None
        self._closed_list = None  # Keep all the states already expanded
        self._closed_list_of_positions = None  # Keep all the positions already visited

    def find_path(self, map, start_pos, goal_pos):
        """
        It computes the path from his start position to his goal position using the A* algorithm.
        It return the path as list of (x, y) positions
        """
        self.initialize_problem(map, start_pos, goal_pos)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.goal_test():
                path = cur_state.get_path_to_parent()
                goal = cur_state.get_position()
                for i in range(self._solver_settings.get_goal_occupation_time()-1):
                    path.append(goal)
                return path

            if cur_state.get_position() not in self._closed_list_of_positions:
                self._closed_list_of_positions.append(cur_state.get_position())
                expanded_nodes = cur_state.expand()
                self._frontier.add_list_of_states(expanded_nodes)

        return []

    def find_path_with_reservation_table(self, map, start_pos, goal_pos, reservation_table):
        """
        It computes the path from his start position to his goal position using the A* algorithm with reservation table.
        It return the path as list of (x, y) positions.

        Closed lists are used to accelerate the process. When a state with a conflict is found the closed list with the
        positions empty in order to allow the wait moves.
        """
        self.initialize_problem(map, start_pos, goal_pos)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                return cur_state.get_path_to_parent()

            if not self._closed_list.contains_state(cur_state):
                self._closed_list.add(cur_state)

                expanded_nodes = cur_state.expand()

                expanded_nodes_no_conflicts = []
                for state in expanded_nodes:

                    busy_times = reservation_table.get(state.get_position(), [])
                    cur_pos_busy_times = reservation_table.get(cur_state.get_position(), [])

                    if not (state.time_step() in busy_times or (state.time_step() - 1 in busy_times and
                                                                state.time_step() in cur_pos_busy_times)):
                        expanded_nodes_no_conflicts.append(state)

                    if state.time_step() not in busy_times:
                        if self._solver_settings.is_edge_conflict():
                            if not (state.time_step() - 1 in busy_times and state.time_step() in cur_pos_busy_times):
                                expanded_nodes_no_conflicts.append(state)
                        else:
                            expanded_nodes_no_conflicts.append(state)


                self._frontier.add_list_of_states(expanded_nodes_no_conflicts)

        return []

    def find_path_with_constraints(self, map, start_pos, goal_pos, constraints, transactional_constraints=None):
        """
        It computes the path from his start position to his goal position using the A* algorithm with reservation table.
        It return the path as list of (x, y) positions.

        Closed lists are used to accelerate the process. When a state with a conflict is found the closed list with the
        positions empty in order to allow the wait moves.
        """
        self.initialize_problem(map, start_pos, goal_pos)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                return cur_state.get_path_to_parent()

            if not self._closed_list.contains_state(cur_state):
                self._closed_list.add(cur_state)

                expanded_nodes = cur_state.expand()

                expanded_nodes_no_conflicts = []
                for state in expanded_nodes:
                    if (state.get_position(), state.time_step()) not in constraints:
                        if (state.predecessor().get_position(), state.get_position(), state.time_step()) not in \
                                transactional_constraints or transactional_constraints is None:
                            expanded_nodes_no_conflicts.append(state)
                self._frontier.add_list_of_states(expanded_nodes_no_conflicts)

        return []

    def initialize_problem(self, map, start_pos, goal_pos):
        problem_instance = ProblemInstance(map, [Agent(0, start_pos, goal_pos)])
        self._heuristics = initialize_heuristics(self._solver_settings.get_heuristics_str(), problem_instance)

        self._frontier = StatesQueue()
        self._closed_list = StatesQueue()
        self._closed_list_of_positions = []

        starter_state = SingleAgentState(map, 0, goal_pos, start_pos, 0, self._heuristics,
                                         self._solver_settings.get_goal_occupation_time())
        self._frontier.add(starter_state)

