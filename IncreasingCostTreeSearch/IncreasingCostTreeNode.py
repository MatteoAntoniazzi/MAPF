import itertools

from AStar import AStar
from IncreasingCostTreeSearch.MDD import MDD
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

        self._solution = None
        self._mdd_vector = self.compute_mdds()
        if self._path_costs_vector == [8, 8]:
            print("MDD 8 8", end=" ")
            [print(i.get_paths(), end=" ") for i in self._mdd_vector]
            print(" ")
        self._total_mdd = self.compute_total_mdd()

    def expand(self):
        candidate_list = []

        for i, agent in enumerate(self._problem_instance.get_agents()):
            path_costs = self._path_costs_vector.copy()
            path_costs[i] += 1
            candidate_list.append(IncreasingCostTreeNode(self._problem_instance, path_costs_vector=path_costs,
                                                         parent=self))
        return candidate_list

    def compute_mdds(self):
        mdd_vector = []
        for i, agent in enumerate(self._problem_instance.get_agents()):
            mdd_vector.append(MDD(self._problem_instance.get_map(), agent, self._path_costs_vector[i]))
        return mdd_vector

    def compute_total_mdd(self):
        # Creo tutte le possibili combinazioni di paths
        candidate_paths = []
        for mdd in self._mdd_vector:
            candidate_paths.append(mdd.get_paths())
        candidate_solutions = list(itertools.product(*candidate_paths))

        # Controllo se esiste una combinazione valida
        for solution in candidate_solutions:
            if self.check_validity(solution):
                self._solution = solution
                return solution
        return None

    def check_validity(self, solution):
        # print("COST:", len(solution[0]) - 5 + len(solution[1]) - 5)
        # print("sol: ")
        # print(solution[0])
        # print(solution[1])

        reservation_table = dict()

        for i, path in enumerate(solution):
            for ts, pos in enumerate(path):
                if reservation_table.get((pos, ts)) is not None:
                    # print("LINEAR CONFLICT")
                    return False
                reservation_table[(pos, ts)] = i

        for ag_i, path in enumerate(solution):
            for ts, pos in enumerate(path):
                ag_j = reservation_table.get((pos, ts - 1))  # Agent in the pos position at the previous time step
                if ag_j is not None and ag_j != ag_i:
                    if len(solution[ag_j]) > ts:
                        if solution[ag_j][ts] == path[ts - 1]:
                            # print("TRANS CONFLICT")
                            return False

        return True

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

    def total_cost(self):
        return sum(self._path_costs_vector)

