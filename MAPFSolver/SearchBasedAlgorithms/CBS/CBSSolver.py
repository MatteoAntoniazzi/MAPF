from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.SearchBasedAlgorithms.CBS.ConstraintTreeNode import ConstraintTreeNode
from MAPFSolver.SearchBasedAlgorithms.CBS.ConstraintTreeNodesQueue import ConstraintTreeNodesQueue
from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from threading import Thread, Event

import time


class CBSSolver(AbstractSolver):
    """
    The key idea of CBS (Conflict based search) is to grow a set of constraints for each of the agents and find paths
    that are consistent with these constraints. If these paths have conflicts, and are thus invalid, the conflicts are
    resolved by adding new constraints. CBS works in two levels. At the high level conflicts are found and constraints
    are added. The low-level updates the agents paths to be consistent with the new constraints.
    """

    def __init__(self, solver_settings):
        """
        Initialize the CBS solver.
        :param solver_settings: settings used by the CBS solver.
        """
        super().__init__(solver_settings)
        self._frontier = None
        self._n_of_generated_nodes = 0
        self._n_of_expanded_nodes = 0
        self._solution = []

        self._stop_event = None

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the given MAPF problem using the CBS algorithm and it returns, if exists, a solution.
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
        At the high-level, CBS searches a constraint tree (CT). A CT is a binary tree. Each node N in the CT contains
        the following fields of data:
        (1) A set of constraints (N.constraints). The root of the CT contains an empty set of constraints. The child of
        a node in the CT inherits the constraints of the parent and adds one new constraint for one agent.
        (2) A solution (N.solution). A set of k paths, one path for each agent. The path for agent a i must be
        consistent with the constraints of a i. Such paths are found by the low-level
        (3) The total cost (N.cost) of the current solution (summation over all the single-agent path costs). We denote
        this cost the f -value of the node.
        Node N in the CT is a goal node when N.solution is valid, i.e., the set of paths for all agents have no
        conflicts.
        """
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_cost()
            cur_state = self._frontier.pop()

            if self._stop_event.is_set():
                break

            if verbose:
                print("Expanding state ... Tot constr:",
                      len(cur_state.vertex_constraints()) + len(cur_state.edge_constraints()),
                      " Vertex constr: ", cur_state.vertex_constraints(),
                      "Edge constr: ", cur_state.edge_constraints())

            if cur_state.is_valid():
                self._solution = cur_state.solution()
                break

            expanded_nodes = cur_state.expand()
            self._n_of_generated_nodes += len(expanded_nodes)
            self._n_of_expanded_nodes += 1
            self._frontier.add_list_of_nodes(expanded_nodes)

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier for the given problem.
        """
        self._frontier = ConstraintTreeNodesQueue()
        self._n_of_generated_nodes = 1
        self._n_of_expanded_nodes = 0

        starter_state = ConstraintTreeNode(problem_instance, self._solver_settings)
        self._frontier.add(starter_state)
