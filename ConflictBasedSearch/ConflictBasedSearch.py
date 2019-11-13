from ConflictBasedSearch.ConstraintTreeNode import ConstraintTreeNode
from Heuristics.initialize_heuristics import initialize_heuristics
from QueueStructures.ConstraintTreeNodesQueue import ConstraintTreeNodesQueue
from Solvers.MAPFSolver import MAPFSolver


class ConflictBasedSearch(MAPFSolver):
    def __init__(self, heuristics_str):
        super().__init__(heuristics_str)
        self._frontier = None
        self._closed_list = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False, print_output=True):
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_total_cost()
            cur_state = self._frontier.pop()

            print("Number of constraints: ", len(cur_state.constraints()) + len(cur_state.transactional_constraints()))

            conflict = cur_state.check_conflicts()
            if conflict is None:
                if print_output:
                    print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                          " Total time: ", cur_state.total_time(), " Total cost:", cur_state.total_cost())
                return cur_state.solution()

            # Expand the Constraint Tree
            expanded_nodes = cur_state.expand()
            self._n_of_expanded_nodes += len(expanded_nodes)
            self._n_of_loops += 1
            self._frontier.add_list_of_nodes(expanded_nodes)

    def high_level_search(self):
        pass

    def low_level_search(self):
        pass

    def initialize_problem(self, problem_instance):
        self._frontier = ConstraintTreeNodesQueue()
        self._closed_list = ConstraintTreeNodesQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        starter_state = ConstraintTreeNode(problem_instance, heuristics_str=self._heuristics_str)
        self._frontier.add(starter_state)
