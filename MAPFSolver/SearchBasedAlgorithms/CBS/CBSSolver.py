from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.SearchBasedAlgorithms.CBS.ConstraintTreeNode import ConstraintTreeNode
from MAPFSolver.SearchBasedAlgorithms.CBS.ConstraintTreeNodesQueue import ConstraintTreeNodesQueue
from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan, check_conflicts_with_type
import time


class CBSSolver(AbstractSolver):
    """
    The key idea of CBS (Conflict based search) is to grow a set of constraints for each of the agents and find paths that are consistent with
    these constraints. If these paths have conflicts, and are thus invalid, the conflicts are resolved by adding new
    constraints. CBS works in two levels. At the high level conflicts are found and constraints are added. The low-level
    updates the agents paths to be consistent with the new constraints.
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

    def solve(self, problem_instance, verbose=False, return_infos=False, time_out=None):
        """
        Solve the MAPF problem using the CBS algorithm returning the paths as lists of list of (x, y) positions.
        :param problem_instance: problem instance to solve
        :param verbose: if True will be printed some computation infos on terminal.
        :param return_infos: if True returns in addition to the paths a struct with the output information.
        :param time_out: max time for computing the solution. If the time is over it returns an empty solution.
        The time is expressed in seconds.
        :return: list of paths, and if return_infos is True some output information.
        """
        start = time.time()

        self.initialize_problem(problem_instance)

        paths = self.high_level_search(verbose=verbose, time_out=time_out)

        if paths:
            soc = calculate_soc(paths, self._solver_settings.stay_at_goal(),
                                self._solver_settings.get_goal_occupation_time())
            makespan = calculate_makespan(paths, self._solver_settings.stay_at_goal(),
                                          self._solver_settings.get_goal_occupation_time())
            output_infos = self.generate_output_infos(soc, makespan, self._n_of_generated_nodes,
                                                  self._n_of_expanded_nodes, time.time() - start)

            if verbose:
                print("PROBLEM SOLVED: ", output_infos)
        else:
            output_infos = self.generate_output_infos(None, None, self._n_of_generated_nodes,
                                                      self._n_of_expanded_nodes, time.time() - start)
            return [] if not return_infos else ([], output_infos)

        return paths if not return_infos else (paths, output_infos)

    def high_level_search(self, verbose=False, time_out=None):
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
        start = time.time()

        while not self._frontier.is_empty():
            self._frontier.sort_by_cost()
            cur_state = self._frontier.pop()

            if time_out is not None:
                if time.time() - start > time_out:
                    break

            if verbose:
                print("Expanding state ... Tot constr:",
                      len(cur_state.vertex_constraints()) + len(cur_state.edge_constraints()),
                      " Vertex constr: ", cur_state.vertex_constraints(),
                      "Edge constr: ", cur_state.edge_constraints())

            if cur_state.is_valid():
                return cur_state.solution()

            # Expand the Constraint Tree
            expanded_nodes = cur_state.expand()
            self._n_of_generated_nodes += len(expanded_nodes)
            self._n_of_expanded_nodes += 1
            self._frontier.add_list_of_nodes(expanded_nodes)

        return []

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier for the given problem.
        """
        self._frontier = ConstraintTreeNodesQueue()
        self._n_of_generated_nodes = 1
        self._n_of_expanded_nodes = 0

        starter_state = ConstraintTreeNode(problem_instance, self._solver_settings)

        self._frontier.add(starter_state)
