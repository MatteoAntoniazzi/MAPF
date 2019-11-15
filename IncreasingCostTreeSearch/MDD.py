from IncreasingCostTreeSearch.MDDNode import MDDNode
from QueueStructures.MDDQueue import MDDQueue
from Utilities.macros import *


class MDD:
    def __init__(self, map, agent, cost):
        self._map = map
        self._agent = agent
        self._cost = cost
        self._paths = []
        self._ending_nodes = []
        self.build_mdd()

    def build_mdd(self):
        root = MDDNode(self._map, self._agent.get_start())

        frontier = MDDQueue()
        frontier.add(root)

        while not frontier.is_empty():
            frontier.sort_by_time_step()
            cur_node = frontier.pop()

            if cur_node.time_step() > self._cost:
                return

            if cur_node.time_step() == self._cost:
                if cur_node.position() == self._agent.get_goal():
                    self._ending_nodes.append(cur_node)
                    path = cur_node.get_path_to_parent()
                    goal_pos = cur_node.position()
                    for i in range(GOAL_OCCUPATION_TIME-1):
                        path.append(goal_pos)
                    self._paths.append(path)

            expanded_nodes = cur_node.expand()
            frontier.add_list_of_nodes(expanded_nodes)

    def get_paths(self):
        return self._paths
