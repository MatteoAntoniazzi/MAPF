from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.StatesQueue import StatesQueue
from .MultiAgentState import MultiAgentState
from threading import Thread, Event
import time


class AStarSolver(AbstractSolver):
    """
    Classical A* multi-agent algorithm. It is complete and optimal.
    """

    def __init__(self, solver_settings):
        """
        Initialize the A* solver.
        :param solver_settings: settings used by the A* solver.
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
        Solve the given MAPF problem using the A* algorithm and it returns, if exists, a solution.
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

        if not self._solution:
            output_infos = self.generate_output_infos(None, None, self._n_of_generated_nodes, self._n_of_expanded_nodes,
                                                      time.time() - start)
        else:
            soc = calculate_soc(self._solution, self._solver_settings.stay_at_goal(),
                                self._solver_settings.get_goal_occupation_time())
            makespan = calculate_makespan(self._solution, self._solver_settings.stay_at_goal(),
                                          self._solver_settings.get_goal_occupation_time())

            output_infos = self.generate_output_infos(soc, makespan, self._n_of_generated_nodes,
                                                      self._n_of_expanded_nodes, time.time() - start)
        if verbose:
            print("Problem ended: ", output_infos)

        return self._solution if not return_infos else (self._solution, output_infos)

    def solve_problem(self, problem_instance, verbose=False):
        """
        Solve the MAPF problem using the A* algorithm.
        :param problem_instance: problem instance to solve
        :param verbose: if True will be printed some computation infos on terminal.
        """
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():

            if self._stop_event.is_set():
                break

            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                self._solution = cur_state.get_paths_to_root()
                return

            if not self._solver_settings.stay_at_goal():
                # In case agents disappear at goals we cannot delete duplicates since can happen that an agent wait that
                # another agent disappear in order to pass from that position. And this waiting is important in this
                # case since some agents is spending its required time in the goal.
                bool_test = False
                for single_agent_state in cur_state.get_single_agent_states():
                    if single_agent_state.goal_test() and not single_agent_state.is_gone():
                        bool_test = True

                if not self._closed_list.contains_state_same_positions(cur_state) or \
                        (bool_test and not self._closed_list.contains_state(cur_state)):
                    self._closed_list.add(cur_state)
                    expanded_nodes = cur_state.expand(verbose=verbose)
                    self._n_of_generated_nodes += len(expanded_nodes)
                    self._n_of_expanded_nodes += 1
                    self._frontier.add_list_of_states(expanded_nodes)

            else:
                # Standard version: no detect duplicates in the frontier.
                if not self._closed_list.contains_state_same_positions(cur_state):
                    self._closed_list.add(cur_state)
                    expanded_nodes = cur_state.expand(verbose=verbose)
                    self._n_of_generated_nodes += len(expanded_nodes)
                    self._n_of_expanded_nodes += 1
                    self._frontier.add_list_of_states(expanded_nodes)

                # Version 2: duplicate detection in the frontier.
                """self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand(verbose=verbose)
    
                expanded_nodes_not_in_closed_list = []
    
                for node in expanded_nodes:
                    if not self._closed_list.contains_state_same_positions(node):
                        frontier_state = self._frontier.contains_state_same_positions(node)
                        if frontier_state is None:
                            expanded_nodes_not_in_closed_list.append(node)
                        else:
                            if node.g_value() < frontier_state.g_value():
                                self._frontier.update(node)
    
                self._n_of_generated_nodes += len(expanded_nodes_not_in_closed_list)
                self._n_of_expanded_nodes += 1
                self._frontier.add_list_of_states(expanded_nodes_not_in_closed_list)"""

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

        starter_state = MultiAgentState(single_agents_states, self._solver_settings)
        self._frontier.add(starter_state)
