from MAPFSolver.SearchBasedAlgorithms.ICTS.MDDNode import MDDNode
from MAPFSolver.SearchBasedAlgorithms.ICTS.MDDQueue import MDDQueue


class MDD:
    """
    Multi-value decision diagram (MDD) for a single agent. It is represented by a list of paths from the start to the
    goal.
    """

    def __init__(self, problem_map, agent, cost, solver_settings):
        """
        Initialize the Multi-value Decision Diagram.
        :param problem_map: map of the problem.
        :param agent: agent involved.
        :param cost: maximum cost for which computing all the possible paths.
        :param solver_settings: settings of the solver
        """
        self._problem_map = problem_map
        self._agent = agent
        self._cost = cost
        self._solver_settings = solver_settings

        self._nodes = MDDQueue()
        self._root = None
        self._goal_node = None

        self.build_mdd()

    def build_mdd(self):
        """
        Multi-value decision diagram for the specific agent.
        """
        self._root = MDDNode(self._problem_map, self._agent.get_goal(), self._agent.get_start())
        self._nodes.add(self._root)

        frontier = MDDQueue()
        frontier.add(self._root)

        while not frontier.is_empty():
            frontier.sort_by_time_step()
            cur_node = frontier.pop()

            if cur_node.time_step() > self._cost:
                return True

            if cur_node.time_step() == self._cost:
                if cur_node.goal_test():
                    self._goal_node = cur_node
                    build_children_descendant(cur_node)

            expanded_nodes = cur_node.expand()

            for node in expanded_nodes:
                if self._nodes.contains_node(node):
                    self._nodes.add_parent_to_node(node, cur_node)
                else:
                    frontier.add(node)
                    self._nodes.add(node)

        return False

    def get_paths(self):
        """
        Returns all the possible paths of length equal to the cost.
        """
        return self._goal_node.get_paths_to_root(self._solver_settings)

    def get_root_node(self):
        """
        Return the reference to the root node.
        """
        return self._root

    def get_cost(self):
        """
        Returns the max cost of this MDD.
        """
        return self._cost


def build_children_descendant(goal_node):
    """
    Complete the building of the MDD. It adds at each node in the final MDD the children starting from the bottom.
    Because we need to keep only the nodes involved in paths that ends in the goal state. So we construct this MDD
    by starting from the bottom and going up, adding for each node the list of valid children. Since we start from
    we just need to add the nodes we encounter going up.
    This in order to have a way to going down through the nodes starting from the root.
    """
    node = goal_node

    while node.parent() is not None and len(node.parent()) == 1:
        node.parent()[0].add_child(node)
        node = node.parent()[0]

    if node.parent() is not None:
        if len(node.parent()) > 1:
            for parent in node.parent():
                parent.add_child(node)
                build_children_descendant(parent)

