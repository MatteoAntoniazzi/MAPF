from AStar import AStar
from Utilities.macros import *


class IncreasingCostTreeNode:
    def __init__(self, problem_instance, path_costs_vector=None, parent=None, heuristics_str="Manhattan"):
        self._problem_instance = problem_instance
        self._heuristics_str = heuristics_str
        self._parent = parent

        if parent is None:
            self._path_costs_vector = self.compute_root_path_costs_vector()
        else:
            self._path_costs_vector = path_costs_vector     # [C1, C2, C3, ...]

        self._mdd_vector = self.compute_mdds()
        self._total_mdd = self.compute_total_mdd()
        self._paths_vector = None                       # vector with all the possible paths for each agent
        self._solution = None

    def expand(self):
        pass

    def compute_mdds(self):
        for i, agent in enumerate(self._problem_instance.get_agents()):
            pass

        return 0

    def compute_single_mdd(self):
        return 0

    def compute_total_mdd(self):
        return 0

    def is_goal(self):
        return self._solution is not None

    def solution(self):
        return self._solution

    def path_costs_vector(self):
        return self._path_costs_vector

    def compute_root_path_costs_vector(self):
        path_costs_vector = []
        solver = AStar(self._heuristics_str)
        for agent in self._problem_instance.get_agents():
            path = solver.find_path(self._problem_instance.get_map(), agent.get_start(), agent.get_goal())
            cost = len(path) - GOAL_OCCUPATION_TIME
            path_costs_vector.append(cost)
        return path_costs_vector
