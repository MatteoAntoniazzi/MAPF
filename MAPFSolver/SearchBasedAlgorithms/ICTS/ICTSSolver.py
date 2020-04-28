from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from MAPFSolver.SearchBasedAlgorithms.ICTS.ICTNode import ICTNode
from MAPFSolver.SearchBasedAlgorithms.ICTS.ICTQueue import ICTQueue
from threading import Thread, Event
import time


class ICTSSolver(AbstractSolver):
    """
    ICTS (Increasing Cost Tree Search) algorithm is a complete and optimal algorithm. It works in a two level way:
    - The high-level performs a search on a new search tree called increasing cost tree (ICT). Each node in the ICT
      consists of a k-vector [C 1 , C 2 , . . . C k ] which represents all possible solutions in which the cost of the
      individual path of each agent a i is exactly C i.
    - The low-level performs a goal test on each of these tree nodes.
    """

    def __init__(self, solver_settings):
        """
        Initialize the ICTS solver.
        :param solver_settings: settings used by the ICTS solver.
        """
        super().__init__(solver_settings)
        self._frontier = None
        self._closed_list = None
        self._n_of_generated_nodes = 0
        self._n_of_expanded_nodes = 1
        self._solution = []

        self._stop_event = None

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the given MAPF problem with the ICTS algorithm and it returns, if exists, a solution.
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
        Solve the MAPF problem using the ICTS algorithm.
        :param problem_instance: problem instance to solve
        :param verbose: if True will be printed some computation infos on terminal.
        :return: list of paths, and if return_infos is True some output information.
        """
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_cost()
            cur_state = self._frontier.pop()

            if self._stop_event.is_set():
                break

            cur_state.initialize_node(self._stop_event, verbose=verbose)

            if cur_state.goal_test():
                self._solution = cur_state.solution()
                return

            # Standard version: no detect duplicates in the frontier.
            """if not self._closed_list.contains_node(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand()
                self._n_of_generated_nodes += len(expanded_nodes)
                self._n_of_expanded_nodes += 1
                self._frontier.add_list_of_nodes(expanded_nodes)"""

            # Version 2: duplicate detection in the frontier.
            self._closed_list.add(cur_state)
            expanded_nodes = cur_state.expand()

            expanded_nodes_not_in_closed_list = []
            for node in expanded_nodes:
                if not self._closed_list.contains_node(node) and not self._frontier.contains_node(node):
                    expanded_nodes_not_in_closed_list.append(node)

            self._n_of_generated_nodes += len(expanded_nodes_not_in_closed_list)
            self._n_of_expanded_nodes += 1
            self._frontier.add_list_of_nodes(expanded_nodes_not_in_closed_list)

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier and the closed list for the given problem.
        """
        self._frontier = ICTQueue()
        self._closed_list = ICTQueue()
        self._n_of_generated_nodes = 1
        self._n_of_expanded_nodes = 0

        starter_state = ICTNode(problem_instance, self._solver_settings)

        self._frontier.add(starter_state)

    def __str__(self):
        return "Increasing Cost Tree Solver using " + self._solver_settings.get_heuristic_str() + \
               " heuristics minimizing " + self._solver_settings.get_objective_function()
