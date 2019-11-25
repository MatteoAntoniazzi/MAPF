from Utilities.MAPFSolver import MAPFSolver
from IncreasingCostTreeSearch.IncreasingCostTreeNode import IncreasingCostTreeNode
from IncreasingCostTreeSearch.IncreasingCostTreeQueue import IncreasingCostTreeQueue


class IncreasingCostTreeSearch(MAPFSolver):
    def __init__(self, heuristics_str):
        super().__init__(heuristics_str)
        self._frontier = None
        self._closed_list = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False, print_output=True):
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            cur_state = self._frontier.pop()

            if verbose:
                print("NODE: ", cur_state.path_costs_vector())

            if cur_state.is_goal():
                solution = cur_state.solution()
                if print_output:
                    print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                          " Total time: ", max([len(path)-1 for path in solution]), " Total cost:", cur_state.total_cost())
                return solution

            if not self._closed_list.contains_node(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand()
                self._n_of_expanded_nodes += len(expanded_nodes)
                self._n_of_loops += 1
                self._frontier.add_list_of_nodes(expanded_nodes)

        return []

    def initialize_problem(self, problem_instance):
        self._frontier = IncreasingCostTreeQueue()
        self._closed_list = IncreasingCostTreeQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        starter_state = IncreasingCostTreeNode(problem_instance, heuristics_str=self._heuristics_str)
        self._frontier.add(starter_state)
