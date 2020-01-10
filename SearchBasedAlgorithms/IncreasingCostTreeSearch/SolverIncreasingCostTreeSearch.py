"""
ICTS algorithm is a complete and optimal algorithm. It works in a two level way:
- The high-level performs a search on a new search tree called increasing cost tree (ICT). Each node in the ICT consists
  of a k-vector [C 1 , C 2 , . . . C k ] which represents all possible solutions in which the cost of the individual
  path of each agent a i is exactly C i.
- The low-level performs a goal test on each of these tree nodes.
"""
from Utilities.MAPFSolver import MAPFSolver
from SearchBasedAlgorithms.IncreasingCostTreeSearch.IncreasingCostTreeNode import IncreasingCostTreeNode
from SearchBasedAlgorithms.IncreasingCostTreeSearch.IncreasingCostTreeQueue import IncreasingCostTreeQueue


class SolverIncreasingCostTreeSearch(MAPFSolver):
    def __init__(self, solver_settings, objective_function):
        super().__init__(solver_settings, objective_function)
        self._frontier = None
        self._closed_list = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False, print_output=True, return_infos=False):
        """
        Solve the MAPF problem using the ICTS algorithm returning the paths as lists of list of (x, y) positions.
        """
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            if self._objective_function == "SOC":
                self._frontier.sort_by_total_cost()
            else:
                self._frontier.sort_by_makespan()
            cur_state = self._frontier.pop()

            if verbose:
                print("NODE: ", cur_state.path_costs_vector())

            if cur_state.is_goal():
                solution = cur_state.solution()
                if print_output:
                    print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                          " Total time: ", max([len(path)-1 for path in solution]), " Total cost:", cur_state.total_cost())
                if return_infos:
                    output_infos = {
                        "sum_of_costs": cur_state.total_cost(),
                        "makespan": max([len(path)-1 for path in solution]),
                        "expanded_nodes": self._n_of_expanded_nodes
                    }
                    return solution, output_infos
                return solution

            if not self._closed_list.contains_node(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand()
                self._n_of_expanded_nodes += len(expanded_nodes)
                self._n_of_loops += 1
                self._frontier.add_list_of_nodes(expanded_nodes)

        return []

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier and the closed list for the given problem.
        """
        self._frontier = IncreasingCostTreeQueue()
        self._closed_list = IncreasingCostTreeQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        starter_state = IncreasingCostTreeNode(problem_instance, self._solver_settings)
        self._frontier.add(starter_state)

    def __str__(self):
        return "Increasing Cost Tree Solver using " + self._solver_settings.get_heuristics_str() + " heuristics minimazing" + self._objective_function
