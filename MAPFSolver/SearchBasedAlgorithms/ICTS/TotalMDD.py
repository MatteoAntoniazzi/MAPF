from MAPFSolver.SearchBasedAlgorithms.ICTS.MDDQueue import MDDQueue
from MAPFSolver.SearchBasedAlgorithms.ICTS.TotalMDDNode import TotalMDDNode


class TotalMDD:
    """
    Total Multi-value decision diagram (MDD). It represents the cartesian product of all the MDD of the agents.
    It also consider only the feasible nodes, by checking the presence of conflicts.
    """

    def __init__(self, problem_map, solver_settings, list_of_mdd, stop_event):
        self._problem_map = problem_map
        self._solver_settings = solver_settings
        self._list_of_mdd = list_of_mdd
        self._cost = max([mdd.get_cost() for mdd in self._list_of_mdd])

        self._stop_event = stop_event

        self._solution = []
        self._nodes = MDDQueue()
        self.build_total_mdd()

    def build_total_mdd(self):
        """
        Build the total multi-value decision diagram.
        """
        # list of initial mdd_nodes, (the first element of the list of nodes)
        list_of_root_mdd_nodes = []
        for agent_mdd in self._list_of_mdd:
            list_of_root_mdd_nodes.append(agent_mdd.get_root_node())

        root = TotalMDDNode(self._problem_map, self._solver_settings, list_of_root_mdd_nodes)
        self._nodes.add(root)

        frontier = MDDQueue()
        frontier.add(root)

        while not frontier.is_empty():
            frontier.sort_by_time_step()
            cur_node = frontier.pop()

            if self._stop_event.is_set():
                break

            if cur_node.time_step() > self._cost:
                break

            if cur_node.goal_test():
                self._solution = cur_node.get_paths_to_root()
                return

            expanded_nodes = cur_node.expand()

            for node in expanded_nodes:
                if self._nodes.contains_node(node):
                    self._nodes.add_parent_to_node(node, cur_node)
                else:
                    frontier.add(node)
                    self._nodes.add(node)

    def get_solution(self):
        """
        Returns all the possible paths of length equal to their respective cost.
        """
        return self._solution
