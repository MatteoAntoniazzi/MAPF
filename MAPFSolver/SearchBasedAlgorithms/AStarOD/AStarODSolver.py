from MAPFSolver.SearchBasedAlgorithms.AStarOD.ODState import ODState
from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.StatesQueue import StatesQueue
from threading import Thread, Event
import time


class AStarODSolver(AbstractSolver):
    """
    A* multi agent solver with Operator Decomposition.
    """

    def __init__(self, solver_settings):
        """
        Initialize the A*+OD solver.
        :param solver_settings: settings used by the A* + OD solver.
        """
        super().__init__(solver_settings)
        self._frontier = None
        self._closed_list = None
        self._n_of_generated_nodes = 0
        self._n_of_expanded_nodes = 0
        self._solution = []

        self._stop_event = None

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the given MAPF problem with the A* algorithm with operator decomposition and it returns, if exists, a
        solution.
        :param problem_instance: instance of the problem to solve.
        :param verbose: if True, infos will be printed on terminal.
        :param return_infos: if True in addition to the paths will be returned also a structure with output infos.
        :return the solution as list of paths, and, if return_infos is True, a tuple composed by the solution and a
        struct with output information.
        """
        self._stop_event = Event()
        start = time.time()

        thread = Thread(target=self.solve_problem, args=(problem_instance, verbose,))
        thread.start()
        thread.join(timeout=self._solver_settings.get_time_out())
        self._stop_event.set()

        soc = calculate_soc(self._solution, self._solver_settings.stay_at_goal(),
                            self._solver_settings.get_goal_occupation_time())
        makespan = calculate_makespan(self._solution, self._solver_settings.stay_at_goal(),
                                      self._solver_settings.get_goal_occupation_time())

        output_infos = self.generate_output_infos(soc, makespan, self._n_of_generated_nodes, self._n_of_expanded_nodes,
                                                  time.time() - start)
        if verbose:
            print("Problem ended: ", output_infos)

        return self._solution if not return_infos else (self._solution, output_infos)

    def solve_problem(self, problem_instance, verbose=False):
        """
        Solve the MAPF problem using the A* algorithm with Operator Decomposition.
        :param problem_instance: problem instance to solve.
        :param verbose: if True will be printed some computation infos on terminal.
        """
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if self._stop_event.is_set():
                break

            if cur_state.is_completed():
                self._solution = cur_state.get_paths_to_root()
                return

            if not self._solver_settings.stay_at_goal():
                bool_test = False
                for single_agent_state in cur_state.get_single_agent_states():
                    if single_agent_state.goal_test() and not single_agent_state.is_gone():
                        bool_test = True

                if not cur_state.is_a_standard_state() or not self._closed_list.contains_state_same_positions(
                        cur_state) or (bool_test and not self._closed_list.contains_state(cur_state)):
                    if cur_state.is_a_standard_state():
                        self._closed_list.add(cur_state)
                    expanded_nodes = cur_state.expand(verbose=verbose)

                    self._n_of_generated_nodes += len(expanded_nodes)
                    self._n_of_expanded_nodes += 1
                    self._frontier.add_list_of_states(expanded_nodes)

            else:
                if not cur_state.is_a_standard_state() or not self._closed_list.contains_state_same_positions(cur_state):
                    if cur_state.is_a_standard_state():
                        self._closed_list.add(cur_state)
                    expanded_nodes = cur_state.expand(verbose=verbose)

                    self._n_of_generated_nodes += len(expanded_nodes)
                    self._n_of_expanded_nodes += 1
                    self._frontier.add_list_of_states(expanded_nodes)

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier and the heuristic for the given problem.
        """
        self._solver_settings.initialize_heuristic(problem_instance)
        self._frontier = StatesQueue()
        self._closed_list = StatesQueue()
        self._n_of_generated_nodes = 1
        self._n_of_expanded_nodes = 0

        single_agents_states = []
        for agent in problem_instance.get_agents():
            s = SingleAgentState(problem_instance.get_map(), agent.get_goal(), agent.get_start(), self._solver_settings)
            single_agents_states.append(s)

        starter_state = ODState(single_agents_states, self._solver_settings)
        self._frontier.add(starter_state)
