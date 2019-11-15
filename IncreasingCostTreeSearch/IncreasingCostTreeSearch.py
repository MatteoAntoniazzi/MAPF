from Solvers.MAPFSolver import MAPFSolver
from IncreasingCostTreeSearch.IncreasingCostTreeNode import IncreasingCostTreeNode
from QueueStructures.IncreasingCostTreeQueue import IncreasingCostTreeQueue


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
            # self._frontier.sort_by_total_cost()
            cur_state = self._frontier.pop()

            if cur_state.is_goal():
                return cur_state.solution()

        print(self._frontier.pop()._path_costs_vector)



    def initialize_problem(self, problem_instance):
        self._frontier = IncreasingCostTreeQueue()
        self._closed_list = IncreasingCostTreeQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        starter_state = IncreasingCostTreeNode(problem_instance, heuristics_str=self._heuristics_str)
        self._frontier.add(starter_state)
