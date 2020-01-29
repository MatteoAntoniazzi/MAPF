"""
The key idea of CBS is to grow a set of constraints for each of the agents and find paths that are consistent with these
constraints. If these paths have conflicts, and are thus invalid, the conflicts are resolved by adding new constraints.
CBS works in two levels. At the high level conflicts are found and constraints are added. The low-level updates the
agents paths to be consistent with the new constraints.
"""
from MAPFSolver.Utilities.MAPFSolver import MAPFSolver
from SearchBasedAlgorithms.ConflictBasedSearch.ConstraintTreeNode import ConstraintTreeNode
from SearchBasedAlgorithms.ConflictBasedSearch.ConstraintTreeNodesQueue import ConstraintTreeNodesQueue
import time


class SolverConflictBasedSearch(MAPFSolver):
    def __init__(self, solver_settings):
        super().__init__(solver_settings)
        self._frontier = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False, print_output=True, return_infos=False):
        """
        Solve the MAPF problem using the CBS algorithm returning the paths as lists of list of (x, y) positions.
        """
        self.initialize_problem(problem_instance)
        if return_infos:
            solution, output_infos = self.high_level_search(verbose=verbose, print_output=print_output,
                                                            return_infos=return_infos)
            return solution, output_infos
        else:
            solution = self.high_level_search(verbose=verbose, print_output=print_output, return_infos=return_infos)
            return solution

    def high_level_search(self, verbose=False, print_output=True, return_infos=False):
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

            if verbose:
                print("Exapanding state ... Number of constraints: ", 
                      len(cur_state.constraints()) + len(cur_state.transactional_constraints()))

            conflict = cur_state.check_conflicts()
            if conflict is None:
                if print_output:
                    print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                          " Total time: ", cur_state.total_time(), " Total cost:", cur_state.total_cost())
                if return_infos:
                    output_infos = {
                        "sum_of_costs": cur_state.total_cost(),
                        "makespan": cur_state.total_time(),
                        "expanded_nodes": self._n_of_expanded_nodes,
                        "computation_time": time.time() - start
                    }
                    return cur_state.solution(), output_infos

                return cur_state.solution()

            # Expand the Constraint Tree
            expanded_nodes = cur_state.expand()
            self._n_of_expanded_nodes += len(expanded_nodes)
            self._n_of_loops += 1
            self._frontier.add_list_of_nodes(expanded_nodes)

        if return_infos:
            output_infos = {
                "sum_of_costs": 0,
                "makespan": 0,
                "expanded_nodes": 0,
                "computation_time": 0
            }
            return [], output_infos

        return []

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier for the given problem.
        """
        self._frontier = ConstraintTreeNodesQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        starter_state = ConstraintTreeNode(problem_instance, self._solver_settings)
        self._frontier.add(starter_state)

    def __str__(self):
        return "Conflict Based Search Solver using " + self._solver_settings.get_heuristic_str() + \
               " heuristics minimazing " + self._solver_settings.get_objective_function()