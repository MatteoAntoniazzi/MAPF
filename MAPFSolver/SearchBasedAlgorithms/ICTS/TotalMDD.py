from MAPFSolver.SearchBasedAlgorithms.ICTS.TotalMDDNode import TotalMDDNode
from MAPFSolver.SearchBasedAlgorithms.ICTS.TotalMDDQueue import TotalMDDQueue


class TotalMDD:
    """
    Total Multi-value decision diagram (MDD). It represents the cartesian product of all the MDD of the agents.
    It also consider only the feasible nodes, by checking the presence of conflicts.
    """

    def __init__(self, problem_map, solver_settings, list_of_mdd):
        self._problem_map = problem_map
        self._solver_settings = solver_settings
        self._list_of_mdd = list_of_mdd
        self._cost = max([mdd.get_cost() for mdd in self._list_of_mdd])

        self._paths = []
        self._nodes = TotalMDDQueue()
        self.build_mdd()

    def build_mdd(self):
        """
        Build the total multi-value decision diagram.
        """

        # list of initial mdd_nodes, (the first element of the list of nodes)
        list_of_root_mdd_nodes = []
        for agent_mdd in self._list_of_mdd:
            list_of_root_mdd_nodes.append(agent_mdd.get_root_node())

        root = TotalMDDNode(self._problem_map, self._solver_settings, list_of_root_mdd_nodes)
        self._nodes.add(root)

        frontier = TotalMDDQueue()
        frontier.add(root)

        while not frontier.is_empty():
            frontier.sort_by_time_step()
            cur_node = frontier.pop()

            if cur_node.time_step() > self._cost:
                print("ERRORE! NON PUO' SUPERARE IL COSTO!!")
                return True

            if cur_node.goal_test():
                self._paths = cur_node.get_path_to_root()
                return True

            expanded_nodes = cur_node.expand()

            for node in expanded_nodes:

                if self._nodes.contains_node(node):
                    self._nodes.add_parent_to_node(node, cur_node)
                else:
                    frontier.add(node)
                    self._nodes.add(node)

        print("Total MDD not build. ")
        return False

    def get_paths(self):
        """
        Returns all the possible paths of length equal to their respective cost.
        """
        return self._paths
