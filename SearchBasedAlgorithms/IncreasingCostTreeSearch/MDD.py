"""
Multi-value decision diagram (MDD) for a single agent. It is represented by a list of paths from the start to the goal.
"""
from SearchBasedAlgorithms.IncreasingCostTreeSearch.MDDNode import MDDNode
from SearchBasedAlgorithms.IncreasingCostTreeSearch.MDDQueue import MDDQueue


class MDD:
    def __init__(self, map, agent, cost, goal_occupation_time):
        self._map = map
        self._agent = agent
        self._cost = cost
        self._goal_occupation_time = goal_occupation_time
        self._paths = []
        self._nodes = MDDQueue()
        self.build_mdd()

    def build_mdd(self):
        """
        Multi-value decision diagram for the specific agent.
        """
        root = MDDNode(self._map, self._agent.get_start())
        self._nodes.add(root)

        frontier = MDDQueue()
        frontier.add(root)

        while not frontier.is_empty():
            frontier.sort_by_time_step()
            cur_node = frontier.pop()

            if cur_node.time_step() > self._cost:
                return

            if cur_node.time_step() == self._cost:
                if cur_node.position() == self._agent.get_goal():
                    self._paths = cur_node.get_paths_to_parent(self._goal_occupation_time)

            expanded_nodes = cur_node.expand()

            for node in expanded_nodes:
                if self._nodes.contains_node(node):
                    self._nodes.add_parent_to_node(node, cur_node)
                else:
                    frontier.add(node)
                    self._nodes.add(node)

    def get_paths(self):
        return self._paths
